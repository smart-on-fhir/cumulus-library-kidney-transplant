from typing import List
from pathlib import Path
from cumulus_library_kidney_transplant import filetool

def make() -> List[Path]:
    """
    TODO: replace templates with cumulus-library `BaseTableBuilder`
    https://github.com/smart-on-fhir/cumulus-library/blob/main/cumulus_library/studies/core/builder_condition.py
    base_templates.get_codeable_concept_denormalize_query
    sql_utils.CodeableConceptConfig
    """
    table_list = ['dispense', 'dosage_timing', 'dosage_quantity', 'dosage_route']
    table_list = [f'medicationrequest_dn_{t}.sql' for t in table_list]
    return [filetool.copy_template(f) for f in table_list]
