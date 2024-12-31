from irae import fhir2sql, common

def include(enc_min=0, enc_max=1000, days_min=0, days_max=36500) -> str:
    view = 'irae__include_utilization'
    cols = ['enc_min', 'enc_max', 'days_min', 'days_max']
    values = [str(enc_min), str(enc_max), str(days_min), str(days_max)]
    return fhir2sql.values2view(view, cols, values)
