import sys

from prj3_robdd import *

def Project3(argc, argv):
    if argc >= 2:
        infile = open(argv[1], 'r')
        dummy = infile.readline()
        count = int(infile.readline())
        varSeq = infile.readline().split()
        for i in range(len(varSeq)):
            varSeq[i] = varSeq[i].strip()
        R = ROBDD(varSeq)

        for i in range(count):
            instr = infile.readline()
            Xstr = instr.split('=')[0].strip()
            iteParam = instr.split('(')[1].split(')')[0].split(',')
            for i in range(len(iteParam)):
                iteParam[i] = iteParam[i].strip()
                p = iteParam[i]
                if '+' in p:
                    Fstr, var = str.split(p, '+')
                    R.addCofFormula(Fstr, var, '+')
                elif '-' in p:
                    Fstr, var = str.split(p, '-')
                    R.addCofFormula(Fstr, var, '-')
            R.addIteFormula(Xstr, iteParam[0], iteParam[1], iteParam[2])
            R.showFormula(Xstr)

        print('---------- Print ----------')
        while True:
            instr = infile.readline()
            if len(instr.split()) < 2:
                break
            Xstr = instr.split()[1].strip()
            R.showFormula(Xstr)
        print('---------------------------')
        
    else:
        dummy = input()
        count = int(input())
        varSeq = input().split()
        for i in range(len(varSeq)):
            varSeq[i] = varSeq[i].strip()
        R = ROBDD(varSeq)

        for i in range(count):
            instr = input()
            Xstr = instr.split('=')[0].strip()
            iteParam = instr.split('(')[1].split(')')[0].split(',')
            for i in range(len(iteParam)):
                iteParam[i] = iteParam[i].strip()
                p = iteParam[i]
                if '+' in p:
                    Fstr, var = str.split(p, '+')
                    R.addCofFormula(Fstr, var, '+')
                elif '-' in p:
                    Fstr, var = str.split(p, '-')
                    R.addCofFormula(Fstr, var, '-')
            R.addIteFormula(Xstr, iteParam[0], iteParam[1], iteParam[2])
            R.showFormula(Xstr)

        print('---------- Print ----------')
        while True:
            instr = input()
            if len(instr.split()) < 2:
                break
            Xstr = instr.split()[1].strip()
            R.showFormula(Xstr)
        print('---------------------------')


if __name__ == '__main__':
	Project3(len(sys.argv), sys.argv)