class Node:
    def __init__(self, var, posCof, negCof):
        self.var = var
        self.posCof = posCof
        self.negCof = negCof

class Formula:
    def __init__(self, node, compBit):
        self.node = node
        self.compBit = compBit

class ROBDD:
    # init
    def __init__(self, varSeq):
        self.varSeq = varSeq + ['1']
        self.table = dict()
        self.formulas = dict()
        self.addLeafNode()
        self.formulas['T'] = Formula(self.leafNode, False)
        self.formulas['F'] = Formula(self.leafNode, True)

    # apply ite(F,G,H) and add the formula to the formula collection self.formulas
    # calls self.applyIteRec to apply ite recursively
    def addIteFormula(self, Xstr, Fstr, Gstr, Hstr):
        F = self.formulas[Fstr]
        G = self.formulas[Gstr]
        H = self.formulas[Hstr]
        X = self.applyIte(F, G, H, 0)
        self.formulas[Xstr] = X

    # apply ite(F,G,H) recursively
    # returns a Formula
    def applyIte(self, F, G, H, varIndex):
        # check terminal cases
        if F == self.formulas['T']:
            return G
        elif F == self.formulas['F']:
            return H
        elif G == self.formulas['T'] and H == self.formulas['F']:
            return F
        elif G == self.formulas['F'] and H == self.formulas['T']:
            return Formula(F.node, not F.compBit)
        # apply ite recursively
        var = self.varSeq[varIndex]
        # 这里有点问题，F.node.posCof的varIndex可能大于varIndex+1（一次跳多级）
        posCof = self.applyIteRec(F.node.posCof, G.node.posCof, H.node.posCof, varIndex + 1)
        negCof = self.applyIteRec(F.node.negCof, G.node.negCof, H.node.negCof, varIndex + 1)
        # check if repetitive
        node, compBit = self.findNode(var, posCof, negCof)
        return Formula(node, compBit)
    
    def addLeafNode(self):
        self.leafNode = Node('1', None, None)
        entry = ('1', -1, -1, -1, -1)
        self.table[entry] = self.leafNode

    # add a node to the unique table
    # returns a Node
    def addNode(self, var, posCof, negCof):
        #pc = posCof
        #nc = negCof
        pc = Formula(posCof.node, posCof.compBit)
        nc = Formula(negCof.node, negCof.compBit)
        node = self.findNode(var, pc, nc)
        if node != None:
            return node, False
        else:
            # guarentee that the posCof edge must be a regular edge
            cb = pc.compBit
            if cb:
                pc.compBit = not(pc.compBit)
                nc.compBit = not(nc.compBit)
            entry = (var, id(pc.node), pc.compBit, id(nc.node), nc.compBit)
            # create a new node
            node = Node(var, pc, nc)
            self.table[entry] = node
            return node, cb

    # find a node from the unique table
    # returns None if not found
    def findNode(self, var, posCof, negCof):
        if var == '1':
            return self.leafNode
        pc = posCof
        nc = negCof
        entry = (var, id(pc.node), pc.compBit, id(nc.node), nc.compBit)
        node = self.table.get(entry)
        return node
    
    def addFormula(self, Xstr, var, posCof, negCof, compBit):
        node, cb = self.addNode(var, posCof, negCof)
        X = Formula(node, compBit ^ cb)
        self.formulas[Xstr] = X
        return X

    def showFormula(self, Xstr):
        X = self.formulas[Xstr]
        if X.node.var == '1':
            print(Xstr, '=', not X.compBit)
        else:
            print(Xstr, '=', end = ' ')
            self.showRec(X, False, list())
            print(0)
    
    def showRec(self, X, compBit, varList):
        if X.node == self.leafNode:
            if X.compBit ^ compBit:
                return
            else:
                for var in varList:
                    print(var, end = '')
                print(' + ', end = '')
        else:
            self.showRec(X.node.posCof, compBit ^ X.compBit, varList + [X.node.var])
            self.showRec(X.node.negCof, compBit ^ X.compBit, varList + ['~' + X.node.var])
