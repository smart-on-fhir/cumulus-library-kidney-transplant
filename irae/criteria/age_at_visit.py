from irae import fhir2sql

def include(age_min=0, age_max=120) -> str:
    """
    :param age_min: min patient `age_at_visit` during `study_period`
    :param age_max: max patient `age_at_visit` during `study_period`
    :return: inclusion criteria for `study_population`
    """
    view = fhir2sql.name_join('include', 'age_at_visit')
    cols = ['age_min', 'age_max']
    values = [age_min, age_max]
    return fhir2sql.criteria2view(view, cols, values)
