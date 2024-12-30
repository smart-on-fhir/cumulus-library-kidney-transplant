from enum import Enum
from typing import List
from irae import fhir2sql, common

VIEW = 'irae__cohort_casedef'
SOURCE = 'irae__cohort_rx_custom'

def make_view(source=SOURCE) -> str:
    sql = f"create or replace view {VIEW} as select * from {source}"
    return common.write_text(sql, fhir2sql.path_athena(f'{VIEW}.sql'))

def make_index() -> str:
    view = f'{VIEW}_index'
    file = f'{view}.sql'
    sql = common.read_text(fhir2sql.path_template(file))
    return common.write_text(sql, fhir2sql.path_athena(file))

def make(source=SOURCE) -> List[str]:
    return [make_view(source), make_index()]
