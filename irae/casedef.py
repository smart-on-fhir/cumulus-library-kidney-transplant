from enum import Enum
from typing import List
from irae import fhir2sql, common

VIEW = 'irae__cohort_casedef'
VARIABLE = 'irae__cohort_rx_transplant'

def make_union_view() -> str:
    view = f'{VIEW}_timeline.sql'
    sql = common.read_text(fhir2sql.path_template(view))
    return common.write_text(sql, fhir2sql.path_athena(view))

def inline(variable: str, sql: str, suffix, equality) -> str:
    return sql.replace('$variable', variable).replace('$suffix', suffix).replace('$equality', equality)

def make_index_date(variable, suffix, equality) -> str:
    view = f'{VIEW}_{suffix}.sql'
    template = f'{VIEW}_index.sql'

    sql = common.read_text(fhir2sql.path_template(template))
    sql = inline(variable, sql, suffix, equality)

    return common.write_text(sql, fhir2sql.path_athena(view))

def make(variable=VARIABLE) -> List[str]:
    return [make_index_date(variable, 'index', '='),
            make_index_date(variable, 'pre', '<'),
            make_index_date(variable, 'post', '>'),
            make_union_view()]
