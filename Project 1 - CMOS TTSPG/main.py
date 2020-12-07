import sys

# node data structure
class Node:
    def __init__(self, nIndex, pe = []):
        self.index = nIndex
        self.edges = pe
        self.netType = 'np' # undetermined net type
        
# edge data structure
class Edge:
    def __init__(self, signal, pn1, pn2):
        self.signal = signal
        self.nodes = [pn1, pn2]
        self.netType = 'np' # undetermined net type

# graph data structure
class graph:
    def __init__(self):
        self.nodes = dict()
        self.edges = []

# get adjacent nodes
def GetAdjNodes(G, pn, netType = 'x'):
    adj = []
    for pe in pn.edges:
        if pe.nodes[0] == pn:
            adj.append(pe.nodes[1])
        else:
            adj.append(pe.nodes[0])
    return adj
    
# 
def IsInNet(obj, netType):
    return (obj.netType.find(netType) != -1)
        
# graph partition using DFS
def DfsNodePartition(G, queue, netType = 'n'):
    pn = queue.pop(0)
    adj = GetAdjNodes(pn)
    # ...

# 
def InputFile(G, infile):
    # ...
    return [eCount, nCount]

# 
def InputConsole(G):
    eCount = input()
    nCount = input()
    for i in range(nCount):
        G.nodes[i] = Node(i)
    for i in range(eCount):
        n1 = input()
        n2 = input()
        signal = input()
        pn1 = G.nodes.get(n1)
        pn2 = G.nodes.get(n2)
        # check index validity
        if pn1 == None or pn2 == None:
            print("Error: invalid node index")
            sys.exit()
        # add to graph
        eNew = Edge(signal, pn1, pn2)
        G.edges.append(eNew)
        pn1.edges.append(eNew)
        pn2.edges.append(eNew)

# main
if __name__ == '__main__':
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
    
    # TTSP detection
    