import sys

from prj1_graph import Node, Edge, graph
from prj1_input import InputFile, InputConsole

def Project1(argc, argv):
    G = graph()
    
    # input
    if sys.argc >= 2:
        infile = open(sys.argv[1], 'r')
        InputFile(G, infile)
    else:
        InputConsole(G, nCount, eCount)
            
    # graph partition
    G.nodes[0].netType = 'n'
    G.nodes[1].netType = 'p'
    DfsNodePartition(G, [G.nodes[0]], 'n')
    for pn in G.nodes.values():
        if pn.index != 2 and pn.netType == 'np':
            pn.netType = 'p'
    for pe in G.edges.values():
        if pe.netType == 'np':
            pe.netType = 'p'
    
    # TTSP detection, SPT generation
    T = SPNode()
    SPTGen(G, T)

# main
if __name__ == '__main__':
    Project1(argc, argv)
