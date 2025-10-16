import unittest
from cumulus_library_kidney_transplant.variable import custom_variables

class TestSpreadsheet(unittest.TestCase):
    def test_list_variables(self):
        self.assertTrue('lab_hla' in custom_variables.list_variables_lab())
        self.assertTrue('rx_prednisone' in custom_variables.list_variables_rx())

s