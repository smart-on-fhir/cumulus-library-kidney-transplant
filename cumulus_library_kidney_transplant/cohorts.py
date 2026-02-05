from typing import List
from pathlib import Path
from cumulus_library_kidney_transplant.variable import vsac_variables, custom_variables
from cumulus_library_kidney_transplant import fhir2sql, filetool

#####################################################################################################
# COHORTS
#
# irae__cohort are built from the irae__study_population
#
# irae__cohort_study_population contains Patient encounters matching `StudyBuilderConfig` .
# irae__cohort_study_population_{dx, rx, lab, proc, doc} tables contain additional FHIR resources.
#
# Each study $variable COHORT is selected from a irae__cohort_study_population* table.
#
#####################################################################################################
def list_variables() -> List[str]:
    """
    :return: List of all variables from VSAC anc custom sources.
    """
    return list(sorted(vsac_variables.list_view_variables()) +
                list(sorted(custom_variables.list_view_custom())))

def ctas(cohort: str, variable: str, where: list) -> str:
    """
    CTAS(create table as) will create a COHORT table as a subselection of the
    study population cohort table.

    :param cohort: study population cohort source
    :param variable: variable cohort target to create
    :param where: JOIN study_population cohort to variable cohort
    :return: str SQL for creating the variable cohort table.
    """
    from_list = fhir2sql.sql_list([cohort, variable])
    select_from = f'select * from \n {from_list}'
    sql = [f'create table {fhir2sql.name_cohort(variable)} as ',
           select_from, 'WHERE', fhir2sql.sql_and(where)]
    return '\n'.join(sql)

