import unittest
import bp.util.BIFParser as parser
import bp.util.bcgraph as bcgraph

class TestBCGraph(unittest.TestCase):

    def setUp(self):
        f = open("bp/tests/tree.bif","r")
        BIF = f.readlines()
        BIF = parser.fixWhiteSpace(BIF)
        self.nodes = parser.parseBIF(BIF)

    def test_building_graph(self):
        graph = bcgraph.BCGraph()
        graph.build_graph_from_BN(self.nodes)
        self.assertEquals(len(graph.var_nodes), 4)
        self.assertEquals(len(graph.factor_nodes), 4)


