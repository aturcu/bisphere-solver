from z3 import *

num_bispheres = input("Number of bispheres: ")

y = input("Number of rows: ")

x = input("Number of columns ")

edges_possible = 2*x*y-x-y

area = x*y

backbone= [[Bool("b_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]

sidechain= [[Bool("s_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]

edges_u = [[Bool("eu_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]

edges_d = [[Bool("ed_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]

edges_l = [[Bool("el_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]

edges_r = [[Bool("er_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]

contacts_u = [[Bool("cu_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]

contacts_d = [[Bool("cd_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]

contacts_l = [[Bool("cl_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]

contacts_r = [[Bool("cr_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]

constraints_spheres = []

constraints_edges = []

constraints_num_spheres = []

constraints_num_edges = []

constraints_edge_sphere = []

# each spot can only have one of the following: backbone, sidechain, empty

for i in range(y):
	for j in range(x):
		constraints_spheres.append((Not(And(backbone[i][j], sidechain[i][j]))))


# constraints for edges and contacts

for i in range(y):
	for j in range(x):
		constraints_edges.append((Xor(edges_u[i][j], edges_d[i][j], Xor(edges_l[i][j], edges_r[i][j]))))
		constraints_edges.append((Xor(contacts_u[i][j], contacts_d[i][j], Xor(contacts_l[i][j], contacts_r[i][j]))))

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

edge_values = [Int("e_%s" % (i+1)) for i in range(edges_possible)]

count = 0

for i in range(y):
	for j in range(x):
		edge_values[count] = If(edges_u[i][j], 1, 0) + If(edges_d[i][j], 1, 0) + If(edges_l[i][j], 1, 0) + If(edges_r[i][j], 1, 0)
		count += 1

constraints_num_edges.append((Sum(edge_values) == 2 * num_bispheres))

# contraints for edges and spheres

# need to add constraint that says "cannot have a standalone sidechain or backbone"

# constraints for contacts

contact_values = [Int("c_%s" % (i+1)) for i in range(edges_possible)]

count = 0

for i in range(y):
	for j in range(x):
		contact_values[count] = If(contacts_u[i][j], 1, 0) + If(contacts_d[i][j], 1, 0) + If(contacts_l[i][j], 1, 0) + If(contacts_r[i][j], 1, 0)
		count += 1

constraints_num_edges.append((Sum(edge_values) == num_bispheres))

# make solver, add constraints, and maximize contacts

s = Solver()

s.check()

m = s.model()

for i in range(x*y):

	s.add(constraints_spheres)
	s.add(constraints_edges)
	s.add(constraints_num_spheres)
	s.add(constraints_num_edges)
	s.add(constraints_edge_sphere)
	s.add((Sum(contact_values) == i))

	if (str(s.check()) == "unsat"):
		print("Maximum number of contacts: " + str(i-1))
		break

	else:
		m = s.model()
		s = Solver()

# print matrix values that satisfy model

back = [ [ m.evaluate(backbone[i][j]) for j in range(x) ] for i in range(y) ]
print("BACKBONE")
print_matrix(back)

side = [ [ m.evaluate(sidechain[i][j]) for j in range(x) ] for i in range(y) ]
print("SIDECHAIN")
print_matrix(side)

edge_u = [ [ m.evaluate(edges_u[i][j]) for j in range(x) ] for i in range(y) ]
print("EDGES UP")
print_matrix(edge_u)

edge_d = [ [ m.evaluate(edges_d[i][j]) for j in range(x) ] for i in range(y) ]
print("EDGES DOWN")
print_matrix(edge_d)

edge_l = [ [ m.evaluate(edges_l[i][j]) for j in range(x) ] for i in range(y) ]
print("EDGES LEFT")
print_matrix(edge_l)

edge_r = [ [ m.evaluate(edges_r[i][j]) for j in range(x) ] for i in range(y) ]
print("EDGES RIGHT")
print_matrix(edge_r)

cont_u = [ [ m.evaluate(contacts_u[i][j]) for j in range(x) ] for i in range(y) ]
print("CONTACTS UP")
print_matrix(cont_u)

cont_d = [ [ m.evaluate(contacts_d[i][j]) for j in range(x) ] for i in range(y) ]
print("CONTACTS DOWN")
print_matrix(cont_d)

cont_l = [ [ m.evaluate(contacts_l[i][j]) for j in range(x) ] for i in range(y) ]
print("CONTACTS LEFT")
print_matrix(cont_l)

cont_r = [ [ m.evaluate(contacts_r[i][j]) for j in range(x) ] for i in range(y) ]
print("CONTACTS RIGHT")
print_matrix(cont_r)

for i in range(y):
	print
	for j in range(x):
		if back[i][j] == True:
			print(" b "),
		elif side[i][j] == True:
			print(" s "),
		else:
			print(" e "),