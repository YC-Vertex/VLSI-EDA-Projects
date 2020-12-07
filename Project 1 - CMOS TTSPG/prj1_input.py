''' ... '''

from prj1_graph import *

# 
def InputFile(G, infile):
    # ...
    return [eCount, nCount]

# 
def InputConsole(G):
    eCount = input()
    nCount = input()
    for i in range(nCount):
        G.AddNode(i)
    for i in range(eCount):
        n1 = input()
        n2 = input()
        signal = input()
        G.AddEdge_NodeIndex(signal, n1, n2)
