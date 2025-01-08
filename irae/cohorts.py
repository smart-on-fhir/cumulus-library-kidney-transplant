from typing import List
from pathlib import Path
from irae.variable import vsac_variables, custom_variables
from irae import fhir2sql, resources

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

def make_study_variable_timeline() -> List[Path]:
    file_list = list()
    table_list = [fhir2sql.name_study_variables(),
                  fhir2sql.name_study_variables('timeline')]

    for table in table_list:
        file = f'{table}.sql'
        text = resources.load_template(file)
        text = resources.inline_template(text)
        file_list.append(resources.save_athena(file, text))

    return file_list

def make_study_variable_groups() -> List[Path]:
    group_list = list()
    variable_list = vsac_variables.list_view_variables() + custom_variables.list_view_variables()
    for variable in variable_list:
        if '__dx' in variable:
            group_list.append(cohort_dx(variable))
        elif '__rx' in variable:
            group_list.append(cohort_rx(variable))
        elif '__lab' in variable:
            group_list.append(cohort_lab(variable))
        elif '__proc' in variable:
            group_list.append(cohort_proc(variable))
        else:
            raise Exception(f'unknown variable type {variable}')
    return group_list + make_study_variable_timeline()

def make() -> List[Path]:
    file_list = list()
    variable_list = vsac_variables.list_view_variables() + custom_variables.list_view_variables()

    for variable in variable_list:
        if 'dx_' in variable:
            file_list.append(cohort_dx(variable))
        elif 'rx_' in variable:
            file_list.append(cohort_rx(variable))
        elif 'lab_' in variable:
            file_list.append(cohort_lab(variable))
        elif 'proc_' in variable:
            file_list.append(cohort_proc(variable))
        else:
            raise Exception(f'unknown variable type {variable}')

    return file_list + make_study_variable_timeline()
