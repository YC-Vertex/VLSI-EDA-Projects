from prj3_robdd import *

robdd = ROBDD(['x1', 'x2', 'x3'])
t = robdd.formulas['T']
f = robdd.formulas['F']

A = robdd.addFormula('A', 'x3', t, f, False)
robdd.showFormula('A')

B = robdd.addFormula('B', 'x3', f, t, False)
robdd.showFormula('B')

C = robdd.addFormula('C', 'x2', f, B, False)
robdd.showFormula('C')

print(robdd.table)