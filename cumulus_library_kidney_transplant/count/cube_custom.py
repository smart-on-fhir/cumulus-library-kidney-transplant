from typing import List
from pathlib import Path
from cumulus_library_kidney_transplant import fhir2sql
from cumulus_library_kidney_transplant.schema import Columns
from cumulus_library_kidney_transplant.count import cube

def make_dx() -> List[Path]:
    source = fhir2sql.name_cohort('study_variables_timeline')
    cols = ['enc_period_start_year',
            'variable',
            'dx_autoimmune',
            'dx_cancer',
            'dx_compromised',
            'dx_diabetes',
            'dx_heart',
            'dx_htn',
            'dx_infection',
            'dx_kidney']
    return [cube.cube_enc(source, cols, fhir2sql.name_cube(source, 'pat_dx'))]

def make_rx() -> List[Path]:
    source = fhir2sql.name_cohort('study_variables_timeline')
    cols = ['enc_period_start_year',
            'variable',
            'rx_custom',
            'rx_diabetes',
            'rx_diuretics',
            'rx_immunosuppressive']
    return [cube.cube_enc(source, cols, fhir2sql.name_cube(source, 'pat_rx'))]

def make_lab() -> List[Path]:
    source = fhir2sql.name_cohort('study_variables_timeline')
    cols = ['enc_period_start_year',
            'lab_autoimmune',
            'lab_creatinine',
            'lab_custom',
            'lab_diabetes',
            'lab_gfr',
            'lab_lft']
    return [cube.cube_enc(source, cols, fhir2sql.name_cube(source, 'pat_rx'))]

def make_variables() -> List[Path]:
    source = fhir2sql.name_cohort('study_variables')
    cols = Columns.cohort_subtype.value + ['variable']
    return [cube.cube_pat(source, cols, fhir2sql.name_cube(source, 'pat')),
            cube.cube_enc(source, cols, fhir2sql.name_cube(source, 'enc'))]

def make() -> List[Path]:
    return make_variables()
