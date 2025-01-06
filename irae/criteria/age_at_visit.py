from irae import fhir2sql

def include(min_age=0, max_age=120) -> str:
    view = f'{fhir2sql.PREFIX}__include_age_at_visit'
    cols = ['age_min', 'age_max']
    values = [str(min_age), str(max_age)]
    return fhir2sql.values2view(view, cols, values)
