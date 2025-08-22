import unittest
from cumulus_library_kidney_transplant import guard
from cumulus_library_kidney_transplant.criteria.race import Race

class TestGuard(unittest.TestCase):

    def test_list_type(self):
        self.assertTrue(guard.is_list_type([Race.asian], Race))
        self.assertTrue(guard.is_list_type(list(Race), Race))

    def test_as_type(self):
        expect_float = '3.14'
        expect_int = '1'

        self.assertAlmostEqual(3.14, guard.as_number(expect_float))
        self.assertAlmostEqual(1, guard.as_number(expect_int))
        self.assertTrue(guard.as_bool('true'))
        self.assertFalse(guard.as_bool('false'))

