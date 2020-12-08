''' ... '''

from prj1_graph import *

# 
def InputFile(infile, AllNodes, AllEdges):
    G = Graph()
    # ...
    return G

# 
def InputConsole():
    G = Graph()
    eCount = int(input())
    nCount = int(input())
    for i in range(nCount):
        nNew = Node(i)
        G.AllNodes[i] = nNew
    for i in range(eCount):
        n1, n2, signal = input().split()
        n1 = int(n1)
        n2 = int(n2)
        eNew = Edge(SPNode(signal), [G.AllNodes[n1], G.AllNodes[n2]])
        G.AllEdges.append(eNew)
    return G
