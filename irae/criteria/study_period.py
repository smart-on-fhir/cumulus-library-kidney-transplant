from irae import fhir2sql

def include(period_start='2016-01-01', period_end='2025-01-01', include_history=True):
    view = 'irae__include_study_period'
    cols = ['period_start', 'period_end', 'include_history']
    values = [
        f"date('{period_start}')",
        f"date('{period_end}')",
        str(include_history)]

    return fhir2sql.values2view(view, cols, values)