#!/usr/bin/python3
import sys
import regex as re
import visor as visualizer
from math import sqrt


spacesRE = r'\s+'
def separatedTokensRE(*argv):
	first = True
	s = ''
	for arg in argv:
		if not first:
			s += spacesRE
		else:
			first = False
		s += arg
	return s

def groupRE(regExp, name=None):
	if name:
		return '(?P<' + name + r'>' + regExp + ')'
	return '(?:' + regExp + ')'


realRE = r'-?\d+(?:\.\d{1,7})?(?:[eE](?:\+\d+|-0*[1-9]\d*))?'
vertexRE = separatedTokensRE('v', groupRE(realRE, 'x'), groupRE(realRE, 'y'), groupRE(realRE, 'z')) + r'(?:\s*' + realRE + r')?'
vectorRE = separatedTokensRE('vn', groupRE(realRE, 'i'), groupRE(realRE, 'j'), groupRE(realRE, 'k'))
textureRE = separatedTokensRE('vt', groupRE(realRE, 'u'), groupRE(realRE, 'v')) + r'(?:\s*' + realRE + r')?'


rawTripletRE = r'(\d+(?:/\d*)?(?:/\d*)?)'
tripletRE = r'(\d+)(?:/(\d*))?(?:/(\d*))?'
faceRE = separatedTokensRE('f', rawTripletRE, rawTripletRE, rawTripletRE) + '(?P<AdditionalVertices>' + spacesRE + rawTripletRE + ')*'
#'(?P<AdditionalVertices>' + rawTripletRE + '(?:' + spacesRE + rawTripletRE + '))?') 

realCRE = re.compile(realRE)
vertexCRE = re.compile(vertexRE)
vectorCRE = re.compile(vectorRE)
textureCRE = re.compile(textureRE)
tripletCRE = re.compile(tripletRE)
faceCRE = re.compile(faceRE)



def normalVector(v1, v2, v3):
	A = [v2[0]-v1[0], v2[1]-v1[1], v2[2]-v1[2]]
	B = [v3[0]-v1[0], v3[1]-v1[1], v3[2]-v1[2]]
	N = [A[1]*B[2]-A[2]*B[1], A[2]*B[0]-A[0]*B[2], A[0]*B[1]-A[1]*B[0]]
	norm = sqrt(N[0]*N[0]+N[1]*N[1]+N[2]*N[2])
	N[0] /= norm
	N[1] /= norm
	N[2] /= norm
	return N

if __name__ == '__main__':
	name = input('Enter input file (.obj):')
	# TODO Check file type
	file = open(name, 'r')
	vertices = []
	vectors = []
	textures = []
	faceVertices = []
	faceVectors = []
	extraVectors = []
	faceTextures = []
	for line in file:
		vertex = vertexCRE.search(line)
		if vertex:
			x = float(vertex.group('x'))
			y = float(vertex.group('y'))
			z = float(vertex.group('z'))
			#DEBUG print(f'[vertex] x:{x} y:{y} z:{z}')
			vertices.append([x,y,z])
		else:
			vector = vectorCRE.search(line)
		if vector:
			i = float(vector.group('i'))
			j = float(vector.group('j'))
			k = float(vector.group('k'))
			#DEBUG print(f'[vector] i:{i} j:{j} k:{k}')
			vectors.append([i,j,k])
		else:
			texture = textureCRE.search(line)
		if texture:
			u = float(texture.group('u'))
			v = float(texture.group('v'))
			#DEBUG print(f'[texture vector] u:{u} v:{v}')
			textures.append([u,v])
		else:
			face = faceCRE.search(line)
		if face:
			triplet1 = tripletCRE.fullmatch(face[1])
			triplet2 = tripletCRE.fullmatch(face[2])
			triplet3 = tripletCRE.fullmatch(face[3])
			#DEBUG print('[face] %s' %(face.group(0)))
			v1 = int(triplet1[1])-1
			v2 = int(triplet2[1])-1
			v3 = int(triplet3[1])-1
			faceVertices.append(v1)
			faceVertices.append(v2)
			faceVertices.append(v3)
			if triplet1[2]:
				# TODO check triplet2[2] and triplet3[2]
				faceTextures.append(int(triplet1[2])-1)
				faceTextures.append(int(triplet2[2])-1)
				faceTextures.append(int(triplet3[2])-1)
			if triplet1[3]:
				# TODO check triplet2[2] and triplet3[2]
				faceVectors.append(int(triplet1[3])-1)
				faceVectors.append(int(triplet2[3])-1)
				faceVectors.append(int(triplet3[3])-1)
			else:
				extraVectors.append(normalVector(vertices[v1], vertices[v2], vertices[v3]))
				faceVectors.append(-len(extraVectors))
				faceVectors.append(-len(extraVectors))
				faceVectors.append(-len(extraVectors))

	for i in range(len(faceVectors)):
		if faceVectors[i] < 0:
			faceVectors[i] = len(vectors)-1-faceVectors[i]
	
	for id in faceVectors:
		if id < 0:
			print(id)
	
	visualizer.mostrar(vertices, textures, vectors+extraVectors, faceVertices, faceTextures, faceVectors)


