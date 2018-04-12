# Produce N-queens problem as DIMACS file, then invoke glucose on it
# Note: list.append in python is really "add", not Racket-style append.

from math import *
import time
import os

# N-queens using boolean variables

n = input("Enter n: ")

t0 = time.time()

clauses = []

# 0-based input, 1-based output
def getv(row, col):
	return n*row + col + 1

# One boolean variable for each square: is there a queen there or not?

# Exactly one queen per row
for row in range(n):
	# >= 1
	clauses.append([ getv(row, j) for j in range(n)])
	# < 2: if true in one column, not true in all others
	for col in range(n):
		for col2 in range(col+1, n):			
			clauses.append([ -getv(row,col), -getv(row,col2) ])

print len(clauses), "clauses after row constraints"

# Exactly one queen per column
for col in range(n):
	# >= 1
	clauses.append([getv(j, col) for j in range(n)])
	# < 2: if true in one row, not true in all others
	for row in range(n):
		for row2 in range(row+1, n):			
				clauses.append([ -getv(row,col), -getv(row2,col)])

print len(clauses), "clauses after column constraints"

# At most one queen per diagonal; expressed as series of 2-literal clauses (quadratic in N)
# But each will be an easy unit-propagation! Remember that \/ is symmetric.
for row in range(n):
	for col in range(n):
		# All \ (down) excluded if true (row+, col+)		
		for offset in range(1, n-max(row, col)):     # No +1 here since n is already 1-based; Python range is [a,b) interval
			clauses.append([-getv(row,col), -getv(row+offset,col+offset)])
		# All / (down) excluded if true (row+, col-)
		for offset in range(1, min(n-row-1, col)+1): # +1 because no 1-based n to start from			
			clauses.append([-getv(row,col), -getv(row+offset,col-offset)])

print len(clauses), "clauses total"

t1 = time.time()
print "Setup time: ", floor((t1-t0) * 1000), "ms."

#print clauses

filename = 'nq%i.cnf' % n
outf = open(filename, "w")
outf.write('c DIMACS for %i queens\n' % n)
outf.write('c \n')
outf.write('p cnf %i %i\n' % (n*n, len(clauses)))
for c in clauses:
	for lit in c:
		outf.write(str(lit))		
		outf.write(' ')
	outf.write('0\n') # don't forget the terminating zero!
outf.close()

# Solve!
#os.system("~/Downloads/glucose-syrup-4.1/simp/glucose_static -model %s | grep \"^v.*\" > nqout.txt" % filename)
os.system("~/glucose-syrup-4.1/simp/glucose -model %s | grep \"^v.*\" > nqout.txt" % filename)

t2 = time.time()
print "Solving time (Glucose): ", floor((t2-t1) * 1000), "ms."

inf = open('nqout.txt', "r")
lines = inf.readlines()
#print lines
line = lines[0]
inf.close()
lst = line.split()
lst = lst[1:] # starts with v
lst = map(lambda x: int(x), lst) # convert to int
lst = filter(lambda x: x>0, lst) # keep only true variables
lst = map(lambda x: ((x-1) / n, (x-1) % n), lst) # convert to locations on board (0-indexed)
# Note in above, in n=4, var 12 is (2, 3) in 0-indexed, hence the -1 
print "Solution: ",lst

# TODO: will crash if unsatisfiable result, because no model output

# Glucose seems to solve (roughly) n=200 at same speed z3py solves n=40.

# Some Validation

onePerRow = all(any((thisrow == thatrow) 
	                for thatrow in map(lambda tup: tup[0], lst)) 
	            for thisrow in range(n))
print "onePerRow", onePerRow
onePerCol = all(any((thiscol == thatcol) 
	                for thatcol in map(lambda tup: tup[1], lst)) 
	            for thiscol in range(n))
print "onePerCol", onePerCol

# lst.append((2, 5)) #for n=10, should yield false (+). 
# lst.append((0, 3)) #for n=10, should yield false (-). 

# Is there an offset where position is equal to the other plus the offset?
multiPerDiag = any(any((offset != 0 and pos1[0] == pos2[0]+offset and pos1[1] == pos2[1]+offset)
	                   for pos1 in lst for pos2 in lst)
	             for offset in range(-n, n+1))
print "onePerDiag", not(multiPerDiag)