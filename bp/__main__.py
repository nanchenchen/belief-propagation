import util.BIFParser as parser
import util.bcgraph as bcgraph
import sys

f = open("%s" %sys.argv[1],"r")
BIF = f.readlines()

BIF = parser.fixWhiteSpace(BIF)
nodes = parser.parseBIF(BIF)
#parser.printNodes(nodes)

graph = bcgraph.BCGraph()
graph.build_graph_from_BN(nodes)

threshold = 1e-10

while True:
    diff_value = graph.var_to_factor_propagate()
    if diff_value < threshold:
        break
    diff_value = graph.factor_to_var_propagate()
    if diff_value < threshold:
        break

    graph.show_vars()