###############################################################################
# make cohort of type=aspect [dx, rx, proc, diag, lab]
###############################################################################
def cohort_dx(variable: str) -> Path:
    """
    :return: Path to athena SQL irae__cohort_dx_$variable
    """
    source = fhir2sql.name_study_population('dx')
    where = [f'{source}.dx_code = {variable}.code',
             f'{source}.dx_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(fhir2sql.name_cohort(variable), sql)

def cohort_rx(variable: str) -> Path:
    """
    :return: Path to athena SQL irae__cohort_rx_$variable
    :return:
    """
    source = fhir2sql.name_study_population('rx')
    where = [f'{source}.rx_code = {variable}.code',
             f'{source}.rx_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(fhir2sql.name_cohort(variable), sql)

def cohort_lab(variable: str) -> Path:
    """
    :return: Path to athena SQL irae__cohort_lab_$variable
    """
    source = fhir2sql.name_study_population('lab')
    where = [f'{source}.lab_observation_code = {variable}.code',
             f'{source}.lab_observation_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(fhir2sql.name_cohort(variable), sql)

def cohort_diag(variable: str) -> Path:
    """
    :return: Path to athena SQL irae__cohort_diag_$variable
    """
    source = fhir2sql.name_study_population('diag')
    where = [f'{source}.diag_code = {variable}.code',
             f'{source}.diag_code_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(fhir2sql.name_cohort(variable), sql)

def cohort_proc(variable: str) -> Path:
    """
    :return: Path to athena SQL irae__cohort_proc_$variable
    """
    source = fhir2sql.name_study_population('proc')
    where = [f'{source}.proc_code = {variable}.code',
             f'{source}.proc_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(fhir2sql.name_cohort(variable), sql)

def cohort_doc(variable: str) -> Path:
    """
    :return: Path to athena SQL irae__cohort_doc_$variable
    """
    source = fhir2sql.name_study_population('doc')
    where = [f'{source}.doc_type_code = {variable}.code',
             f'{source}.doc_type_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(fhir2sql.name_cohort(variable), sql)

###############################################################################
# Helper functions for UNION and WIDE variable representations
###############################################################################
def select_union(variable_list: list[str]) -> str:
    """
    :param variable_list: variable names (typically list of valuesets)
    :return: str SQL select UNION ALL for the provided variable list
    """
    sql = list()
    for variable in variable_list:
        variable = fhir2sql.name_simple(variable)
        select = f"\tselect distinct '{variable}'\t as variable, code, display, system, encounter_ref "
        from_table = f" from {fhir2sql.PREFIX}__cohort_{variable}"
        sql.append(select + from_table)
    return ' UNION ALL\n'.join(sql)

def select_lookup_variable_as_column(variable_list: list[str]) -> str:
    """
    :param variable_list: variable names (typically list of valuesets)
    :return: str SQL select variable table as column name
    """
    sql = list()
    for variable in variable_list:
        variable = fhir2sql.name_simple(variable)
        sql.append(f"\tIF(lookup.variable='{variable}', True) AS {variable}")
    return ',\n'.join(sql)

def select_lookup_wide(variable_list: list[str]) -> str:
    """
    :param variable_list: variable names (typically list of valuesets)
    :return: str SQL select variable for any arbitrary match (typically on the FHIR encounter)
    """
    sql = list()
    for variable in variable_list:
        variable = fhir2sql.name_simple(variable)
        sql.append(f"\tarbitrary({variable})    FILTER (where {variable} ) as {variable}")
    return ',\n'.join(sql)

###############################################################################
# MAKE variables UNION and WIDE representations
###############################################################################
def make_union() -> Path:
    """
    All study variable cohorts in one table.
    "see `template/cohort_variable.sql`"
    :return: Path to SQL file for each study variable 1+ `valueset`
    """
    template_sql = filetool.load_template(f"cohort_variable_union.sql")
    template_sql = template_sql.replace('$variable_list', select_union(list_variables()))
    cohort_name = fhir2sql.name_cohort('variable_union')
    target_file = filetool.path_athena(f"{cohort_name}.sql")

    return filetool.save_athena(target_file, template_sql)

def make_wide() -> Path:
    """
    All study variable cohorts in one table in WIDE format.
    each column is a study variable.

    see `template/cohort_variable_wide.sql`
    :return: Path to SQL file `athena/
    irae__cohort_study_variable_wide.sql`
    """
    variable_list = list_variables()
    template_sql = filetool.load_template(f"cohort_variable_wide.sql")
    template_sql = template_sql.replace('$variable_list_lookup', select_lookup_variable_as_column(variable_list))
    template_sql = template_sql.replace('$variable_list_wide', select_lookup_wide(variable_list))
    cohort_name = fhir2sql.name_cohort('variable_wide')
    target_file = filetool.path_athena(f"{cohort_name}.sql")

    return filetool.save_athena(target_file, template_sql)

def make_timeline() -> Path:
    return filetool.copy_template('cohort_variable_timeline.sql')

###############################################################################
# MAKE EACH Variable (make a cohort for each variable by itself)
###############################################################################
def make_each_study_variable() -> List[Path]:
    """
    :return: List of SQL files for each study variable COHORT.
    """
    group_list = list()
    for variable in list_variables():
        if '__dx' in variable:
            group_list.append(cohort_dx(variable))
        elif '__rx' in variable:
            group_list.append(cohort_rx(variable))
        elif '__lab' in variable:
            group_list.append(cohort_lab(variable))
        elif '__proc' in variable:
            group_list.append(cohort_proc(variable))
        elif '__doc' in variable:
            group_list.append(cohort_doc(variable))
        else:
            raise Exception(f'unknown variable type {variable}')
    return group_list

def make() -> List[Path]:
    """
    Make Patient COHORTS for each study variable from
    * `vsac_variables.py`   VSAC valueset definitions.
    * `custom_variables.py` custom valueset definitions.

    Each cohort contains FHIR Patient Encounters with variable metadata.

    Variable SQL are built from "template/" folder.

    For each $variable create an irae__cohort
    * $study_period_dx --> dx_$variable using FHIR Condition.code,system
    * $study_period_rx --> rx_$variable using FHIR MedicationRequest.code,system
    * $study_period_lab --> lab_$variable using FHIR Observation.code,system
    * $study_period_proc --> proc_$variable using FHIR Procedure.code,system
    * $study_period_doc --> doc_$variable using FHIR DocumentReference.code,system

    :return: List of SQL files for each study variable COHORT.
    """
    variables_each = make_each_study_variable()
    variables_all = [make_union(), make_wide(), make_timeline()]

    return variables_each + variables_all
