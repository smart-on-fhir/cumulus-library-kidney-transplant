import unittest
import csv
from typing import List
from pathlib import Path
from cumulus_library_kidney_transplant import guard, fhir2sql, filetool

class TestFHIR2sql(unittest.TestCase):

    def test_name_simple(self):
        expected = 'casedef_timeline'
        actual = fhir2sql.name_simple('irae__cohort_casedef_timeline')
        self.assertEqual(expected, actual)

        expected = 'dx_diabetes'
        actual = fhir2sql.name_simple('irae__dx_diabetes')
        self.assertEqual(expected, actual)

    def test_prefix(self):
        expected = 'irae__cohort_casedef_timeline'
        actual = fhir2sql.name_prefix('cohort_casedef_timeline')
        self.assertEqual(expected, actual)

        expected = ['irae__cohort_casedef_timeline', 'irae__dx_diabetes']
        actual = fhir2sql.name_prefix(['cohort_casedef_timeline', 'dx_diabetes'])
        self.assertSetEqual(set(expected), set(actual))

    def test_name_join(self):
        expected = 'irae__cohort_casedef_timeline'
        actual = fhir2sql.name_join('cohort', 'casedef_timeline')
        self.assertEqual(expected, actual)

    def test_headers(self):
        header_list = ['system','code','display',
                       'likely','preop','transplant',
                       'rejection','failure','outcome',
                       'lab','imaging','count_sum']

        file_csv = filetool.path_spreadsheet('casedef_custom.csv')
        actual = csv_headers(file_csv)
        self.assertEqual(header_list, actual)

    def ignore_test_criteria2view(self):
        file_csv = filetool.path_spreadsheet('casedef_custom.csv')
        view_name = fhir2sql.name_prefix('casedef_custom_csv')
        view_file = filetool.path_athena(f'{view_name}.sql')

        _sql = csv2sql(file_csv, view_name)
        filetool.write_text(_sql, view_file)

