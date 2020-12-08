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
        queue.extend([i for i in adj if (i != G.AllNodes[2] and i.visited == False)])

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

    queue = collection

    while len(queue) > 0:
        pn = queue.pop(0)
        # skip terminals
        if pn in terminals:
            continue
        # skip nodes whose degree > 2
        adj = GetAdjNodes(pn, netType)
        if len(adj) != 2:
            continue
        
        # parallel reduction + series reduction
        n1 = adj[0]
        e1 = [pe for pe in pn.edges if (not pe.deleted) and GetConnNode(n1, pe)]
        n2 = adj[1]
        e2 = [pe for pe in pn.edges if (not pe.deleted) and GetConnNode(n2, pe)]
        SPTNew1 = e1[0].SPTree
        SPTNew2 = e2[0].SPTree
        if len(e1) >= 2:
            for pe in e1[1:]:
                SPTNew1 = SPNode('p', False, [SPTNew1, pe.SPTree])
        if len(e2) >= 2:
            for pe in e2[1:]:
                SPTNew2 = SPNode('p', False, [SPTNew2, pe.SPTree])
        # delete old edges
        for pe in e1:
            pe.deleted = True
        for pe in e2:
            pe.deleted = True
        # construct new edge
        SPTNew = SPNode('s', False, [SPTNew1, SPTNew2])
        eNew = Edge(SPTNew, [n1, n2])
        # add new edge to nodes
        n1.edges.append(eNew)
        n2.edges.append(eNew)
        # add nodes to queue
        queue.append(n1)
        queue.append(n2)
    
    # deal with terminals
    pn = terminals[0]
    for pe in pn.edges:
        if pe.deleted == False and GetConnNode(pn, pe) != terminals[1]:
            # ...
            print('Error')
            sys.exit()
    e = [pe for pe in pn.edges if (not pe.deleted)]
    SPTNew = e[0].SPTree
    if len(e) >= 2:
        for pe in e[1:]:
            SPTNew = SPNode('p', False, [SPTNew, pe.SPTree])
    for pe in e:
        pe.deleted = True
    # construct new edge
    eNew = Edge(SPTNew, terminals)
    # add new edge to nodes
    terminals[0].edges = [eNew]
    terminals[1].edges = [eNew]
