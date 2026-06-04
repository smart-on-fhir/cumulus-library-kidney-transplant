import unittest
from cumulus_library_kidney_transplant.tools import guard
from cumulus_library_kidney_transplant.tools.fhir_reference import Aspect

class TestGuard(unittest.TestCase):

    def test_list_type(self):
        self.assertTrue(guard.is_list_type([Aspect.lab], Aspect))
        self.assertTrue(guard.is_list_type(list(Aspect), Aspect))

