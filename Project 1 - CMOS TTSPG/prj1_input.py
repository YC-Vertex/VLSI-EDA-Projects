''' ... '''

from prj1_graph import *

# 
def InputFile(infile):
    G = Graph()
    eCount = int(infile.readline())
    nCount = int(infile.readline())
    for i in range(nCount):
        nNew = Node(i)
        G.AllNodes[i] = nNew
    for i in range(eCount):
        n1, n2, signal = infile.readline().split()
        pn1 = G.AllNodes[int(n1)]
        pn2 = G.AllNodes[int(n2)]
        eNew = Edge(SPNode(signal), [pn1, pn2])
        pn1.edges.append(eNew)
        pn2.edges.append(eNew)
        G.AllEdges.append(eNew)
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
        pn1 = G.AllNodes[int(n1)]
        pn2 = G.AllNodes[int(n2)]
        eNew = Edge(SPNode(signal), [pn1, pn2])
        pn1.edges.append(eNew)
        pn2.edges.append(eNew)
        G.AllEdges.append(eNew)
    return G
