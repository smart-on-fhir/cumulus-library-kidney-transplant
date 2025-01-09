from pathlib import Path
from typing import List
from irae import fhir2sql, filetool

def make(variable=None) -> List[Path]:
    if not variable:
        variable = fhir2sql.name_join('cohort', 'rx_transplant')

    return [make_index_date(variable, 'index', '='),
            make_index_date(variable, 'pre', '<'),
            make_index_date(variable, 'post', '>'),
            make_timeline()]

def get_view() -> str:
    return fhir2sql.name_join('cohort', 'casedef')

def make_index_date(variable, suffix, equality) -> Path:
    view = f'{get_view()}_{suffix}.sql'
    template = f'{get_view()}_index.sql'

    sql = filetool.load_template(template)
    sql = filetool.inline_template(sql, suffix, variable, equality)

    return filetool.save_athena(view, sql)

def make_timeline() -> Path:
    template = fhir2sql.name_join('cohort', 'casedef_timeline') + '.sql'
    sql = filetool.load_template(template)
    sql = filetool.inline_template(sql)
    return filetool.save_athena(template, sql)
