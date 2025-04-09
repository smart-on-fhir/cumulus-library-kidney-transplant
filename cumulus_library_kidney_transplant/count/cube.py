from typing import List
from pathlib import Path
from cumulus_library.builders.counts import CountsBuilder
from cumulus_library_kidney_transplant import filetool, fhir2sql
from cumulus_library_kidney_transplant.study_prefix import PREFIX
from cumulus_library_kidney_transplant.variable import vsac_variables, custom_variables
from cumulus_library_kidney_transplant.count.columns import Columns, Duration

def cube_enc(from_table='study_population', cols=None, cube_table=None) -> Path:
    from_table = fhir2sql.name_cohort(from_table)

    if not cube_table:
        cube_table = fhir2sql.name_cube(from_table, 'encounter')

    if not cols:
        cols = Columns.cohort.value + Columns.demographics.value

    cols = sorted(list(set(cols)))
    sql = CountsBuilder(PREFIX).count_encounter(cube_table, from_table, cols)
    return filetool.save_athena_view(cube_table, sql)

def cube_pat(from_table='study_population', cols=None, cube_table=None) -> Path:
    from_table = fhir2sql.name_cohort(from_table)

    if not cube_table:
        cube_table = fhir2sql.name_cube(from_table, 'patient')

    if not cols:
        cols = Columns.cohort.value + Columns.demographics.value

    cols = sorted(list(set(cols)))
    sql = CountsBuilder(PREFIX).count_patient(cube_table, from_table, cols)
    return filetool.save_athena_view(cube_table, sql)

def cube_doc(from_table='study_population', cols=None, cube_table=None) -> Path:
    from_table = fhir2sql.name_cohort(from_table)

    if not cube_table:
        cube_table = fhir2sql.name_cube(from_table, 'document')

    if not cols:
        cols = Columns.cohort.value + Columns.demographics.value

    cols = sorted(list(set(cols)))
    sql = CountsBuilder(PREFIX).count_documentreference(cube_table, from_table, cols)
    return filetool.save_athena_view(cube_table, sql)


def make_study_population_duration(duration: Duration | str) -> Path:
    """
    :param duration: week, month, or year
    :return: path to SQL counts file
    """
    if isinstance(duration, Duration):
        duration = duration.value

    return cube_enc(from_table='study_population',
                    cols=(Columns.cohort.value + Columns.month.value),
                    cube_table=fhir2sql.name_cube(f'encounter_study_population_{duration}'))


def make_study_population() -> List[Path]:
    return [
            cube_pat(),
            cube_enc(),
            cube_pat('study_population_dx', Columns.cohort.value + Columns.diagnoses.value),
            cube_enc('study_population_dx', Columns.cohort.value + Columns.diagnoses.value),
            cube_pat('study_population_rx', Columns.cohort.value + Columns.medications.value),
            cube_enc('study_population_rx', Columns.cohort.value + Columns.medications.value),
            cube_pat('study_population_lab', Columns.cohort.value + Columns.labs.value),
            cube_enc('study_population_lab', Columns.cohort.value + Columns.labs.value),
            cube_pat('study_population_doc', Columns.cohort.value + Columns.documents.value),
            cube_enc('study_population_doc', Columns.cohort.value + Columns.documents.value),
            cube_pat('study_population_proc', Columns.cohort.value + Columns.procedures.value),
            cube_enc('study_population_proc', Columns.cohort.value + Columns.procedures.value)]

def make_variables() -> List[Path]:
    file_list = list()
    variable_list = vsac_variables.list_view_variables() + custom_variables.list_view_variables()
    for variable in variable_list:
        if '__dx' in variable:
            file_list.append(cube_pat(variable, Columns.valueset.value + Columns.diagnoses.value))
        elif '__rx' in variable:
            file_list.append(cube_pat(variable, Columns.valueset.value + Columns.medications.value))
        elif '__lab' in variable:
            file_list.append(cube_pat(variable, Columns.valueset.value + Columns.labs.value))
        elif '__proc' in variable:
            file_list.append(cube_pat(variable, Columns.valueset.value + Columns.procedures.value))
        elif '__doc' in variable:
            file_list.append(cube_pat(variable, Columns.valueset.value + Columns.documents.value))
    return file_list

def make_casedef_timeline() -> List[Path]:
    from_table = fhir2sql.name_cohort('casedef_timeline')
    cols = ['soe', 'variable', 'valueset', 'enc_period_start_month']
    return [cube_pat(from_table, cols),
            cube_enc(from_table, cols)]

def make() -> List[Path]:
    return make_study_population() + make_variables() + make_casedef_timeline()
