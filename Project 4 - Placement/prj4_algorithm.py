import random
import math
import copy

from prj4_data import *

def GetRandomVacancy(L):
    x = random.randint(0, L.xlim-1)
    y = random.randint(0, L.ylim-1)
    while L.layout[x][y] != None:
        x = random.randint(0, L.xlim-1)
        y = random.randint(0, L.ylim-1)
    return x, y

def RandomPlacement(L):
    for k,v in L.AllCells.items():
        x, y = GetRandomVacancy(L)
        L.layout[x][y] = k
        v.loc = [x, y]

def SimulatedAnnealing(L, Tstart, Tend, iterPerT):
    T = Tstart
    alpha = 0.95
    iterEst = math.log(Tend/Tstart, 0.85) # 对总退火周期的估计
    print('estimated annealing iterations:', iterEst * iterPerT)

    iOuterLoop = 0
    while T > Tend:
        cost = [L.getCost()]
        accepted = list()
        # 退火过程
        for iInnerLoop in range(iterPerT):
            flag = random.randint(0, 1)
            Lnew = copy.deepcopy(L)
            # 移动
            if flag:
                tIndex = random.choice(list(Lnew.AllCells.keys()))
                Lnew.move(tIndex, GetRandomVacancy(Lnew))
            # 交换
            else:
                t1Index = random.choice(list(Lnew.AllCells.keys()))
                t2Index = random.choice(list(Lnew.AllCells.keys()))
                while t2Index == t1Index:
                    t2Index = random.choice(list(Lnew.AllCells.keys()))
                Lnew.swap(t1Index, t2Index)
            cost.append(Lnew.getCost())
            delta = cost[-1] - cost[-2]
            if random.random() < math.exp(-delta/T):
                L = Lnew
                accepted.append(True)
            else:
                cost[-1] = cost[-2]
                accepted.append(False)
        print('temperature:', T)
        print('cost:', cost[1:])
        print('accepted:', accepted)
        # 降低温度
        if iOuterLoop < iterEst * 0.25:
            alpha -= (0.95 - 0.8) / (iterEst / 4)
        elif iOuterLoop > iterEst * 0.75:
            alpha += (0.95 - 0.8) / (iterEst / 4)
        if alpha < 0.8:
            alpha = 0.8
        elif alpha > 0.95:
            alpha = 0.95
        T *= alpha
        iOuterLoop += 1
    return L
        