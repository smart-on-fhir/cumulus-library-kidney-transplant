from irae import fhir2sql

def include(min_age='2016-01-01', max_age='2025-01-01') -> str:
    view = 'irae__include_age_at_visit'
    cols = ['age_min', 'age_max']
    values = [str(min_age), str(max_age)]

    return fhir2sql.values2view(view, cols, values)
