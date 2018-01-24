import random
import string
# import pyperclip
import numpy as np
import os

def getStartPoint(direction, word, rowDim, colDim):
	if direction == 'N':
		startX = random.randint(0, colDim - 1)
		startY = random.randint(len(word) - 1, rowDim - 1)
	elif direction == 'E':
		startX = random.randint(0, colDim - len(word))
		startY = random.randint(0, rowDim  - 1)
	elif direction == 'S':
		startX = random.randint(0, colDim  - 1)
		startY = random.randint(0, rowDim - len(word))
	elif direction == 'W':
		startX = random.randint(len(word)-1, colDim - 1)
		startY = random.randint(0, rowDim  - 1)
	elif direction == 'NE':
		startX = random.randint(0, colDim - len(word))
		startY = random.randint(len(word) - 1, rowDim - 1)
	elif direction == 'SE':
		startX = random.randint(0, colDim - len(word))
		startY = random.randint(0, rowDim - len(word))
	elif direction == 'SW':
		startX = random.randint(len(word)-1, colDim - 1)
		startY = random.randint(0, rowDim - len(word))
	elif direction == 'NW':
		startX = random.randint(len(word)-1, colDim - 1)
		startY = random.randint(len(word) - 1, rowDim - 1)
	return (startX, startY)

def placeWord(wordScramble, word, direction, startX, startY):
	currentX, currentY = startX, startY
	for letter in word:
		wordScramble[currentY][currentX] = letter
		if 'N' in direction:
			currentY -= 1
		if 'S' in direction:
			currentY += 1
		if 'E' in direction:
			currentX += 1
		if 'W' in direction:
			currentX -= 1
	return wordScramble

def checkWord(wordScramble, word, direction, startX, startY):
	canBePlaced = True
	currentX, currentY = startX, startY
	for letter in word:
		if wordScramble[currentY][currentX] != '!' and wordScramble[currentY][currentX] != letter:
			# print('Error, word cannot be placed.')
			canBePlaced = False
			return canBePlaced
		if 'N' in direction:
			currentY -= 1
		if 'S' in direction:
			currentY += 1
		if 'E' in direction:
			currentX += 1
		if 'W' in direction:
			currentX -= 1
	return canBePlaced

def makeWordSearch(words, rowDim, colDim):
	wordScramble = np.full((rowDim, colDim), '!')
	# wordDict = {'word': word, 'direction': NW, 'startPos' : (x,y)}
	for word in words:
		# convert to uppercase
		word = word.upper()

		canBePlaced = False
		while not canBePlaced:
			direction = random.choice(['N', 'E', 'S', 'W', 'NE', 'SE', 'SW', 'NW'])
			# direction = random.choice(['N', 'E', 'S', 'W'])
			startX, startY = getStartPoint(direction, word, rowDim, colDim)
			canBePlaced = checkWord(wordScramble, word, direction, startX, startY)


		# place word:
		wordScramble = placeWord(wordScramble, word, direction, startX, startY)


	# print(wordScramble)
	# fill in blanks
	alpha = list(string.ascii_uppercase)
	for rowIndex in range(rowDim):
		for colIndex in range(colDim):
			if wordScramble[rowIndex,colIndex] == '!':
				wordScramble[rowIndex,colIndex] = random.choice(alpha)

	# print(wordScramble)
	return wordScramble

def matrixToLatex(wordScramble, colDim):
	introText = '\\begin{center}\n\\renewcommand{\\arraystretch}{1.5}{\n\\noindent\\begin{tabular}{' + 'c'*colDim + '}'

	endText = '''\n\\end{tabular}\n}\n\\end{center}'''
	rows = []
	for row in wordScramble:
		row = ' & '.join(row)
		rows.append(row)
	output = introText
	output += ' \\\\ \n'.join(rows)
	output += endText

	# pyperclip.copy(output)

def matrixToLatexFile(wordScramble, colDim):
	pre_amb = '\\documentclass{standalone}\n\\usepackage{tikz}\n\n\\begin{document}\n'
	endDocText = '\\end{document}'
	introText = '\\begin{center}\n\\renewcommand{\\arraystretch}{1.5}{\n\\noindent\\begin{tabular}{' + 'c'*colDim + '}'

	endText = '''\n\\end{tabular}\n}\n\\end{center}'''
	rows = []
	for row in wordScramble:
		row = ' & '.join(row)
		rows.append(row)
	output = pre_amb
	output += introText
	output += ' \\\\ \n'.join(rows)
	output += endText
	output += endDocText

	os.system('cd wordsearch')
	document_title = 'testout'
	with open(document_title + '.tex', 'w') as f:
		f.write(output)
	os.system('pdflatex -synctex=1 -interaction=nonstopmode {}.tex > /dev/null'.format(document_title))
	os.system('convert -density 300 {}.pdf -quality 90 {}.png'.format(document_title, document_title))
	os.system('convert -flatten {}.png {}.png'.format(document_title, document_title))
	os.system('convert {}.png -fill white -alpha remove static/{}.png'.format(document_title, document_title))
	os.remove(document_title + '.aux')
	os.remove(document_title + '.log')
	os.remove(document_title + '.synctex.gz')
	os.system('mv {}.png static'.format(document_title))
	# os.system('open {}.pdf'.format(document_title))	

	# pyperclip.copy(output)

if __name__ == '__main__':
	rowDim = 10
	colDim = 10
	wordList = ['henry', 'granger', 'history', 'century', 'math']
	wordScramble = makeWordSearch(wordList, rowDim, colDim)
	matrixToLatex(wordScramble, colDim)