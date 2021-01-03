class Cell:
    def __init__(self):
        self.loc = [-1, -1]
        self.net = list()
    def addNet(self, netIndex):
        self.net.append(netIndex)

class Layout:
    def __init__(self, length, width, netCount):
        self.xlim = length
        self.ylim = width
        self.netCount = netCount
        self.AllCells = dict()
        self.layout = list()
        for i in range(self.xlim):
            self.layout.append([None] * self.ylim)
    def getCost(self):
        netHull = list()
        for i in range(self.netCount):
            netHull.append([[self.xlim, self.ylim], [-1, -1]])
        for cell in self.AllCells.values():
            for net in cell.net:
                if cell.loc[0] < netHull[net][0][0]:
                    netHull[net][0][0] = cell.loc[0]
                if cell.loc[0] > netHull[net][1][0]:
                    netHull[net][1][0] = cell.loc[0]
                if cell.loc[1] < netHull[net][0][1]:
                    netHull[net][0][1] = cell.loc[1]
                if cell.loc[1] > netHull[net][1][1]:
                    netHull[net][1][1] = cell.loc[1]
        cost = 0
        for net in range(self.netCount):
            cost += netHull[net][1][0] - netHull[net][0][0]
            cost += netHull[net][1][1] - netHull[net][0][1]
        return cost
    def move(self, cindex, loc):
        cell = self.AllCells[cindex]
        self.layout[cell.loc[0]][cell.loc[1]] = None
        self.layout[loc[0]][loc[1]] = cindex
        cell.loc = loc[:]
    def swap(self, c1index, c2index):
        c1 = self.AllCells[c1index]
        c2 = self.AllCells[c2index]
        loc1 = c1.loc[:]
        loc2 = c2.loc[:]
        c1.loc = loc2[:]
        c2.loc = loc1[:]
        self.layout[loc1[0]][loc1[1]] = c2index
        self.layout[loc2[0]][loc2[1]] = c1index
    def showCells(self):
        print('---------- Cells  ----------')
        for k,v in self.AllCells.items():
            print('id:', k, 'net:', v.net, 'loc:', v.loc)
        print('----------------------------')
    def showLayout(self):
        print('---------- Layout ----------')
        for row in self.layout:
            print(row)
        print('cost:', self.getCost())
        print('----------------------------')
