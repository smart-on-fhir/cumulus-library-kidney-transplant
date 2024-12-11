import unittest
from enum import Enum
from typing import List, Dict
from kidney_transplant import common, guard
from kidney_transplant.criteria.demographic.race import Race

class TestGuard(unittest.TestCase):

    def test_list_type(self):
        self.assertTrue(guard.is_list_type([Race.asian], Race))
        self.assertTrue(guard.is_list_type(list(Race), Race))


if __name__ == '__main__':
    unittest.main()
