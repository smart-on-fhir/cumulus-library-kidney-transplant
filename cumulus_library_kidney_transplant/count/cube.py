from typing import List
from pathlib import Path
from cumulus_library.builders.counts import CountsBuilder
from cumulus_library_kidney_transplant import filetool, fhir2sql
from cumulus_library_kidney_transplant.study_prefix import PREFIX
from cumulus_library_kidney_transplant.variable import vsac_variables, custom_variables
from cumulus_library_kidney_transplant.schema import Columns

def cube_enc(from_table='study_population', cols=None, cube_table=None) -> Path:
    from_table = fhir2sql.name_cohort(from_table)

    if not cube_table:
        cube_table = fhir2sql.name_cube(from_table, 'enc')

    if not cols:
        cols = list(set(Columns.cohort.value + Columns.demographics.value))

    sql = CountsBuilder(PREFIX).count_encounter(cube_table, from_table, cols)
    return filetool.save_athena_view(cube_table, sql)

def cube_pat(source='study_population', cols=None, cube_table=None) -> Path:
    from_table = fhir2sql.name_cohort(source)

    if not cube_table:
        cube_table = fhir2sql.name_cube(source, 'pat')

    if not cols:
        cols = list(set(Columns.cohort.value + Columns.demographics.value))

    sql = CountsBuilder(PREFIX).count_patient(cube_table, from_table, cols)
    return filetool.save_athena_view(cube_table, sql)

def make_study_population() -> List[Path]:
    return [cube_pat(),
            cube_enc(),
            cube_pat('study_population_dx', Columns.cohort.value + Columns.diagnoses.value),
            cube_pat('study_population_rx', Columns.cohort.value + Columns.medications.value),
            cube_pat('study_population_lab', Columns.cohort.value + Columns.labs.value),
            cube_pat('study_population_doc', Columns.cohort.value + Columns.documents.value),
            cube_pat('study_population_proc', Columns.cohort.value + Columns.procedures.value)]

def make_variables() -> List[Path]:
    file_list = list()
    variable_list = vsac_variables.list_view_variables() + custom_variables.list_view_variables()
    for variable in variable_list:
        if '__dx' in variable:
            file_list.append(cube_enc(variable, Columns.cohort_valueset.value + Columns.diagnoses.value))
        elif '__rx' in variable:
            file_list.append(cube_enc(variable, Columns.cohort_valueset.value + Columns.medications.value))
        elif '__lab' in variable:
            file_list.append(cube_enc(variable, Columns.cohort_valueset.value + Columns.labs.value))
        elif '__proc' in variable:
            file_list.append(cube_enc(variable, Columns.cohort_valueset.value + Columns.procedures.value))
        elif '__doc' in variable:
            file_list.append(cube_enc(variable, Columns.cohort_valueset.value + Columns.documents.value))
    return file_list

def make() -> List[Path]:
    return make_study_population() + make_variables()
