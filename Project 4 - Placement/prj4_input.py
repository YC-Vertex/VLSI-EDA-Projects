import sys

from prj4_data import *

def InputFile(infile):
    L = int(infile.readline())
    W = int(infile.readline())
    cellCount = int(infile.readline())
    netCount = int(infile.readline())
    layout = Layout(L, W, netCount)
    infile.readline()
    for netIndex in range(netCount):
        cs = infile.readline().split()
        for c in cs:
            cell = layout.AllCells.get(c)
            if cell == None:
                layout.AllCells[c] = Cell()
                layout.AllCells[c].addNet(netIndex)
            else:
                cell.addNet(netIndex) 
    return layout

def InputConsole():
    L = int(input())
    W = int(input())
    cellCount = int(input())
    netCount = int(input())
    layout = Layout(L, W, netCount)
    input()
    for netIndex in range(netCount):
        cs = input().split()
        for c in cs:
            cell = layout.AllCells.get(c)
            if cell == None:
                layout.AllCells[c] = Cell()
                layout.AllCells[c].addNet(netIndex)
            else:
                cell.addNet(netIndex) 
    return layout
