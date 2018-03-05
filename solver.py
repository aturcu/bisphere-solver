from z3 import *

num_bispheres = 4

backbone = [[Int("b_%s_%s" % (i+1, j+1)) for j in range(3)] for i in range(3)]

sidechain = [[Int("s_%s_%s" % (i+1, j+1)) for j in range(3)] for i in range(3)]

empty = [[Int("n_%s_%s" % (i+1, j+1)) for j in range(3)] for i in range(3)]

edges = [Int("e_%s" % (i+1)) for i in range(12)]

contacts = [Int("c_%s" % (i+1)) for i in range(12)] 

constraints_spheres = []

constraints_edges = []

constraints_num_spheres = []

constraints_num_edges = []

# each spot can only have one of the following: backbone, sidechain, empty
for i in range(3):
	for j in range(3):
		constraints_spheres.append((backbone[i][j] + sidechain[i][j] + empty[i][j] <= 1))

# constraints for edges: can have an edge, a contact, or neither (but not both)
for i in range(12):
	constraints_edges.append((edges[i] + contacts[i] <= 1))

# constraints for number of spheres 
backbone_spheres = []
sidechain_spheres = []

for i in range(3):
	for j in range(3):
		backbone_spheres.append(backbone[i][j])
		sidechain.append(sidechain[i][j])

# 3 lines below do not work, have to look into it more

# constraints_num_spheres = []

# constraints_num_spheres.append([Sum(backbone_spheres) == num_bispheres])
# constraints_num_spheres.append([Sum(sidechain_spheres) == num_bispheres])

# constraints for number of edges
constraints_num_edges.append(Sum(edges) == num_bispheres)
for i in range(12):
	constraints_num_edges.append(edges[i] <= 1)

# constraints for contacts 

# NEED TO ADD THIS

# make solver and add constraints
s = Solver()

s.add(constraints_spheres)
s.add(constraints_edges)
# s.add(constraints_num_spheres) # z3 does not like how this constraint is generated, not sure why
s.add(constraints_num_edges)

print (s.check())

# output model
m = s.model()

# print matrix values that satisfy model

back = [ [ m.evaluate(backbone[i][j]) for j in range(3) ] for i in range(3) ]
print("BACKBONE")
print_matrix(back)

side = [ [ m.evaluate(sidechain[i][j]) for j in range(3) ] for i in range(3) ]
print("SIDECHAIN")
print_matrix(side)

empt = [ [ m.evaluate(empty[i][j]) for j in range(3) ] for i in range(3) ]
print("EMPTY")
print_matrix(empt)

edge = [ m.evaluate(edges[i]) for i in range(12)]
print("EDGES")
print_matrix(edge)

cont = [ m.evaluate(contacts[i]) for i in range(12)]
print("CONTACTS")
print_matrix(cont)
