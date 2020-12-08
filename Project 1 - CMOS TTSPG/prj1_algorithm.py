''' ... '''

from prj1_graph import *

# graph partition
def NodePartition(G, queue, netType):
    collection = list()
    if netType == 'n':
        collection = G.nNodes
    elif netType == 'p':
        collection = G.pNodes
    else:
        # ....
        print('Error')
        sys.exit()

    while len(queue) > 0:
        pn = queue.pop(0)
        # process node
        pn.visited = True
        pn.netType = netType
        collection.append(pn)
        # add adjacent nodes to queue (node != output && node not visited)
        adj = GetAdjNodes(pn)
        queue.extend([i for i in adj if (i != G.nodes[2] and i.visited == False)])

def EdgePartition(G):
    for pe in G.AllEdges:
        if pe.nodes[0].IsInNet('n') and pe.nodes[1].IsInNet('n'):
            pe.netType = 'n'
        elif pe.nodes[0].IsInNet('p') and pe.nodes[1].IsInNet('p'):
            pe.netType = 'p'
        else:
            # ...
            print('Error')
            sys.exit()

#  series-parallel tree generation
def SPTGen(G, netType):
    collection = list()
    terminals = list()
    if netType == 'n':
        collection = G.nNodes
        terminals = [G.AllNodes[0], G.AllNodes[2]]
    elif netType == 'p':
        collection = G.pNodes
        terminals = [G.AllNodes[1], G.AllNodes[2]]
    else:
        # ...
        print('Error')
        sys.exit()

    while len(queue) > 0:
        # ...
        return

