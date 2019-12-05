#!/usr/bin/python3

'''
ObjRE defines and precompiles the regular expresions needed to parse an OBJ file.
ObjRE utiliza el módulo regex 

@author Emilio Domínguez Sánchez y José Manuel Ruiz Ródenas
@title ObjRE
'''

import regex as re


SPACES = r'\s+'


def separatedTokensRE(*argv):
	'''
	Returns a regular expresion that accepts multiple regular
	expressions separated by spaces.
	'''
	first = True
	s = ''
	for arg in argv:
		if not first:
			s += SPACES
		else:
			first = False
		s += arg
	return s


def groupRE(regExp, name=None):
	'''
	Groups a regular expression. You can also specify a name
	for the group.
	'''
	if name is None:
		return '(?:' + regExp + ')'
	return '(?P<' + name + r'>' + regExp + ')'


def optGroupRE(regExp, name=None):
	'''
	Groups an additional optional expresion separated by spaces.
	You can also specify a name for the group.
	'''
	return '(?:' + SPACES + groupRE(regExp, name) + ')?'



# Regular expressions.
REAL        = r'-?\d+(?:\.\d{1,9})?(?:[eE](?:\+\d+|-0*[1-9]\d*))?'
RAW_TRIPLET = r'(\d+(?:/\d*)?(?:/\d*)?)'
TRIPLET     = r'(\d+)(?:/(\d*))?(?:/(\d*))?'
VERTEX  = (separatedTokensRE('v',
                             groupRE(REAL, 'x'),
                             groupRE(REAL, 'y'),
                             groupRE(REAL, 'z'))
           + optGroupRE(REAL, 'w'))

VECTOR  =  separatedTokensRE('vn',
                             groupRE(REAL, 'i'),
                             groupRE(REAL, 'j'),
                             groupRE(REAL, 'k'))

TEXTURE = (separatedTokensRE('vt',
                             groupRE(REAL, 'u'),
                             groupRE(REAL, 'v'))
           + optGroupRE(REAL, 'w'))

FACE    = (separatedTokensRE('f',
                             RAW_TRIPLET,
                             RAW_TRIPLET,
                             RAW_TRIPLET)
           + r'(?P<ExtraTrip>'
           + SPACES
           + RAW_TRIPLET
           + r')*')


# Compilation of regular expressions
real = re.compile(REAL)
vertex = re.compile(VERTEX)
vector = re.compile(VECTOR)
texture = re.compile(TEXTURE)
triplet = re.compile(TRIPLET)
face = re.compile(FACE)
trim = re.compile(r'\s*(.*?)\s*')


def trimSpaces(string):
	'''
	Trims leading and trailing whitespace from a string.
	'''
	return trim.fullmatch(string)[1]
