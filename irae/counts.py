from typing import List
from cumulus_library.builders.counts import CountsBuilder
from irae.fhir2sql import PREFIX, save_athena_sql
from irae.variable import vsac_variables, custom_variables

PAT = ['gender', 'race_display', 'ethnicity_display']
ENC = ['gender', 'age_at_visit', 'enc_class_code']
SUBTYPE = ['subtype']
DX = ['dx_category_code'] + ENC
RX = ['rx_category_code'] + ENC
LAB = ['lab_observation_code'] + ENC
MONTH = ['enc_period_start_month']
YEAR = ['enc_period_start_year']


def name_cohort(table: str) -> str:
    return f'{PREFIX}__cohort_{name_simple(table)}'

def name_cube(table: str, suffix=None) -> str:
    if suffix:
        table = f'{table}_{suffix}'
    return f'{PREFIX}__cube_{name_simple(table)}'

def name_simple(table):
    if 'irae__cohort_' in table:
        _, simple = table.split('irae__cohort_')
        return simple

    if 'irae__' in table:
        _, simple = table.split('irae__')
        return simple
    return table

def cube_enc(source='study_population', cols=None, cube_table=None) -> str:
    from_table = name_cohort(source)

    if not cube_table:
        cube_table = name_cube(source, 'enc')

    if not cols:
        cols = PAT + ENC + MONTH

    sql = CountsBuilder(PREFIX).count_encounter(cube_table, from_table, cols)
    return save_athena_sql(cube_table, sql)

def cube_pat(source='study_population', cols=None, cube_table=None) -> str:
    from_table = name_cohort(source)

    if not cube_table:
        cube_table = name_cube(source, 'pat')

    if not cols:
        cols = PAT

    sql = CountsBuilder(PREFIX).count_patient(cube_table, from_table, cols)
    return save_athena_sql(cube_table, sql)

def make_study_population() -> List[str]:
    return [cube_pat(),
            cube_enc(),
            cube_enc('study_population_dx', DX),
            cube_enc('study_population_rx', RX),
            cube_enc('study_population_lab', LAB)]

def make_variables() -> List[str]:
    file_list = list()
    variable_list = vsac_variables.list_view_variables() + custom_variables.list_view_variables()
    for variable in variable_list:
        if '__dx' in variable:
            file_list.append(cube_enc(variable, SUBTYPE+DX))
        elif '__rx' in variable:
            file_list.append(cube_enc(variable, SUBTYPE+RX))
        elif '__lab' in variable:
            file_list.append(cube_enc(variable, SUBTYPE+LAB))
    return file_list

def make_variables_timeline_dx() -> List[str]:
    source = 'irae__cohort_study_variables_timeline'
    cols = ['variable',
            'dx_autoimmune',
            'dx_cancer',
            'dx_compromised',
            'dx_diabetes',
            'dx_heart',
            'dx_htn',
            'dx_infection',
            'dx_kidney']
    return [cube_pat(source, cols, name_cube(source, 'dx_pat'))]

def make_variables_timeline_rx() -> List[str]:
    source = 'irae__cohort_study_variables_timeline'
    cols = ['variable',
            'rx_custom',
            'rx_diabetes',
            'rx_diuretics',
            'rx_immunosuppressive']
    return [cube_enc(source, cols, name_cube(source, 'rx_pat'))]

def make_timeline() -> List[str]:
    return make_variables_timeline_dx() + make_variables_timeline_rx()

def make():
    return make_study_population() + make_variables() + make_timeline()
