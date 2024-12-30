from enum import Enum
from typing import List
from irae import fhir2sql, common

VIEW = 'irae__cohort_casedef'
SOURCE = 'irae__cohort_rx_custom'

def make_view(source=SOURCE) -> str:
    sql = f"create or replace view {VIEW} as select * from {source}"
    return common.write_text(sql, fhir2sql.path_athena(f'{VIEW}.sql'))

def inline(sql: str, suffix, equality) -> str:
    return sql.replace('$prefix', fhir2sql.PREFIX).replace('$suffix', suffix).replace('$equality', equality)

def make_index_date(suffix, equality) -> str:
    view = f'{VIEW}_{suffix}.sql'
    template = f'{VIEW}_index.sql'

    sql = common.read_text(fhir2sql.path_template(template))
    sql = inline(sql, suffix, equality)

    return common.write_text(sql, fhir2sql.path_athena(view))

def make(source=SOURCE) -> List[str]:
    return [make_view(source),
            make_index_date('index', '='),
            make_index_date('pre', '<'),
            make_index_date('post', '>')]
