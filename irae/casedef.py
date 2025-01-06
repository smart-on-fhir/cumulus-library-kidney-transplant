from enum import Enum
from typing import List
from irae import fhir2sql, resources

VIEW = 'irae__cohort_casedef'
VARIABLE = 'irae__cohort_rx_transplant'

def make_union_view() -> str:   # TDOO Refactor
    """
    :return:
    """
    template = f'{VIEW}_timeline.sql'
    sql = resources.load_template(template)
    return resources.save_athena(template, sql)

def inline(variable: str, sql: str, suffix, equality) -> str:
    return sql.replace('$variable', variable).replace('$suffix', suffix).replace('$equality', equality)

def make_index_date(variable, suffix, equality) -> str:
    view = f'{VIEW}_{suffix}.sql'
    template = f'{VIEW}_index.sql'

    sql = resources.load_template(template)
    sql = inline(variable, sql, suffix, equality)

    return resources.save_athena(view, sql)

def make(variable=VARIABLE) -> List[str]:
    return [make_index_date(variable, 'index', '='),
            make_index_date(variable, 'pre', '<'),
            make_index_date(variable, 'post', '>'),
            make_union_view()]
