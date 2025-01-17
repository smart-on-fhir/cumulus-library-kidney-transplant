import unittest
from cumulus_library_kidney_transplant import filetool, fhir2sql

class TestValuesetFilter(unittest.TestCase):

    def test(self):
        valueset_json = 'irae__dx_cancer/any.json'
        filetool.save_valueset('irae__dx_cancer/skin.json', fhir2sql.filter_expansion(valueset_json, ['skin']))
        filetool.save_valueset('irae__dx_cancer/melanoma.json', fhir2sql.filter_expansion(valueset_json, ['melanoma']))
        filetool.save_valueset('irae__dx_cancer/sarcoma.json', fhir2sql.filter_expansion(valueset_json, ['sarcoma']))
        filetool.save_valueset('irae__dx_cancer/squamous.json', fhir2sql.filter_expansion(valueset_json, ['squamous']))
