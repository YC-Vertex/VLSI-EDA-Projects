from prj3_robdd import *

robdd = ROBDD(['x1', 'x2', 'x3'])
t = robdd.formulas['T']
f = robdd.formulas['F']

A = robdd.addFormula('A', 'x3', t, f, False)
robdd.showFormula('A')

A_ = robdd.addFormula('A_', 'x3', t, f, False)
print(A_ == A)

B = robdd.addFormula('B', 'x3', f, t, False)
robdd.showFormula('B')

C = robdd.addFormula('C', 'x2', f, B, False)
robdd.showFormula('C')

D = robdd.addIteFormula('D', 'A', 'C', 'F')
robdd.showFormula('D')

E = robdd.addIteFormula('E', 'B', 'C', 'F')
robdd.showFormula('E')

robdd.addCofFormula('B', 'x3', '+')
robdd.showFormula('B+x3')

robdd.addCofFormula('E', 'x2', '+')
robdd.showFormula('E+x2')

robdd.addCofFormula('E', 'x2', '-')
robdd.showFormula('E-x2')


print(robdd.table)