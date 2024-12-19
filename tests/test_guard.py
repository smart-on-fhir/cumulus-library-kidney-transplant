import unittest
from irae import guard
from irae.criteria.race import Race

class TestGuard(unittest.TestCase):

    def test_list_type(self):
        self.assertTrue(guard.is_list_type([Race.asian], Race))
        self.assertTrue(guard.is_list_type(list(Race), Race))


if __name__ == '__main__':
    unittest.main()
