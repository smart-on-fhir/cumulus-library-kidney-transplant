import unittest
from cumulus_library_kidney_transplant import filetool, fhir2sql

def filter_sql(variable:str, subset:str, search_terms=None):
    if search_terms is None:
        search_terms = [subset]
    variable_json = f'{variable}/any.json'
    subset_json = f'{variable}/{subset}.json'
    filetool.save_valueset(subset_json, fhir2sql.filter_expansion(variable_json, search_terms))

def filter_sql_cancer():
    variable = 'irae__dx_cancer'

    filter_sql(variable, 'carcinoma', ['carcinoma', 'squamous', 'basal'])
    filter_sql(variable, 'squamous')
    filter_sql(variable, 'basal')
    filter_sql(variable, 'melanoma')
    filter_sql(variable, 'skin')
    filter_sql(variable, 'lymph', ['lymphoma', 'lymphoid'])
    filter_sql(variable, 'leukemia')
    filter_sql(variable, 'kidney',  ['kidney', 'renal', 'nephr'])
    filter_sql(variable, 'malignant')
    filter_sql(variable, 'neoplasm')

class TestValuesetFilter(unittest.TestCase):

    def ignore_test(self):
        filter_sql_cancer()
