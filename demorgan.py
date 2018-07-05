from z3 import *

# create two boolean variables

a = Bool("a")
b = Bool("b")

constraints1 = []

# demorgans first law, Not (a or b) is the same as Not a and not b

constraints1.append(Or(a, b))
constraints1.append(And(Not(a), Not(b)))

# create solver, add constraint, print satisfiability

s1 = Solver()

s1.add(constraints1)

print("A or B AND not A and not B: " + str(s1.check()))

constraints2 = []

# demorgans second law, Not (a and b) is the same as Not a or not b

constraints2.append(And(a, b))
constraints2.append(Or(Not(a), Not(b)))

# create solver, add constraint, print satisfiability

s2 = Solver()

s2.add(constraints2)

print("A and B AND not A or not B: " + str(s1.check()))



