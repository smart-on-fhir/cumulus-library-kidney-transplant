from pathlib import Path
from typing import List
from cumulus_library_kidney_transplant import fhir2sql, filetool

def get_view() -> str:
    return fhir2sql.name_join('cohort', 'casedef')

def make_index_date(variable, suffix, equality) -> Path:
    view = f'{get_view()}_{suffix}.sql'
    template = f'{get_view()}_index.sql'
    sql = filetool.load_template(template)
    sql = filetool.inline_template(sql, variable)
    sql = sql.replace('$suffix', suffix)
    sql = sql.replace('$equality', equality)
    return filetool.save_athena(view, sql)

def make_timeline() -> Path:
    template = fhir2sql.name_join('cohort', 'casedef_timeline') + '.sql'
    sql = filetool.load_template(template)
    sql = filetool.inline_template(sql)
    return filetool.save_athena(template, sql)

def make_samples(size: int = None, suffix: str = 'post') -> Path:
    table = fhir2sql.name_join('sample', 'casedef')
    if size:
        template = f"{table}_size.sql"
        target = f"{table}_{suffix}_{size}.sql"
    else:
        template = f"{table}.sql"
        target = f"{table}_{suffix}.sql"

    sql = filetool.load_template(template)
    sql = filetool.inline_template(sql)
    sql = sql.replace('$size', str(size))
    sql = sql.replace('$suffix', suffix)
    return filetool.save_athena(target, sql)


def make(variable=None) -> List[Path]:
    if not variable:
        variable = fhir2sql.name_join('cohort', 'rx_custom')

    return [make_index_date(variable, 'index', '='),
            make_index_date(variable, 'pre', '<'),
            make_index_date(variable, 'post', '>'),
            make_samples(None, 'pre'),
            make_samples(100, 'pre'),
            make_samples(1000, 'pre'),
            make_samples(None, 'post'),
            make_samples(100, 'post'),
            make_samples(1000, 'post'),
            make_timeline()]
