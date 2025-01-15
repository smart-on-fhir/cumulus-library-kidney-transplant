import unittest
from cumulus_library_kidney_transplant import cohorts

class TestCohort(unittest.TestCase):

    def test(self):
        print(cohorts.cohort_dx('irae__dx_autoimmune'))
        print(cohorts.cohort_rx('irae__rx_htn'))
        print(cohorts.cohort_lab('irae__lab_lft'))


if __name__ == '__main__':
    unittest.main()
