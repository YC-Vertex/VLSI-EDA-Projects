''' ... '''

from prj1_graph import *

# graph partition using DFS
def DfsNodePartition(G, queue, netType = 'n'):
    pn = queue.pop(0)
    adj = GetAdjNodes(pn)
    # ...

#  series-parallel tree generation
def SPTGen(G, T):
    # ...
