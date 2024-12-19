from irae import fhir2sql

TEMPLATE_SQL = """
create or replace view irae__study_period as select * from
(VALUES
    (date('$period_start'), date('$period_end'), $include_history)
) AS t (period_start, period_end, include_history);
"""

def include(period_start='2016-01-01', period_end='2025-01-01', include_history=True):
    _sql = TEMPLATE_SQL

    _sql = _sql.replace('$period_start', period_start)
    _sql = _sql.replace('$period_end', period_end)
    _sql = _sql.replace('$include_history', str(include_history))

    _view = f"{fhir2sql.PREFIX}__include_study_period"

    return fhir2sql.save_sql(_view, _sql)
