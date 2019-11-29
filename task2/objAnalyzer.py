#!/usr/bin/python3
import sys
import regex as re
import visor
import math
import ObjRE


def normalVector(v1, v2, v3):
	'''
	Returns the normal vector to the triangle defined
	by 3 vertices.

	Takes three 3d vectors indexable starting by cero.
	'''
	A = [v2[0]-v1[0], v2[1]-v1[1], v2[2]-v1[2]]
	B = [v3[0]-v1[0], v3[1]-v1[1], v3[2]-v1[2]]
	N = [A[1]*B[2]-A[2]*B[1],
	     A[2]*B[0]-A[0]*B[2],
	     A[0]*B[1]-A[1]*B[0]]
	norm = math.sqrt(N[0]*N[0]+N[1]*N[1]+N[2]*N[2])
	N[0] /= norm
	N[1] /= norm
	N[2] /= norm
	return N


def processVertex(vertex):
	global verticesHaveWeight
	# Check whether it has the optional weight argument
	# and the rest of vertices do/don't as well
	hasWeight = True if vertex.group('w') else False
	if not vertices:
		# If this is the first vertex, set the format
		verticesHaveWeight = hasWeight
	elif hasWeight != verticesHaveWeight:
		# Otherwise check compliance with previous vertices
		print("All vertices don't follow the same format.", file=sys.stderr)
		sys.exit(-2)

	# If it does have weight, check whether is one
	if hasWeight:
		# Note: There are no precision problems representing 1 as a float
		if not float(vertex.group('w')) == 1.0:
			print("Couldn't parse vertex because weight wasn't 1.0", file=sys.stderr)
			sys.exit(-2)

	# Finally, add it to the list
	vertices.append([float(vertex.group('x')),
	                 float(vertex.group('y')),
	                 float(vertex.group('z'))])


def processVector(vector):
	# Add it to the list
	vectors.append([float(vector.group('i')),
	                float(vector.group('j')),
	                float(vector.group('k'))])


def processTexture(texture):
	global texturesHaveWeight
	# As with vertices, we should check if it has the optional weight argument
	hasWeight = True if texture.group('w') else False
	if not textures:
		texturesHaveWeight = hasWeight
	elif hasWeight != texturesHaveWeight:
		print("All textures don't follow the same format.", file=sys.stderr)
		exit(-2)

	# Add the texture to the list
	textures.append([float(texture.group('u')),
	                 float(texture.group('v'))])


def processFace(face):
	# We must check that this face is a triangle
	# Which means that it doesn't have additional vertices
	if face.group('ExtraTrip'):
		print(
			"Unsupported face geometry. Only triangles are allowed. Face: ", face[0])
		sys.exit(-3)

	# Now we will be working with the face triplets
	triplets = [ObjRE.triplet.fullmatch(face[1]), ObjRE.triplet.fullmatch(
		face[2]), ObjRE.triplet.fullmatch(face[3])]
	# First, add its vertices to the list
	v1, v2, v3 = int(triplets[0][1])-1, int(triplets[1]
									[1])-1, int(triplets[2][1])-1
	faceVertices.append(v1)
	faceVertices.append(v2)
	faceVertices.append(v3)
	# Then, do the same with textures (if present)
	if triplets[0][2]:
		if not triplets[1][2] or not triplets[2][2]:
			print('Incorrect face format: Not all triplets follow the same format.',
					'Face:', face[0])
			sys.exit(-2)
		faceTextures.append(int(triplets[0][2])-1)
		faceTextures.append(int(triplets[1][2])-1)
		faceTextures.append(int(triplets[2][2])-1)
	# Lastly, we add the normal vectors
	if triplets[0][3]:
		if not triplets[1][3] or not triplets[2][3]:
			print('Incorrect face format: Not all triplets follow the same format.',
					'Face:', face[0])
			sys.exit(-3)
		faceVectors.append(int(triplets[0][3])-1)
		faceVectors.append(int(triplets[1][3])-1)
		faceVectors.append(int(triplets[2][3])-1)
	# If they are not present, we should calculate one using the vertices
	else:
		# We will add the normal vector to the triangle to a different list
		# We will merge both list at the end
		extraVectors.append(normalVector(vertices[v1], vertices[v2], vertices[v3]))
		# To know which indices correspond to extra vertices,
		# we'll use negative numbers (starting with index -1
		# to avoid clashing with the first vector)
		faceVectors.append(-len(extraVectors))
		faceVectors.append(-len(extraVectors))
		faceVectors.append(-len(extraVectors))





if __name__ == '__main__':
	# Read input file and perform checks
	name = input('Enter input file (.obj):')
	objFile = re.compile(r'.+\.obj')
	if not objFile.fullmatch(name):
		print('This is not an OBJ file.', file=sys.stderr)
		sys.exit(-1)
	file = open(name, 'r')
	if not file:
		print("Couldn't open", name, file=sys.stderr)
		sys.exit(-1)


	# Data lists for the visualizer
	vertices = []
	vectors = []
	extraVectors = []
	textures = []
	faceVertices = []
	faceVectors = []
	faceTextures = []
	# Format Check variables
	verticesHaveWeight = None
	texturesHaveWeight = None


	# Parsing of commands in file. One command per line.
	for line in file:
		line = ObjRE.trimSpaces(line)
		# Try to parse this line as a vertex command
		vertex = ObjRE.vertex.fullmatch(line)
		vector = ObjRE.vector.fullmatch(line)
		texture = ObjRE.texture.fullmatch(line)
		face = ObjRE.face.fullmatch(line)
		# Have we found a new command?
		if vertex:
			processVertex(vertex)
		elif vector:
			processVector(vector)
		elif texture:
			processTexture(texture)
		elif face:
			processFace(face)
		# else:
		# 	Unparsed line:
		# 	print("Couldn't parse:", line)



	# In the end, we need to assign proper indices to the faces with extra vectors
	for i in range(len(faceVectors)):
		if faceVectors[i] < 0:
			# If the index was -1, now it has to be len(vectors)
			# If it was -2, now it has to be len(vectors)+1
			# etc
			faceVectors[i] = len(vectors)-1-faceVectors[i]


	# With the file parsed, we are ready to display the image
	visor.mostrar(vertices, textures, vectors+extraVectors,
	              faceVertices, faceTextures, faceVectors)
