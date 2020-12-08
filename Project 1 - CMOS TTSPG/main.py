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
    
    # debug output
    print('\n----- debug 1 -----')
    for pn in G.AllNodes.values():
        print(pn, pn.edges)
    for pe in G.AllEdges:
        print(pe, pe.nodes)
    print('----------')
            
    # graph partition
    G.ResetNodeStatus()
    G.ResetEdgeStatus()
    NodePartition(G, [G.AllNodes[0]], 'n')
    NodePartition(G, [G.AllNodes[1]], 'p')
    EdgePartition(G)
    for pe in G.AllEdges:
        if pe.netType == 'p':
            pe.SPTree.signal += '\''

    # debug output
    print('\n----- debug 2 -----')
    print(len(G.nNodes), len(G.pNodes))
    for pn in G.AllNodes.values():
        print(pn.index, pn.netType, pn.edges)
    for pe in G.AllEdges:
        print([pe.nodes[0].index, pe.nodes[1].index], pe.netType, pe.nodes)
    print('----------')

    # TTSP detection, SPT generation
    SPTGen(G, 'n')
    SPTGen(G, 'p')
    
    # debug output
    print('\n----- debug 3 -----')
    for pe in G.AllNodes[0].edges:
        pe.ShowExpr()
    for pe in G.AllNodes[1].edges:
        pe.ShowExpr()
    print('----------')

# main
if __name__ == '__main__':
    Project1(len(sys.argv), sys.argv)
