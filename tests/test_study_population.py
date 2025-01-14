import unittest
from irae import study_population

class TestStudyPopulation(unittest.TestCase):

    def test_table_names(self):
        table_list = study_population.list_tables()
        print(table_list)
