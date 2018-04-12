from z3 import *

num_bispheres = 4

backbone= [[Int("b_%s_%s" % (i+1, j+1)) for j in range(3)] for i in range(3)]

sidechain= [[Int("s_%s_%s" % (i+1, j+1)) for j in range(3)] for i in range(3)]

edges = [[Int("e_%s_%s" % (i+1, j+1)) for j in range(3)] for i in range(3)]

contacts = [[Int("c_%s_%s" % (i+1, j+1)) for j in range(3)] for i in range(3)]

constraints_spheres = []

constraints_edges = []

constraints_edge_sphere = []

constraints_contacts = []

# each spot can only have one of the following: backbone, sidechain, empty

for i in range(3):
	for j in range(3):
		constraints_spheres.append((Or(backbone[i][j] == 1, backbone[i][j] == 0)))
		constraints_spheres.append((Or(sidechain[i][j] == 1, sidechain[i][j] == 0)))
		constraints_spheres.append((backbone[i][j] + sidechain[i][j] <= 1))

# constraints for edges and contacts

for i in range(3):
	for j in range(3):
		constraints_edges.append((Or(edges[i][j] == 1, edges[i][j] == 0)))
		constraints_edges.append((Or(contacts[i][j] == 1, contacts[i][j] == 0)))

# constraints for number of spheres

backbone_spheres = [Int("bb_%s" % (i+1)) for i in range(9)]
sidechain_spheres = [Int("sc_%s" % (i+1)) for i in range(9)]

count = 0

for i in range(3):
	for j in range(3):
		backbone_spheres[count] = backbone[i][j]
		sidechain_spheres[count] = sidechain[i][j]
		count += 1

constraints_num_spheres = []

constraints_num_spheres.append((Sum(backbone_spheres) == num_bispheres))
constraints_num_spheres.append((Sum(sidechain_spheres) == num_bispheres))

# contraints for edges and spheres

for i in range(3):
	for j in range(3):
		if i == 2 and j == 2:
			constraints_edge_sphere.append(Xor(And(backbone[i][j] == 0, sidechain[i][j] == 0, edges[i][j] == 0), 
										Xor(And(backbone[i][j] == 1, sidechain[i-1][j] == 1, edges[i][j] == 1, edges[i-1][j] == 1), 
										And(backbone[i][j] == 1, sidechain[i][j-1] == 1, edges[i][j] == 1, edges[i][j-1] == 1)), 
										Xor(And(sidechain[i][j] == 1, backbone[i-1][j] == 1, edges[i][j] == 1, edges[i-1][j] == 1), 
										And(sidechain[i][j] == 1, backbone[i][j-1] == 1, edges[i][j] == 1, edges[i][j-1] == 1))))
		elif i == 2:
			constraints_edge_sphere.append(Xor(Xor(And(backbone[i][j] == 1, sidechain[i][j+1] == 1, edges[i][j] == 1, edges[i][j+1] == 1),  
										And(sidechain[i][j] == 1, backbone[i][j+1] == 1, edges[i][j] == 1, edges[i][j+1] == 1)),
										And(backbone[i][j] == 0, sidechain[i][j] == 0, edges[i][j] == 0)))
		elif j == 2:
			constraints_edge_sphere.append(Xor(Xor(And(backbone[i][j] == 1, sidechain[i+1][j] == 1, edges[i][j] == 1, edges[i+1][j] == 1),  
										And(sidechain[i][j] == 1, backbone[i+1][j] == 1, edges[i][j] == 1, edges[i+1][j] == 1)),
										And(backbone[i][j] == 0, sidechain[i][j] == 0, edges[i][j] == 0)))
		else:
			constraints_edge_sphere.append(Xor(Xor(And(backbone[i][j] == 1, sidechain[i][j+1] == 1, edges[i][j] == 1, edges[i][j+1] == 1), 
										And(backbone[i][j] == 1, sidechain[i+1][j] == 1, edges[i][j] == 1, edges[i+1][j] == 1), 
										Xor(And(sidechain[i][j] == 1, backbone[i][j+1] == 1, edges[i][j] == 1, edges[i][j+1] == 1), 
										And(sidechain[i][j] == 1, backbone[i+1][j] == 1, edges[i][j] == 1, edges[i+1][j] == 1))), 
										And(backbone[i][j] == 0, sidechain[i][j] == 0, edges[i][j] == 0)))

# constraints for contacts

# NEED TO ADD THIS

# make solver and add constraints
s = Solver()

s.add(constraints_spheres)
s.add(constraints_edges)
s.add(constraints_num_spheres)
# s.add(constraints_edge_sphere) # this does not work, have to fix constraints

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

edge = [ [ m.evaluate(edges[i][j]) for j in range(3) ] for i in range(3) ]
print("EDGES")
print_matrix(edge)

cont = [ [ m.evaluate(contacts[i][j]) for j in range(3) ] for i in range(3) ]
print("CONTACTS")
print_matrix(cont)

for i in range(3):
	print
	for j in range(3):
		if back[i][j] == 1:
			print(" b "),
		elif side[i][j] == 1:
			print(" s "),
		else:
			print(" e "),

