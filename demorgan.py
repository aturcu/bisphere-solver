from z3 import *

a = Bool("a")
b = Bool("b")

constraints1 = []

constraints1.append(Or(a, b))
constraints1.append(And(Not(a), Not(b)))

s1 = Solver()

s1.add(constraints1)

print("not (A or B) AND not A and not B: " + str(s1.check()))

constraints2 = []

constraints2.append(And(a, b))
constraints2.append(Or(Not(a), Not(b)))

s2 = Solver()

s2.add(constraints2)

print("not (A and B) AND not A or not B: " + str(s1.check()))



