import unittest
from irae import fhir2sql

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
        actual = fhir2sql.prefix('cohort_casedef_timeline')
        self.assertEqual(expected, actual)

        expected = ['irae__cohort_casedef_timeline', 'irae__dx_diabetes']
        actual = fhir2sql.prefix(['cohort_casedef_timeline', 'dx_diabetes'])
        self.assertEqual(expected, actual)

    def test_name_join(self):
        expected = 'irae__cohort_casedef_timeline'
        actual = fhir2sql.name_join('cohort', 'casedef_timeline')
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
