import unittest
from cumulus_library_kidney_transplant.tools import tablespace, filetool

class TestTablespace(unittest.TestCase):

    def test_name_trim(self):
        expected = 'casedef_timeline'
        actual = tablespace.name_trim('irae__cohort_casedef_timeline')
        self.assertEqual(expected, actual)

        expected = 'rx_azathioprine'
        actual = tablespace.name_trim('irae__valueset_rx_azathioprine')
        self.assertEqual(expected, actual)

    def test_prefix(self):
        expected = 'irae__cohort_casedef_timeline'
        actual = tablespace.name_prefix('cohort_casedef_timeline')
        self.assertEqual(expected, actual)

        expected = ['irae__cohort_casedef_timeline', 'irae__dx_diabetes']
        actual = tablespace.name_prefix(['cohort_casedef_timeline', 'dx_diabetes'])
        self.assertSetEqual(set(expected), set(actual))

    def test_name_join(self):
        expected = 'irae__cohort_casedef_timeline'
        actual = tablespace.name_join('cohort', 'casedef_timeline')
        self.assertEqual(expected, actual)