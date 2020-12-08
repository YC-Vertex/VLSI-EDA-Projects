import sys

from prj1_algorithm import *
from prj1_graph import *
from prj1_input import *

def Project1(argc, argv):
    G = None
    debugEn = False
    
    # input
    if argc >= 2:
        infile = open(argv[1], 'r')
        G = InputFile(infile)
    else:
        G = InputConsole()
    
    # debug output
    if debugEn:
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
    if debugEn:
        print('\n----- debug 2 -----')
        print(len(G.nNodes), len(G.pNodes))
        for pn in G.AllNodes.values():
            print(pn.index, pn.netType, pn.edges)
        for pe in G.AllEdges:
            print([pe.nodes[0].index, pe.nodes[1].index], pe.netType, pe.nodes)
        print('----------')

    # TTSP detection, SPT generation
    SPTGeneration(G, 'n')
    SPTGeneration(G, 'p')
    SPTn = G.AllNodes[0].edges[0].SPTree
    SPTp = G.AllNodes[1].edges[0].SPTree
    
    # print result
    print('\n----- logic result -----')
    print('n-net logic: ', end = '')
    G.AllNodes[0].edges[0].ShowExpr()
    print('p-net logic: ', end = '')
    G.AllNodes[1].edges[0].ShowExpr()
    print('----------')

    # check duality
    NormalFormTransform(SPTn, None)
    NormalFormTransform(SPTp, None)
    dual = CheckDuality(SPTn, SPTp)

    # print result
    print('\n----- duality test result -----')
    if dual:
        print('success')
    else:
        print('Error 0: circuit definition violates duality assertion')
    print('----------')

# main
if __name__ == '__main__':
    Project1(len(sys.argv), sys.argv)
