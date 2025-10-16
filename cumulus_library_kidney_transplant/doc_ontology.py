from typing import List
from pathlib import Path
from cumulus_library_kidney_transplant import filetool, fhir2sql

def copy_template(template) -> Path:
    sql = filetool.load_template(f"{template}.sql")
    view_name = fhir2sql.name_prefix(template)
    return filetool.save_athena_view(view_name, sql)

def make() -> List[Path]:
    templates = [
        'doc_ontology',
        'doc_ontology_kind',
        'doc_ontology_role',
        'doc_ontology_service',
        'doc_ontology_domain',
        'doc_ontology_include',
    ]
    return [copy_template(t) for t in templates]

if __name__ == "__main__":
    make()
