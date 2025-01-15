import unittest
from cumulus_library_kidney_transplant import guard
from cumulus_library_kidney_transplant.criteria import encounter_type
from cumulus_library_kidney_transplant.criteria.race import Race

class TestGuard(unittest.TestCase):

    def test_list_type(self):
        self.assertTrue(guard.is_list_type([Race.asian], Race))
        self.assertTrue(guard.is_list_type(list(Race), Race))

    def test_filter_list_coding(self):
        standard = encounter_type.list_coding()


if __name__ == '__main__':
    unittest.main()
