from typing import List
from irae import fhir2sql, resources
from irae.variable import vsac_variables, custom_variables

STUDY_POP = 'irae__cohort_study_population'

def select_from(tables: list) -> str:
    return f'select * from \n {fhir2sql.sql_list(tables)}'

def ctas(cohort: str, variable: str, where: list) -> str:
    sql = [f'create table {name_cohort(variable)} as ',
           select_from([cohort, variable]),
           'WHERE', fhir2sql.sql_and(where)]

    return '\n'.join(sql)

def name_cohort(variable: str) -> str:
    return variable.replace('irae__', 'irae__cohort_')

def cohort_dx(variable: str) -> str:
    source = f'{STUDY_POP}_dx'
    where = [f'{source}.dx_code = {variable}.code',
             f'{source}.dx_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(name_cohort(variable), sql)

def cohort_rx(variable: str) -> str:
    source = f'{STUDY_POP}_rx'
    where = [f'{source}.rx_code = {variable}.code',
             f'{source}.rx_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(name_cohort(variable), sql)

def cohort_lab(variable: str) -> str:
    source = f'{STUDY_POP}_lab'
    where = [f'{source}.lab_observation_code = {variable}.code',
             f'{source}.lab_observation_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(name_cohort(variable), sql)

def cohort_proc(variable: str) -> str:
    source = f'{STUDY_POP}_proc'
    where = [f'{source}.proc_code = {variable}.code',
             f'{source}.proc_system = {variable}.system']
    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_view(name_cohort(variable), sql)

def make_study_variable_timeline() -> List[str]:
    file_list = list()
    table_list = ['irae__cohort_study_variables',
                  'irae__cohort_study_variables_timeline']

    for table in table_list:
        file = f'{table}.sql'
        text = resources.load_template(file)
        file_list.append(resources.save_athena(file, text))

    return file_list

def make_study_variable_groups() -> List[str]:
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

def make() -> List[str]:
    file_list = list()
    variable_list = vsac_variables.list_view_variables() + custom_variables.list_view_variables()
    for variable in variable_list:
        if '__dx' in variable:
            file_list.append(cohort_dx(variable))
        elif '__rx' in variable:
            file_list.append(cohort_rx(variable))
        elif '__lab' in variable:
            file_list.append(cohort_lab(variable))
        elif '__proc' in variable:
            file_list.append(cohort_proc(variable))
        else:
            raise Exception(f'unknown variable type {variable}')

    return file_list + make_study_variable_timeline()
