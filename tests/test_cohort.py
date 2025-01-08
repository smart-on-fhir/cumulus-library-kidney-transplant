import unittest
from irae import cohort

class TestCohort(unittest.TestCase):

    def test(self):
        print(cohort.cohort_dx('irae__dx_autoimmune'))
        print(cohort.cohort_rx('irae__rx_htn'))
        print(cohort.cohort_lab('irae__lab_lft'))


if __name__ == '__main__':
    unittest.main()
