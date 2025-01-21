from typing import List
from pathlib import Path
from cumulus_library_kidney_transplant.variable import vsac_variables, custom_variables
from cumulus_library_kidney_transplant import fhir2sql, filetool

###############################################################################
# VSAC and custom variables list
###############################################################################
def list_variables() -> List[str]:
    return list(sorted(vsac_variables.list_view_variables()) + list(sorted(custom_variables.list_view_variables())))

###############################################################################
# COHORTS : create table as select from where
###############################################################################
def ctas(cohort: str, variable: str, where: list) -> str:
    from_list = fhir2sql.sql_list([cohort, variable])
    select_from = f'select * from \n {from_list}'
    sql = [f'create table {fhir2sql.name_cohort(variable)} as ',
           select_from, 'WHERE', fhir2sql.sql_and(where)]
    return '\n'.join(sql)

def cohort_dx(variable: str) -> Path:
    source = fhir2sql.name_study_population('dx')
    where = [f'{source}.dx_code = {variable}.code',
             f'{source}.dx_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(fhir2sql.name_cohort(variable), sql)

def cohort_rx(variable: str) -> Path:
    source = fhir2sql.name_study_population('rx')
    where = [f'{source}.rx_code = {variable}.code',
             f'{source}.rx_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(fhir2sql.name_cohort(variable), sql)

def cohort_lab(variable: str) -> Path:
    source = fhir2sql.name_study_population('lab')
    where = [f'{source}.lab_observation_code = {variable}.code',
             f'{source}.lab_observation_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(fhir2sql.name_cohort(variable), sql)

def cohort_proc(variable: str) -> Path:
    source = fhir2sql.name_study_population('proc')
    where = [f'{source}.proc_code = {variable}.code',
             f'{source}.proc_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(fhir2sql.name_cohort(variable), sql)

def cohort_doc(variable: str) -> Path:
    source = fhir2sql.name_study_population('doc')
    where = [f'{source}.doc_type_code = {variable}.code',
             f'{source}.doc_type_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(fhir2sql.name_cohort(variable), sql)

###############################################################################
# EACH Select Variable, make a cohort for each by itself.
###############################################################################
def make_each_study_variable() -> List[Path]:
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

###############################################################################
# Select Variables UNION and WIDE representation
###############################################################################
def make_study_variables_union() -> Path:
    select = fhir2sql.select_union_study_variables(list_variables())
    file = fhir2sql.name_study_variables() + '.sql'
    text = filetool.load_template(file)
    text = filetool.inline_template(sql=text, variable=select)
    return filetool.save_athena(file, text)

def make_study_variables_wide() -> Path:
    select = fhir2sql.select_lookup_study_variables(list_variables())
    file = fhir2sql.name_study_variables('wide') + '.sql'
    text = filetool.load_template(file)
    text = filetool.inline_template(sql=text, variable=select)
    return filetool.save_athena(file, text)

###############################################################################
# Comorbidity from UNION of study variables
###############################################################################
def make_comorbidity() -> Path:
    file = fhir2sql.name_study_variables('comorbidity') + '.sql'
    text = filetool.load_template(file)
    text = filetool.inline_template(text)
    return filetool.save_athena(file, text)

def make() -> List[Path]:
    variables_each = make_each_study_variable()
    variables_union_wide = [make_study_variables_union(), make_study_variables_wide()]
    variables_comorbidity = [make_comorbidity()]

    return variables_each + variables_union_wide + variables_comorbidity
