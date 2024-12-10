import os
from kidney_transplant import common, fhir2sql

def filepath(filename: str) -> str:
    pwd = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(pwd, filename)

def include(period_start='2016-01-01', period_end='2025-01-01', include_history=True):
    _sql = common.read_text(filepath(__file__.replace('.py', '.sql')))

    _sql = _sql.replace('$period_start', period_start)
    _sql = _sql.replace('$period_end', period_end)
    _sql = _sql.replace('$include_history', str(include_history))

    _view = f"{fhir2sql.PREFIX}__include_study_period"

    return fhir2sql.save_sql(_view, _sql)
