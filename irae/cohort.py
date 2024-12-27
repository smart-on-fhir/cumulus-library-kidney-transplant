from typing import List
from irae import fhir2sql, common
from irae.variable import vsac_variables, custom_variables

STUDY_POP = 'irae__cohort_study_population'

def select_from(tables: list) -> str:
    return f'select * from \n {sql_list(tables)}'

def sql_iter(clauses_list, operator=',') -> str:
    if not isinstance(clauses_list, list):
        return sql_iter([clauses_list])
    return f' {operator} \n'.join(clauses_list)

def sql_and(clauses_list) -> str:
    return sql_iter(clauses_list, 'and')

def sql_or(clauses_list) -> str:
    return sql_iter(clauses_list, 'or')

def sql_list(clauses_list) -> str:
    return sql_iter(clauses_list, ',')

def sql_paren(statement: str) -> str:
    return f'({statement})'

def ctas(cohort: str, variable: str, where: list) -> str:
    sql = [f'create table {name_cohort(variable)} as ',
           select_from([cohort, variable]),
           'WHERE', sql_and(where)]

    return '\n'.join(sql)

def name_cohort(variable: str) -> str:
    return variable.replace('irae__', 'irae__cohort_')

def cohort_dx(variable: str) -> str:
    source = f'{STUDY_POP}_dx'
    where = [f'{source}.dx_code = {variable}.code',
             f'{source}.dx_system = {variable}.system']

    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_sql(name_cohort(variable), sql)

def cohort_rx(variable: str) -> str:
    source = f'{STUDY_POP}_rx'
    where = [f'{source}.rx_code = {variable}.code',
             f'{source}.rx_system = {variable}.system']

    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_sql(name_cohort(variable), sql)

def cohort_lab(variable: str) -> str:
    source = f'{STUDY_POP}_lab'
    where = [f'{source}.lab_observation_code = {variable}.code',
             f'{source}.lab_observation_system = {variable}.system']
    # where2 = [f'{source}.lab_concept_code = {variable}.code',
    #           f'{source}.lab_concept_system = {variable}.system']
    # where = sql_or([sql_paren(sql_and(where1)),
    #                sql_paren(sql_and(where2))])

    sql = ctas(source, variable, where)
    return fhir2sql.save_athena_sql(name_cohort(variable), sql)

def make() -> List[str]:
    file_list = list()
    variable_list = vsac_variables.list_variable_views() + custom_variables.list_variables()
    for variable in variable_list:
        if '__dx' in variable:
            file_list.append(cohort_dx(variable))
        elif '__rx' in variable:
            file_list.append(cohort_rx(variable))
        elif '__lab' in variable:
            file_list.append(cohort_lab(variable))
    return file_list
