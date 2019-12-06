#!/usr/bin/python3

'''TextFormatter interactor to process a file.'''

import regex as re
import sys
import TextFormatter


fileNameCRE = re.compile(r'(.+)\.txt')

if __name__ == '__main__':
	while True:
		name = input('Introduce la ruta a un fichero:')

		basename = fileNameCRE.fullmatch(name)
		if not basename:
			print('Debes introducir un fichero con extensión .txt')
			continue
		try:
			inputF = open(name)
		except IOError:
			print('No existe el fichero o no se pudo abrir.')
			continue

		try:
			outputF = open(basename[1] + '_g.txt', mode='w')
		except IOError:
			print(f"No se pudo crear el fichero de salida '{basename[1]}_g.txt'.")
			sys.exit(-1)
		
		break

	while True:
		try:
			lineLen = int(input('Introduce la longitud de línea(mínimo 10 caracteres por línea):'))
			txtForm = TextFormatter.SpanishFormatter(lineLen)
		except ValueError:
			print('Tamaño de línea no válido')
			continue
		break


	for line in inputF:
		# Supress empty lines
		if re.fullmatch(r'\s*', line):
			continue
		txtForm.processLine(line, file=outputF)
	
