from typing import List
from pathlib import Path
from cumulus_library_kidney_transplant import fhir2sql
from cumulus_library_kidney_transplant.count.columns import Columns
from cumulus_library_kidney_transplant.count import cube

def make_pair() -> List[Path]:
    # return make_comorbidity_kidney() + make_comorbidity_autoimmune() + make_comorbidity_diabetes()
    source = fhir2sql.name_study_variables('pair')
    by_variable = fhir2sql.name_cube('pair_variable', 'pat')
    by_valueset = fhir2sql.name_cube('pair_valueset', 'pat')
    by_variable_cols = ['variable1', 'variable2', 'age_at_visit1', 'enc_class_code1']
    by_valueset_cols = ['valueset1', 'valueset2', 'age_at_visit1', 'enc_class_code1']
    return [cube.cube_pat(source, by_variable_cols, fhir2sql.name_cube(by_variable)),
            cube.cube_pat(source, by_valueset_cols, fhir2sql.name_cube(by_valueset))]

def make_variables() -> List[Path]:
    source = fhir2sql.name_cohort('study_variables')
    cols = Columns.valueset.value + ['variable']
    return [cube.cube_pat(source, cols),
            cube.cube_enc(source, cols)]

def make() -> List[Path]:
    return make_variables()
