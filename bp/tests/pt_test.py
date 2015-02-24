import unittest
import bp.util.table as table

class TestNode:
    def __init__(self, name=None):
        if name is not None:
            self.name = name
        self.states = ['TRUE', 'FALSE']
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name


class TestPotentialTable(unittest.TestCase):

    def setUp(self):
        self.pt = table.PotentialTable()
        nodes = []
        for n in ['1W', '2R', '3S']:
            nodes.append(TestNode(name=n))
        self.pt.set_nodes(nodes)

    def test_permutation(self):
        state_list = self.pt._get_state_list()
        print state_list
        self.assertEqual(len(state_list), 2 ** len(self.pt.nodes))

    def test_init_table(self):
        self.pt.init_table()
        self.assertEqual(self.pt.table.values()[0], 0.0)
        print self.pt.get_json()

    def test_from_json(self):
        json_str = """{  "('TRUE', 'FALSE', 'TRUE')": 0.9,
                         "('TRUE', 'FALSE', 'FALSE')": 0.01,
                         "('TRUE', 'TRUE', 'TRUE')": 0.99,
                         "('TRUE', 'TRUE', 'FALSE')": 0.9,
                         "('FALSE', 'FALSE', 'FALSE')": 0.99,
                         "('FALSE', 'TRUE', 'TRUE')": 0.01,
                         "('FALSE', 'TRUE', 'FALSE')": 0.1,
                         "('FALSE', 'FALSE', 'TRUE')": 0.1}""";
        self.pt.set_table_from_json_str(json_str)
        self.assertEqual(len(self.pt.table), 2 ** len(self.pt.nodes))
    def test_to_json(self):
        json_str = """{  "('TRUE', 'FALSE', 'TRUE')": 0.9,
                         "('TRUE', 'FALSE', 'FALSE')": 0.01,
                         "('TRUE', 'TRUE', 'TRUE')": 0.99,
                         "('TRUE', 'TRUE', 'FALSE')": 0.9,
                         "('FALSE', 'FALSE', 'FALSE')": 0.99,
                         "('FALSE', 'TRUE', 'TRUE')": 0.01,
                         "('FALSE', 'TRUE', 'FALSE')": 0.1,
                         "('FALSE', 'FALSE', 'TRUE')": 0.1}""";
        self.pt.set_table_from_json_str(json_str)
        print self.pt.get_json()

    def test_sum_out_var(self):
        json_str = """{  "('TRUE', 'FALSE', 'TRUE')": 0.9,
                         "('TRUE', 'FALSE', 'FALSE')": 0.01,
                         "('TRUE', 'TRUE', 'TRUE')": 0.99,
                         "('TRUE', 'TRUE', 'FALSE')": 0.9,
                         "('FALSE', 'FALSE', 'FALSE')": 0.99,
                         "('FALSE', 'TRUE', 'TRUE')": 0.01,
                         "('FALSE', 'TRUE', 'FALSE')": 0.1,
                         "('FALSE', 'FALSE', 'TRUE')": 0.1}""";
        self.pt.set_table_from_json_str(json_str)
        new_table = self.pt.sum_out_var_by_idx(2)
        print new_table.get_json()

    def test_setting(self):
        pt = table.PotentialTable()
        nodes = []
        for n in ['A', 'B', 'C']:
            nodes.append(TestNode(name=n))
        pt.set_nodes(nodes[:2])

        json_str = """{  "('TRUE', 'TRUE')": 0.3,
                         "('TRUE', 'FALSE')": 0.7,
                         "('FALSE', 'FALSE')": 0.2,
                         "('FALSE', 'TRUE')": 0.8}""";
        pt.set_table_from_json_str(json_str)

        print pt.get_row_setting(('TRUE','FALSE'))

    def test_multiply(self):
        pt = table.PotentialTable()
        pt2 = table.PotentialTable()
        nodes = []
        for n in ['A', 'B', 'C']:
            nodes.append(TestNode(name=n))
        pt.set_nodes(nodes[:2])
        pt2.set_nodes(nodes[1:])

        json_str = """{  "('TRUE', 'TRUE')": 0.3,
                         "('TRUE', 'FALSE')": 0.7,
                         "('FALSE', 'FALSE')": 0.2,
                         "('FALSE', 'TRUE')": 0.8}""";
        pt.set_table_from_json_str(json_str)

        json_str = """{  "('TRUE', 'TRUE')": 0.1,
                         "('TRUE', 'FALSE')": 0.9,
                         "('FALSE', 'FALSE')": 0.5,
                         "('FALSE', 'TRUE')": 0.5}""";
        pt2.set_table_from_json_str(json_str)

        new_table = pt.multiply(pt2)
        new_table.show_table()