from typing import List
from pathlib import Path
from cumulus_library_kidney_transplant import fhir2sql
from cumulus_library_kidney_transplant.schema import Columns
from cumulus_library_kidney_transplant.count import cube

def make_comorbidity_kidney() -> List[Path]:
    source = fhir2sql.name_cohort('study_variables_wide')
    cols = Columns.cohort.value
    cols += ['dx_kidney',
             'dx_heart',
             'dx_compromised',
             'dx_infection',
             'dx_htn']
    return [cube.cube_pat(source, cols, fhir2sql.name_cube('comorbidity_kidney'))]

def make_comorbidity_diabetes() -> List[Path]:
    source = fhir2sql.name_cohort('study_variables_wide')
    cols = Columns.cohort.value
    cols += ['dx_diabetes',
             'dx_heart',
             'dx_htn',
             'dx_kidney']
    return [cube.cube_pat(source, cols, fhir2sql.name_cube('comorbidity_diabetes'))]

def make_comorbidity_autoimmune() -> List[Path]:
    source = fhir2sql.name_cohort('study_variables_wide')
    cols = Columns.cohort.value
    cols += ['dx_autoimmune',
             'dx_compromised',
             'dx_infection',
             'dx_cancer',
             'dx_kidney']
    return [cube.cube_pat(source, cols, fhir2sql.name_cube('comorbidity_autoimmune'))]

def make_comorbidity() -> List[Path]:
    return make_comorbidity_kidney() + make_comorbidity_autoimmune() + make_comorbidity_diabetes()

def make_variables() -> List[Path]:
    source = fhir2sql.name_cohort('study_variables')
    cols = Columns.valueset.value + ['variable']
    return [cube.cube_pat(source, cols, fhir2sql.name_cube(source, 'pat')),
            cube.cube_enc(source, cols, fhir2sql.name_cube(source, 'enc'))]

def make() -> List[Path]:
    return make_variables() + make_comorbidity()
