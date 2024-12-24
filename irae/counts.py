from typing import List
from cumulus_library.builders.counts import CountsBuilder
from irae.fhir2sql import PREFIX, save_athena_sql
from irae.variable import vsac_variables, custom_variables

PAT = ['gender', 'race_display', 'ethnicity_display']
ENC = ['age_at_visit', 'enc_class_code']
MONTH = ['enc_period_start_month']
YEAR = ['enc_period_start_year']

def name_cohort(table: str) -> str:
    return f'{PREFIX}__cohort_{name_simple(table)}'

def name_cube(table: str) -> str:
    return f'{PREFIX}__cube_{name_simple(table)}'

def name_simple(table):
    if 'irae__' in table:
        _, simple = table.split('irae__')
        return simple
    return table

def cube_dx(source='study_population_dx', cols=None) -> str:
    if not cols:
        cols = ['dx_category_code', 'dx_code'] + PAT + ENC
    return cube(source, cols)

def cube_rx(source='study_population_rx', cols=None) -> str:
    if not cols:
        cols = ['rx_category_code', 'rx_code'] + PAT + ENC
    return cube(source, cols)

def cube_lab(source='study_population_lab', cols=None) -> str:
    if not cols:
        cols = ['lab_observation_code'] + ENC
    return cube(source, cols)

def cube(source='study_population', cols=None) -> str:
    cube_table = name_cube(source)
    from_table = name_cohort(source)
    if not cols:
        cols = PAT + ENC + MONTH
    sql = CountsBuilder(PREFIX).count_encounter(cube_table, from_table, cols)
    return save_athena_sql(cube_table, sql)

def make_study_population() -> List[str]:
    return [cube(),
            cube_dx(),
            cube_rx()]

def make_variable_cohorts() -> List[str]:
    file_list = list()
    variable_list = vsac_variables.list_variable_views() + custom_variables.list_variables()
    for variable in variable_list:
        if '__dx' in variable:
            file_list.append(cube_dx(variable))
        elif '__rx' in variable:
            file_list.append(cube_rx(variable))
        # elif '__lab' in variable:
        #     file_list.append(cube_lab(variable))
    return file_list

def make():
    return make_study_population() + make_variable_cohorts()
