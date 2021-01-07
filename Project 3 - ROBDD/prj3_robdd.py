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
        self.formulas['1'] = self.formulas['T']
        self.formulas['0'] = self.formulas['F']
        for var in varSeq:
            self.formulas[var] = Formula(Node(var, self.formulas['T'], self.formulas['F']), False)
            self.formulas['~'+var] = Formula(Node(var, self.formulas['T'], self.formulas['F']), True)
    
    # add the leaf node '1'
    def addLeafNode(self):
        self.leafNode = Node('1', None, None)
        entry = ('1', -1, -1, -1, -1)
        self.table[entry] = self.leafNode

    # add a node to the unique table
    # returns a Node
    def addNode(self, var, posCof, negCof):
        if self.cmpFormula(posCof, negCof):
            return posCof.node, posCof.compBit
        pc = self.cpyFormula(posCof)
        nc = self.cpyFormula(negCof)
        # guarentee that the posCof edge must be a regular edge
        cb = pc.compBit
        if cb:
            pc.compBit = not(pc.compBit)
            nc.compBit = not(nc.compBit)
        # check if repetitive node
        node = self.findNode(var, pc, nc)
        if node != None:
            return node, cb
        # add a new node
        else:
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
    
    # add a new formula to the formula collection
    def addFormula(self, Xstr, var, posCof, negCof, compBit):
        node, cb = self.addNode(var, posCof, negCof)
        X = Formula(node, compBit ^ cb)
        self.formulas[Xstr] = X
        return X

    # apply ite(F,G,H) and add the formula to the formula collection self.formulas
    # calls self.applyIteRec to apply ite recursively
    def addIteFormula(self, Xstr, Fstr, Gstr, Hstr):
        F = self.formulas[Fstr]
        G = self.formulas[Gstr]
        H = self.formulas[Hstr]
        X = self.applyIte(F, G, H, 0)
        self.formulas[Xstr] = X
        return X

    # apply ite(F,G,H) recursively
    # returns a Formula
    def applyIte(self, F, G, H, varIndex):
        # check terminal cases
        if self.cmpFormula(F, self.formulas['T']):
            return G
        elif self.cmpFormula(F, self.formulas['F']):
            return H
        elif self.cmpFormula(G, self.formulas['T']) and self.cmpFormula(H, self.formulas['F']):
            return F
        elif self.cmpFormula(G, self.formulas['F']) and self.cmpFormula(H, self.formulas['T']):
            return Formula(F.node, not F.compBit)
        # F.node的index可能大于varIndex（一次跳多级）
        var = self.varSeq[varIndex]
        if F.node.var == var:
            Fpc = F.node.posCof
            Fnc = F.node.negCof
            if F.compBit == True:
                Fpc = self.cpyFormula(Fpc)
                Fnc = self.cpyFormula(Fnc)
                Fpc.compBit = not Fpc.compBit
                Fnc.compBit = not Fnc.compBit
        else:
            Fpc = F
            Fnc = F
        if G.node.var == var:
            Gpc = G.node.posCof
            Gnc = G.node.negCof
            if G.compBit == True:
                Gpc = self.cpyFormula(Gpc)
                Gnc = self.cpyFormula(Gnc)
                Gpc.compBit = not Gpc.compBit
                Gnc.compBit = not Gnc.compBit
        else:
            Gpc = G
            Gnc = G
        if H.node.var == var:
            Hpc = H.node.posCof
            Hnc = H.node.negCof
            if H.compBit == True:
                Hpc = self.cpyFormula(Hpc)
                Hnc = self.cpyFormula(Hnc)
                Hpc.compBit = not Hpc.compBit
                Hnc.compBit = not Hnc.compBit
        else:
            Hpc = H
            Hnc = H
        # apply ite recursively
        posCof = self.applyIte(Fpc, Gpc, Hpc, varIndex + 1)
        negCof = self.applyIte(Fnc, Gnc, Hnc, varIndex + 1)
        # add the new node
        node, cb = self.addNode(var, posCof, negCof)
        return Formula(node, cb)
    
    # apply cofactor and add the formula to the formula collection self.formulas
    # calls self.applyCof to apply cofactor recursively
    def addCofFormula(self, Fstr, tgVar, sign):
        tgVarIndex = self.varSeq.index(tgVar)
        F = self.formulas[Fstr]
        X = self.applyCof(F, tgVarIndex, sign)
        self.formulas[Fstr + sign + tgVar] = X

    # apply cofactor
    # returns a Formula
    def applyCof(self, F, tgVarIndex, sign):
        # check terminal cases
        if tgVarIndex < self.varSeq.index(F.node.var):
            return F
        pc = self.cpyFormula(F.node.posCof)
        nc = self.cpyFormula(F.node.negCof)
        if F.compBit == True:
            pc.compBit = not pc.compBit
            nc.compBit = not nc.compBit
        if tgVarIndex == self.varSeq.index(F.node.var):
            if sign == '+':
                return pc
            else:
                return nc
        # apply cofactor
        posCof = self.applyCof(pc)
        negCof = self.applyCof(nc)
        # add the new node
        node, cb = self.addNode(F.node.var, posCof, negCof)
        return Formula(node, cb)
    
    # compares two formulas
    def cmpFormula(self, F1, F2):
        return F1.node == F2.node and F1.compBit == F2.compBit
    
    # copies a formula
    def cpyFormula(self, F):
        return Formula(F.node, F.compBit)

    #
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
