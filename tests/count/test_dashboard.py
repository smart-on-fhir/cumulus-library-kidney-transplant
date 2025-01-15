import unittest
from cumulus_library_kidney_transplant.count import dashboard

class TestDashboard(unittest.TestCase):

    def test_graph_list(self):
        for graph in dashboard.graph_list():
            print(graph.as_json())


if __name__ == '__main__':
    unittest.main()
