from z3 import *

# create two boolean variables

a = Bool("a")
b = Bool("b")

constraints1 = []

# to show one implies the other, try to find a counterexample to the implication

constraints1.append(Not(Or(a, b)))
constraints1.append(Not(And(Not(a), Not(b))))

# create solver, add constraint, print satisfiability

s1 = Solver()

s1.add(constraints1)

print("Counterexample for: not A or B implies not A and not B: " + str(s1.check()))

# now, in the other direction

constraints2 = []

constraints2.append(Not(Not(Or(a,b))))
constraints2.append(And(Not(a), Not(b)))

s2 = Solver()

s2.add(constraints2)

print("Counterexample for: not A and not B implies not A or B: " + str(s2.check()))

constraints3 = []

# demorgans second law, Not (a and b) is the same as Not a or not b

constraints3.append(Not(And(a, b)))
constraints3.append(Not(Or(Not(a), Not(b))))

# create solver, add constraint, print satisfiability

s3 = Solver()

s3.add(constraints3)

print("Counterexample for: not A and B implies not A or not B: " + str(s3.check()))

# now in the other direction

constraints4 = []

constraints4.append(Not(Not(And(a, b))))
constraints4.append(Or(Not(a), Not(b)))

s4 = Solver()

s4.add(constraints4)

print("Counterexample for: not A or not B implies not A and B: " + str(s4.check()))

