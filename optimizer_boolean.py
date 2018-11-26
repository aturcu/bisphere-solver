from z3 import *
import math
import sys
import time

def optimize(num_bispheres, v, h, p):
	y = 4 if num_bispheres <= 4 else int(math.ceil(float(num_bispheres)/2) + 1)
	x = 4 if num_bispheres <= 4 else int(math.ceil(float(num_bispheres)/2) + 1)

	if num_bispheres == 1:
		print("Number of bispheres must be greater than 1")
		sys.exit()

	# calculates how many edges are possible on grid, and the area of the grid 
	edges_possible = 2*x*y-x-y
	area = x*y

	# writes the dimensions of the board to a file
	dimensions = open("board_dimensions.txt", "w")
	dimensions.write(str(y) + ", " + str(x))
	dimensions.close()

	# opens files that will hold whether or not there is a backbone, sidechain, edge, or contact at positions on the board
	backbone_file = open("backbone.txt", "w")
	sidechain_file = open("sidechain.txt", "w")
	edges_file = open("edges.txt", "w")
	contacts_file = open("contacts.txt", "w")

	# Boolean variable matrices that will hold whether there is a backbone, sidechain, edge, or contact at a spot
	backbone= [[Bool("b_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]
	sidechain= [[Bool("s_%s_%s" % (i+1, j+1)) for j in range(x)] for i in range(y)]
	edges = [Bool("e_%s" % (i+1)) for i in range(edges_possible)]
	contacts = [Bool("c_%s" % (i+1)) for i in range(edges_possible)]

	# lists that will hold constraints to be given to solver
	constraints_spheres = []
	constraints_edges = []
	constraints_num_spheres = []
	constraints_num_edges = []
	constraints_edge_sphere = []
	constraints_contacts = []
	constraints_v_backbone = []
	constraints_v_sidechain = []
	constraints_h_backbone = []
	constraints_h_sidechain = []
	constraints_packing = []

	# dictionaries that map edge number to grid coordinate, coordinate to edge numbers, and a string version of a coordinate to a coordinate
	edges_to_coords = {}
	coords_to_edges = {}
	coords_string_to_coords = {}

	# filling dictionaries

	edge_count = 0

	for i in range(y):
		for j in range(x-1):
			coordinate1 = []
			coordinate2 = []
			coordinate1.append(i)
			coordinate1.append(j)
			coordinate2.append(i)
			coordinate2.append(j+1)
			coordinate_pair = []
			coordinate_pair.append(coordinate1)
			coordinate_pair.append(coordinate2)
			edges_to_coords[edge_count] = coordinate_pair
			edge_count += 1
		if i < y-1:
			for j in range(x):
				coordinate1 = []
				coordinate2 = []
				coordinate1.append(i)
				coordinate1.append(j)
				coordinate2.append(i+1)
				coordinate2.append(j)
				coordinate_pair = []
				coordinate_pair.append(coordinate1)
				coordinate_pair.append(coordinate2)
				edges_to_coords[edge_count] = coordinate_pair
				edge_count += 1

	for edge, coordinate_pair in edges_to_coords.items():
		for coordinate in coordinate_pair:
			if not str(coordinate) in coords_to_edges.keys():
				coords_to_edges[str(coordinate)] = []
				coords_string_to_coords[str(coordinate)] = coordinate
			coords_to_edges[str(coordinate)].append(edge)

	# each spot can only have one of the following: backbone, sidechain, empty

	for i in range(y):
		for j in range(x):
			constraints_spheres.append((Not(And(backbone[i][j], sidechain[i][j]))))


	# cannot have an edge and a contact in the same spot

	for i in range(edges_possible):
			constraints_edges.append((Not(And(edges[i], contacts[i]))))

	# must have a number of backbone spheres and sidechain spheres equal to the number of bispheres

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


	# number of edges must be equal to the number of bispheres

	edge_values = [Int("ee_%s" % (i+1)) for i in range(edges_possible)]

	for i in range(edges_possible):
		edge_values[i] = If(edges[i], 1, 0)

	constraints_num_edges.append((Sum(edge_values) == num_bispheres))

	# contraints for relationship between edges and spheres

	for coordinate_string, coordinate in coords_string_to_coords.items():

		edge_list = coords_to_edges[coordinate_string]
		y1 = coordinate[0]
		x1 = coordinate[1]

		for edge in edge_list:
			edge_coords = edges_to_coords[edge]
			list_coords = list(edge_coords)
			list_coords.remove(coordinate)
			other_coordinate = list_coords[0]
			y2 = other_coordinate[0]
			x2 = other_coordinate[1]

			# if connected spheres, must be one backbone and one sidechain

			constraints_edge_sphere.append(Not(And(backbone[y1][x1], backbone[y2][x2], edges[edge])))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], sidechain[y2][x2], edges[edge])))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], Not(sidechain[y2][x2]), edges[edge])))
			constraints_edge_sphere.append(Not(And(Not(backbone[y1][x1]), sidechain[y2][x2], edges[edge])))
			constraints_edge_sphere.append(Not(And(Not(sidechain[y1][x1]), backbone[y2][x2], edges[edge])))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], Not(backbone[y2][x2]), edges[edge])))

		# cannot have a standalone backbone or sidechain, and no more than one edge per sphere

		if len(edge_list) == 2:
			edge1 = edge_list[0]
			edge2 = edge_list[1]
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], Not(edges[edge1]), Not(edges[edge2]))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], Not(edges[edge1]), Not(edges[edge2]))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], edges[edge1], edges[edge2])))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], edges[edge1], edges[edge2])))

		elif len(edge_list) == 3:
			edge1 = edge_list[0]
			edge2 = edge_list[1]
			edge3 = edge_list[2]
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], Not(edges[edge1]), And(Not(edges[edge2]), Not(edges[edge3])))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], Not(edges[edge1]), And(Not(edges[edge2]), Not(edges[edge3])))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], edges[edge1], And(edges[edge2]), Not(edges[edge3]))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], edges[edge1], And(Not(edges[edge2]), edges[edge3]))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], Not(edges[edge1]), And(edges[edge2], edges[edge3]))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], edges[edge1], And(edges[edge2], edges[edge3]))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], edges[edge1], And(edges[edge2]), Not(edges[edge3]))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], edges[edge1], And(Not(edges[edge2]), edges[edge3]))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], Not(edges[edge1]), And(edges[edge2], edges[edge3]))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], edges[edge1], And(edges[edge2], edges[edge3]))))
		
		else:
			edge1 = edge_list[0]
			edge2 = edge_list[1]
			edge3 = edge_list[2]
			edge4 = edge_list[3]
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], Not(edges[edge1]), And(Not(edges[edge2]), Not(edges[edge3]), Not(edges[edge4])))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], Not(edges[edge1]), And(Not(edges[edge2]), Not(edges[edge3]), Not(edges[edge4])))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], Not(edges[edge1]), And(edges[edge2], edges[edge3], edges[edge4]))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], edges[edge1], And(Not(edges[edge2]), edges[edge3], edges[edge4]))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], edges[edge1], And(edges[edge2], Not(edges[edge3]), edges[edge4]))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], edges[edge1], And(edges[edge2], edges[edge3], Not(edges[edge4])))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], Not(edges[edge1]), And(Not(edges[edge2]), edges[edge3], edges[edge4]))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], Not(edges[edge1]), And(edges[edge2], Not(edges[edge3]), edges[edge4]))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], Not(edges[edge1]), And(edges[edge2], edges[edge3], Not(edges[edge4])))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], edges[edge1], And(Not(edges[edge2]), Not(edges[edge3]), edges[edge4]))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], edges[edge1], And(Not(edges[edge2]), edges[edge3], Not(edges[edge4])))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], edges[edge1]), And(edges[edge2], Not(edges[edge3], Not(edges[edge4])))))
			constraints_edge_sphere.append(Not(And(backbone[y1][x1], edges[edge1]), And(edges[edge2], edges[edge3], edges[edge4])))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], Not(edges[edge1]), And(edges[edge2], edges[edge3], edges[edge4]))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], edges[edge1], And(Not(edges[edge2]), edges[edge3], edges[edge4]))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], edges[edge1], And(edges[edge2], Not(edges[edge3]), edges[edge4]))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], edges[edge1], And(edges[edge2], edges[edge3], Not(edges[edge4])))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], Not(edges[edge1]), And(Not(edges[edge2]), edges[edge3], edges[edge4]))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], Not(edges[edge1]), And(edges[edge2], Not(edges[edge3]), edges[edge4]))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], Not(edges[edge1]), And(edges[edge2], edges[edge3], Not(edges[edge4])))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], edges[edge1], And(Not(edges[edge2]), Not(edges[edge3]), edges[edge4]))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], edges[edge1], And(Not(edges[edge2]), edges[edge3], Not(edges[edge4])))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], edges[edge1]), And(edges[edge2], Not(edges[edge3], Not(edges[edge4])))))
			constraints_edge_sphere.append(Not(And(sidechain[y1][x1], edges[edge1]), And(edges[edge2], edges[edge3], edges[edge4])))

	# two sidechains next to each other is a contact

	edge_count = 0

	for i in range(y):
		for j in range(x-1):
			constraints_contacts.append(Not(And(sidechain[i][j], sidechain[i][j+1], Not(contacts[edge_count]))))
			constraints_contacts.append(Not(And(Not(sidechain[i][j]), sidechain[i][j+1], contacts[edge_count])))
			constraints_contacts.append(Not(And(sidechain[i][j], Not(sidechain[i][j+1]), contacts[edge_count])))
			constraints_contacts.append(Not(And(Not(sidechain[i][j]), Not(sidechain[i][j+1]), contacts[edge_count])))
			edge_count += 1
		if i < y-1:
			for j in range(x):
				constraints_contacts.append(Not(And(sidechain[i][j], sidechain[i+1][j], Not(contacts[edge_count]))))
				constraints_contacts.append(Not(And(Not(sidechain[i][j]), sidechain[i+1][j], contacts[edge_count])))
				constraints_contacts.append(Not(And(sidechain[i][j], Not(sidechain[i+1][j]), contacts[edge_count])))
				constraints_contacts.append(Not(And(Not(sidechain[i][j]), Not(sidechain[i+1][j]), contacts[edge_count])))
				edge_count += 1

	# constraints for counting contacts (try making a board with 0 contacts, then 1, then 2, etc. until it is no longer possible)

	contact_values = [Int("ee_%s" % (i+1)) for i in range(edges_possible)]

	for i in range(edges_possible):
		contact_values[i] = If(contacts[i], 1, 0)

	# Breaking vertical symmetry using lex leader
	if v:

		# stores vertical symmetries
		v_sym = {}

		for i in range(y):
			for j in range(x):
				v_sym[i,j] = [y-i-1, j]

		# Holds previous equalities for lex leader
		v_prev_backbone = []
		v_prev_sidechain = []

		index = 0

		# adds first equality for lex leader
		v_prev_backbone.append(backbone[0][0] == backbone[v_sym[0,0][0]][v_sym[0,0][1]])
		v_prev_sidechain.append(sidechain[0][0] == sidechain[v_sym[0,0][0]][v_sym[0,0][1]])

		# adds first implication to the constraints
		constraints_v_backbone.append(Implies(backbone[0][0], backbone[v_sym[0,0][0]][v_sym[0,0][1]]))
		constraints_v_sidechain.append(Implies(sidechain[0][0], sidechain[v_sym[0,0][0]][v_sym[0,0][1]]))

		for i in range(y/2):
			for j in range(x):
				if i == 0 and j == 0: 
					continue 

				# according to lex leader format, adds an implication to the constraints using stored equalities and symmetries
				constraints_v_backbone.append(Implies(v_prev_backbone[index], Implies(backbone[i][j], backbone[v_sym[i,j][0]][v_sym[i,j][1]])))
				constraints_v_sidechain.append(Implies(v_prev_sidechain[index], Implies(sidechain[i][j], sidechain[v_sym[i,j][0]][v_sym[i,j][1]])))

				# extends the equality list for lex leader
				v_prev_backbone.append(And(v_prev_backbone[index], backbone[i][j] == backbone[v_sym[i,j][0]][v_sym[i,j][1]]))
				v_prev_sidechain.append(And(v_prev_sidechain[index], sidechain[i][j] == sidechain[v_sym[i,j][0]][v_sym[i,j][1]]))
				index += 1

	# Breaking horizontal symmetry using lex leader
	if h:

		# stores horizontal symmetries
		h_sym = {}

		for i in range(y):
			for j in range(x):
				h_sym[i,j] = [i, x-j-1]

		# Holds previous equalities for lex leader
		h_prev_backbone = []
		h_prev_sidechain = []

		index = 0

		# adds first equality for lex leader
		h_prev_backbone.append(backbone[0][0] == backbone[h_sym[0,0][0]][h_sym[0,0][1]])
		h_prev_sidechain.append(sidechain[0][0] == sidechain[h_sym[0,0][0]][h_sym[0,0][1]])

		# adds first implication to the constraints
		constraints_h_backbone.append(Implies(backbone[0][0], backbone[h_sym[0,0][0]][h_sym[0,0][1]]))
		constraints_h_sidechain.append(Implies(sidechain[0][0], sidechain[h_sym[0,0][0]][h_sym[0,0][1]]))

		for i in range(y):
			for j in range(x/2):
				if i == 0 and j == 0: 
					continue

				# according to lex leader format, adds an implication to the constraints using stored equalities and symmetries
				constraints_h_backbone.append(Implies(h_prev_backbone[index], Implies(backbone[i][j], backbone[h_sym[i,j][0]][h_sym[i,j][1]])))
				constraints_h_sidechain.append(Implies(h_prev_sidechain[index], Implies(sidechain[i][j], sidechain[h_sym[i,j][0]][h_sym[i,j][1]])))

				# extends the equality list for lex leader
				h_prev_backbone.append(And(h_prev_backbone[index], backbone[i][j] == backbone[h_sym[i,j][0]][h_sym[i,j][1]]))
				h_prev_sidechain.append(And(h_prev_sidechain[index], sidechain[i][j] == sidechain[h_sym[i,j][0]][h_sym[i,j][1]]))
				index += 1

	# Breaking corner packing symmetry
	if p:

		# ensures that there is at least one bisphere in some row and some column (depending on symmetry breaking chosen)
		col = [Int("fr_%s" % (i+1)) for i in range(y)]
		row = [Int("fc_%s" % (i+1)) for i in range(x)]

		count = 0

		for i in range(y):
				col[count] = If(Or(backbone[i][0], sidechain[i][0]), 1, 0)
				count += 1

		count = 0

		for i in range(x):
				row[count] = If(Or(backbone[0][i], sidechain[0][i]), 1, 0)
				count += 1

		constraints_packing.append((Sum(col) > 0))
		constraints_packing.append((Sum(row) > 0))


	# make solver, add constraints, and maximize contacts (max number is the last number of contacts that could be made)

	s = Optimize()
	s.add(constraints_spheres)
	s.add(constraints_edges)
	s.add(constraints_num_spheres)
	s.add(constraints_num_edges)
	s.add(constraints_edge_sphere)
	s.add(constraints_contacts)
	s.add(constraints_v_backbone)
	s.add(constraints_v_sidechain)
	s.add(constraints_h_backbone)
	s.add(constraints_h_sidechain)
	s.add(constraints_packing)

 	start = time.time()
	optimize = s.maximize(Sum(contact_values))
	print(s.check())
	elapsed = time.time() - start
	print(elapsed)

	max_contacts = s.upper(optimize)

	print("Maximum number of contacts: " + str(max_contacts))

	m = s.model()

	# print matrix values that satisfy model

	back = [[m.evaluate(backbone[i][j]) for j in range(x)] for i in range(y)]

	side = [[m.evaluate(sidechain[i][j]) for j in range(x)] for i in range(y)]

	edge = [m.evaluate(edges[i]) for i in range(edges_possible)]

	cont = [m.evaluate(contacts[i]) for i in range(edges_possible)]

	# translate matrices into backbone, sidechain, and empty spots and print these

	for i in range(y):
		print
		for j in range(x):
			if back[i][j] == True:
				print(" b "),
			elif side[i][j] == True:
				print(" s "),
			else:
				print(" e "),

	# write solution matrices to output files

	for i in range(y-1):
		backbone_file.write(str(back[i]).strip('[').strip(']') + ", \n")
		sidechain_file.write(str(side[i]).strip('[').strip(']') + ", \n")

	backbone_file.write(str(back[y-1]).strip('[').strip(']'))
	sidechain_file.write(str(side[y-1]).strip('[').strip(']'))

	edges_file.write(str(edge).strip('[').strip(']'))
	contacts_file.write(str(cont).strip('[').strip(']'))

	# close output files

	backbone_file.close()
	sidechain_file.close()
	edges_file.close()
	contacts_file.close()

if __name__ == '__main__':
	# prompts user for number of bispheres
	num_bispheres = input("Number of bispheres: ")
	print("\nNo symmetry breaking...")
	optimize(num_bispheres, False, False, False)
	print("\nOnly vertical symmetry breaking...")
	optimize(num_bispheres, True, False, False)
	print("\nOnly horizontal symmetry breaking...")
	optimize(num_bispheres, False, True, False)
	print("\nOnly corner packing symmetry breaking...")
	optimize(num_bispheres, False, False, True)
	print("\nVertical and horizontal symmetry breaking...")
	optimize(num_bispheres, True, True, False)

	# Notes: cannot yet implement corner packing with vertical or horizontal symmetry breaking. 
	# Corner packing seems to slow down the program considerably. The effect of vertical and 
	# horizontal breaking varies (sometimes improves performance but sometimes slows it down, not
	# sure why this is).


