from typing import List
from pathlib import Path
from cumulus_library.builders.counts import CountsBuilder
from irae import resources, fhir2sql
from irae.variable import vsac_variables, custom_variables

PAT = ['gender', 'race_display', 'ethnicity_display']
ENC = ['gender', 'age_at_visit', 'enc_class_code']
SUBTYPE = ['subtype']
DX = ['dx_category_code'] + ENC
RX = ['rx_category_code'] + ENC
LAB = ['lab_observation_code'] + ENC
MONTH = ['enc_period_start_month']
YEAR = ['enc_period_start_year']

def cube_enc(source='study_population', cols=None, cube_table=None) -> Path:
    from_table = fhir2sql.name_cohort(source)

    if not cube_table:
        cube_table = fhir2sql.name_cube(source, 'enc')

    if not cols:
        cols = PAT + ENC + MONTH

    sql = CountsBuilder(fhir2sql.PREFIX).count_encounter(cube_table, from_table, cols)
    return resources.save_athena_view(cube_table, sql)

def cube_pat(source='study_population', cols=None, cube_table=None) -> Path:
    from_table = fhir2sql.name_cohort(source)

    if not cube_table:
        cube_table = fhir2sql.name_cube(source, 'pat')

    if not cols:
        cols = PAT

    sql = CountsBuilder(fhir2sql.PREFIX).count_patient(cube_table, from_table, cols)
    return resources.save_athena_view(cube_table, sql)

def make_study_population() -> List[Path]:
    return [cube_pat(),
            cube_enc(),
            cube_enc('study_population_dx', DX),
            cube_enc('study_population_rx', RX),
            cube_enc('study_population_lab', LAB)]

def make_variables() -> List[Path]:
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

def make_variables_timeline_dx() -> List[Path]:
    source = fhir2sql.name_studypop('timeline')
    cols = ['variable',
            'dx_autoimmune',
            'dx_cancer',
            'dx_compromised',
            'dx_diabetes',
            'dx_heart',
            'dx_htn',
            'dx_infection',
            'dx_kidney']
    return [cube_pat(source, cols, fhir2sql.name_cube(source, 'pat_dx'))]

def make_variables_timeline_rx() -> List[Path]:
    source = fhir2sql.name_studypop('timeline')
    cols = ['variable',
            'rx_transplant',
            'rx_diabetes',
            'rx_diuretics',
            'rx_immunosuppressive']
    return [cube_enc(source, cols, fhir2sql.name_cube(source, 'pat_rx'))]

def make_timeline() -> List[Path]:
    return make_variables_timeline_dx() + make_variables_timeline_rx()

def make() -> List[Path]:
    return make_study_population() + make_variables() + make_timeline()
