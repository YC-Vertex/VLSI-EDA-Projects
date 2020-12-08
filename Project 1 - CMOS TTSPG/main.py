import sys

from prj1_algorithm import *
from prj1_graph import *
from prj1_input import *

def Project1(argc, argv):
    G = None
    
    # input
    if argc >= 2:
        infile = open(argv[1], 'r')
        G = InputFile(infile)
    else:
        G = InputConsole()
            
    # graph partition
    NodePartition(G, [G.AllNodes[0]], 'n')
    NodePartition(G, [G.AllNodes[1]], 'p')
    EdgePartition(G)

    # debug output
    print(len(G.nNodes), len(G.pNodes))
    for pn in G.AllNodes.values():
        print(pn.index, pn.netType)
    for pe in G.AllEdges:
        print([pe.nodes[0].index, pe.nodes[1].index], pe.netType)

    # TTSP detection, SPT generation
    return
    SPTGen(G, 'n')
    SPTGen(G, 'p')

# main
if __name__ == '__main__':
    Project1(len(sys.argv), sys.argv)
