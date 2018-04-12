from z3 import *

num_bispheres = 4

backbone= [[Bool("b_%s_%s" % (i+1, j+1)) for j in range(3)] for i in range(3)]

sidechain= [[Bool("s_%s_%s" % (i+1, j+1)) for j in range(3)] for i in range(3)]

edges = [[Bool("e_%s_%s" % (i+1, j+1)) for j in range(3)] for i in range(3)]

contacts = [[Bool("c_%s_%s" % (i+1, j+1)) for j in range(3)] for i in range(3)]

constraints_spheres = []

constraints_edges = []

constraints_edge_sphere = []

constraints_contacts = []

# each spot can only have one of the following: backbone, sidechain, empty

for i in range(3):
	for j in range(3):
		constraints_spheres.append((Xor(backbone[i][j], sidechain[i][j])))

# constraints for number of spheres

# NEED TO DO THIS USING BOOLEANS?

# backbone_spheres = [Int("bb_%s" % (i+1)) for i in range(9)]
# sidechain_spheres = [Int("sc_%s" % (i+1)) for i in range(9)]

# count = 0

# for i in range(3):
# 	for j in range(3):
# 		backbone_spheres[count] = backbone[i][j]
# 		sidechain_spheres[count] = sidechain[i][j]
# 		count += 1

# constraints_num_spheres = []

# constraints_num_spheres.append((Sum(backbone_spheres) == num_bispheres))
# constraints_num_spheres.append((Sum(sidechain_spheres) == num_bispheres))

# contraints for edges and spheres

for i in range(3):
	for j in range(3):
		if i == 2 and j == 2:
			constraints_edge_sphere.append(Xor(And(Not(backbone[i][j]), Not(sidechain[i][j]), Not(edges[i][j])), 
										Xor(And(backbone[i][j], sidechain[i-1][j], edges[i][j], edges[i-1][j]), 
										And(backbone[i][j], sidechain[i][j-1], edges[i][j], edges[i][j-1])), 
										Xor(And(sidechain[i][j], backbone[i-1][j], edges[i][j], edges[i-1][j]), 
										And(sidechain[i][j], backbone[i][j-1], edges[i][j], edges[i][j-1]))))
		elif i == 2:
			constraints_edge_sphere.append(Xor(Xor(And(backbone[i][j], sidechain[i][j+1], edges[i][j], edges[i][j+1]),  
										And(sidechain[i][j], backbone[i][j+1], edges[i][j], edges[i][j+1])),
										And(Not(backbone[i][j]), Not(sidechain[i][j]), Not(edges[i][j]))))
		elif j == 2:
			constraints_edge_sphere.append(Xor(Xor(And(backbone[i][j], sidechain[i+1][j], edges[i][j], edges[i+1][j]),  
										And(sidechain[i][j], backbone[i+1][j], edges[i][j], edges[i+1][j])),
										And(Not(backbone[i][j]), Not(sidechain[i][j]), Not(edges[i][j]))))
		else:
			constraints_edge_sphere.append(Xor(Xor(And(backbone[i][j], sidechain[i][j+1], edges[i][j], edges[i][j+1]), 
										And(backbone[i][j], sidechain[i+1][j], edges[i][j], edges[i+1][j]), 
										Xor(And(sidechain[i][j], backbone[i][j+1], edges[i][j], edges[i][j+1]), 
										And(sidechain[i][j], backbone[i+1][j], edges[i][j], edges[i+1][j]))), 
										And(Not(backbone[i][j]), Not(sidechain[i][j]), Not(edges[i][j]))))

# constraints for contacts

# NEED TO ADD THIS

# make solver and add constraints
s = Solver()

s.add(constraints_spheres)
# s.add(constraints_num_spheres)
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
		if back[i][j] == True:
			print(" b "),
		elif side[i][j] == True:
			print(" s "),
		else:
			print(" e "),