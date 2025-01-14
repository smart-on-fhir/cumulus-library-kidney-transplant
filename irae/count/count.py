from typing import List
from pathlib import Path
from cumulus_library.builders.counts import CountsBuilder
from irae import filetool, fhir2sql
from irae.study_prefix import PREFIX
from irae.variable import vsac_variables, custom_variables
from irae.schema import Columns

def cube_enc(from_table='study_population', cols=None, cube_table=None) -> Path:
    from_table = fhir2sql.name_cohort(from_table)

    if not cube_table:
        cube_table = fhir2sql.name_cube(from_table, 'enc')

    if not cols:
        cols = Columns.cohort.value

    sql = CountsBuilder(PREFIX).count_encounter(cube_table, from_table, cols)
    return filetool.save_athena_view(cube_table, sql)

def cube_pat(source='study_population', cols=None, cube_table=None) -> Path:
    from_table = fhir2sql.name_cohort(source)

    if not cube_table:
        cube_table = fhir2sql.name_cube(source, 'pat')

    if not cols:
        cols = Columns.demographics.value

    sql = CountsBuilder(PREFIX).count_patient(cube_table, from_table, cols)
    return filetool.save_athena_view(cube_table, sql)

def make_study_population() -> List[Path]:
    return [cube_pat(),
            cube_enc(),
            cube_enc('study_population_dx', Columns.diagnoses.value),
            cube_enc('study_population_rx', Columns.medications.value),
            cube_enc('study_population_lab', Columns.labs.value),
            cube_enc('study_population_doc', Columns.documents.value),
            cube_enc('study_population_proc', Columns.procedures.value)]

def make_variables() -> List[Path]:
    file_list = list()
    variable_list = vsac_variables.list_view_variables() + custom_variables.list_view_variables()
    for variable in variable_list:
        if '__dx' in variable:
            file_list.append(cube_enc(variable, Columns.subtype.value + Columns.diagnoses.value))
        elif '__rx' in variable:
            file_list.append(cube_enc(variable, Columns.subtype.value + Columns.medications.value))
        elif '__lab' in variable:
            file_list.append(cube_enc(variable, Columns.subtype.value + Columns.labs.value))
    return file_list

def make_variables_timeline_dx() -> List[Path]:
    source = fhir2sql.name_cohort('study_variables_timeline')
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
    source = fhir2sql.name_cohort('study_variables_timeline')
    cols = ['variable',
            'rx_custom',
            'rx_diabetes',
            'rx_diuretics',
            'rx_immunosuppressive']
    return [cube_enc(source, cols, fhir2sql.name_cube(source, 'pat_rx'))]

def make_timeline() -> List[Path]:
    return make_variables_timeline_dx() + make_variables_timeline_rx()

def make() -> List[Path]:
    return make_study_population() + make_variables() + make_timeline()
