from typing import List
from pathlib import Path
from cumulus_library_kidney_transplant import filetool, fhir2sql

def make() -> List[Path]:
    targets = [
        'doc_ontology',
        'doc_ontology_kind',
        'doc_ontology_role',
        'doc_ontology_service',
        'doc_ontology_domain',
        'doc_ontology_include',
    ]
    for target in targets:
        sql = filetool.load_template(f"{target}.sql")
        view_name = fhir2sql.name_prefix(target)
        filetool.save_athena_view(view_name, sql)

if __name__ == "__main__":
    make()
