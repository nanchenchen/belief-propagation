import util.BIFParser as parser
import util.bcgraph as bcgraph
import sys


def usage():
    print >>sys.stderr, "Usage: python %s <.bif file path> [-o output file] [-t threshold]\n" % sys.argv[0]
    print >>sys.stderr, "Options:"
    print >>sys.stderr, "   -o, --output \t output file name, default to 'result.txt'"
    print >>sys.stderr, "   -t, --threshold \t threshold for convergence default to 1e-10"

if len(sys.argv) < 2:
    usage()
    exit()

threshold = 1e-10
result_file = "result.txt"

for i in range(1, len(sys.argv)):
    if sys.argv[i] == "-o" or sys.argv[i] == "--output":
        try:
            result_file = sys.argv[i + 1]
        except IndexError:
            usage()
            exit()
    elif sys.argv[i] == "-t" or sys.argv[i] == "--threshold":
        try:
            threshold = float(sys.argv[i + 1])
        except IndexError:
            usage()
            exit()

try:
    f = open("%s" %sys.argv[1],"r")
except IOError:
    print >>sys.stderr, "Cannot find the .BIF file!\n"
    usage()
    exit()

BIF = f.readlines()

BIF = parser.fixWhiteSpace(BIF)
nodes = parser.parseBIF(BIF)
f.close()
#parser.printNodes(nodes)

graph = bcgraph.BCGraph()
graph.build_graph_from_BN(nodes)



while True:
    diff_value = graph.var_to_factor_propagate()
    if diff_value < threshold:
        break
    diff_value = graph.factor_to_var_propagate()
    if diff_value < threshold:
        break

    #graph.show_vars()

f = open("result.txt", "w")
print >> f, graph.marginalized_results(nodes)
f.close()