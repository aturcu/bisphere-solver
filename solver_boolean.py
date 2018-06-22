from z3 import *

num_bispheres = 4

x = 3

y = 3

edges_possible = 2*x*y-x-y

area = x*y

backbone= [[Bool("b_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]

sidechain= [[Bool("s_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]

edges = [Bool("e_%s" % (i+1)) for i in range(edges_possible)]

contacts = [Bool("c_%s" % (i+1)) for i in range(edges_possible)]

constraints_spheres = []

constraints_edges = []

constraints_num_spheres = []

constraints_num_edges = []

constraints_edge_sphere = []

constraints_contacts = []

# each spot can only have one of the following: backbone, sidechain, empty

for i in range(y):
	for j in range(x):
		constraints_spheres.append((Not(And(backbone[i][j], sidechain[i][j]))))


# constraints for edges and contacts

for i in range(edges_possible):
		constraints_edges.append((Not(And(edges[i], contacts[i]))))

# constraints for number of spheres

backbone_spheres = [Int("bb_%s" % (i+1)) for i in range(area)]
sidechain_spheres = [Int("sc_%s" % (i+1)) for i in range(area)]

count = 0

for i in range(y):
	for j in range(x):
		backbone_spheres[count] = If(backbone[i][j], 1, 0)
		sidechain_spheres[count] = If(sidechain[i][j], 1, 0)
		count += 1

constraints_num_spheres.append((Sum(backbone_spheres) == num_bispheres))
constraints_num_spheres.append((Sum(sidechain_spheres) == num_bispheres))


# constraints for number of edges

edge_values = [Int("ee_%s" % (i+1)) for i in range(edges_possible)]

for i in range(edges_possible):
	edge_values[i] = If(edges[i], 1, 0)

constraints_num_edges.append((Sum(edge_values) == num_bispheres))

# contraints for edges and spheres

# need to add constraint that says "cannot have a standalone sidechain or backbone"

edge_count = edges_possible-x+1

for j in range(x-1):
	constraints_edge_sphere.append(Not(And(backbone[y-1][j], backbone[y-1][j+1], edges[edge_count])))
	constraints_edge_sphere.append(Not(And(sidechain[y-1][j], sidechain[y-1][j+1], edges[edge_count])))
	constraints_edge_sphere.append(Not(And(Not(backbone[y-1][j]), Not(sidechain[y-1][j+1]), edges[edge_count])))
	constraints_edge_sphere.append(Not(And(Not(sidechain[y-1][j]), Not(backbone[y-1][j+1]), edges[edge_count])))
	constraints_edge_sphere.append(Not(And(backbone[y-1][j], Not(sidechain[y-1][j+1]), edges[edge_count])))
	constraints_edge_sphere.append(Not(And(Not(backbone[y-1][j]), sidechain[y-1][j+1], edges[edge_count])))
	constraints_edge_sphere.append(Not(And(Not(sidechain[y-1][j]), backbone[y-1][j+1], edges[edge_count])))
	constraints_edge_sphere.append(Not(And(sidechain[y-1][j], Not(backbone[y-1][j+1]), edges[edge_count])))
	edge_count += 1

edge_count = 2*x-2

for i in range(y-1):
	constraints_edge_sphere.append(Not(And(backbone[i][x-1], backbone[i+1][x-1], edges[edge_count])))
	constraints_edge_sphere.append(Not(And(sidechain[i][x-1], sidechain[i+1][x-1], edges[edge_count])))
	constraints_edge_sphere.append(Not(And(Not(backbone[i][x-1]), Not(sidechain[i+1][x-1]), edges[edge_count])))
	constraints_edge_sphere.append(Not(And(Not(sidechain[i][x-1]), Not(backbone[i+1][x-1]), edges[edge_count])))
	constraints_edge_sphere.append(Not(And(backbone[i][x-1], Not(sidechain[i+1][x-1]), edges[edge_count])))
	constraints_edge_sphere.append(Not(And(Not(backbone[i][x-1]), sidechain[i+1][x-1], edges[edge_count])))
	constraints_edge_sphere.append(Not(And(Not(sidechain[i][x-1]), backbone[i+1][x-1], edges[edge_count])))
	constraints_edge_sphere.append(Not(And(sidechain[i][x-1], Not(backbone[i+1][x-1]), edges[edge_count])))
	edge_count += 2*x-1

edge_count = 0

# create constraints for the rest of board by looping through even and odd rows independently


# for i in range(y):
# 	for j in range(x):
# 		if i == 2 and j == 2:
# 			constraints_edge_sphere.append(Xor(And(Not(backbone[i][j]), Not(sidechain[i][j]), Not(edges[i][j])), 
# 										Xor(And(backbone[i][j], sidechain[i-1][j], edges[i][j], edges[i-1][j]), 
# 										And(backbone[i][j], sidechain[i][j-1], edges[i][j], edges[i][j-1])), 
# 										Xor(And(sidechain[i][j], backbone[i-1][j], edges[i][j], edges[i-1][j]), 
# 										And(sidechain[i][j], backbone[i][j-1], edges[i][j], edges[i][j-1]))))
# 		elif i == 2:
# 			constraints_edge_sphere.append(Xor(Xor(And(backbone[i][j], sidechain[i][j+1], edges[i][j], edges[i][j+1]),  
# 										And(sidechain[i][j], backbone[i][j+1], edges[i][j], edges[i][j+1])),
# 										And(Not(backbone[i][j]), Not(sidechain[i][j]), Not(edges[i][j]))))
# 		elif j == 2:
# 			constraints_edge_sphere.append(Xor(Xor(And(backbone[i][j], sidechain[i+1][j], edges[i][j], edges[i+1][j]),  
# 										And(sidechain[i][j], backbone[i+1][j], edges[i][j], edges[i+1][j])),
# 										And(Not(backbone[i][j]), Not(sidechain[i][j]), Not(edges[i][j]))))
# 		else:
# 			constraints_edge_sphere.append(Xor(Xor(And(backbone[i][j], sidechain[i][j+1], edges[i][j], edges[i][j+1]), 
# 										And(backbone[i][j], sidechain[i+1][j], edges[i][j], edges[i+1][j]), 
# 										Xor(And(sidechain[i][j], backbone[i][j+1], edges[i][j], edges[i][j+1]), 
# 										And(sidechain[i][j], backbone[i+1][j], edges[i][j], edges[i+1][j]))), 
# 										And(Not(backbone[i][j]), Not(sidechain[i][j]), Not(edges[i][j]))))

# constraints for contacts

# NEED TO ADD THIS

# make solver and add constraints
s = Solver()

s.add(constraints_spheres)
s.add(constraints_edges)
s.add(constraints_num_spheres)
s.add(constraints_num_edges)
s.add(constraints_edge_sphere) # this does not work, have to fix constraints

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

edge = [ m.evaluate(edges[i]) for i in range(9) ]
print("EDGES")
print_matrix(edge)

cont = [ m.evaluate(contacts[i]) for i in range(9) ]
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