from flask import Flask, render_template, request, jsonify, url_for
from wordsearchfunctions import makeWordSearch, matrixToLatexFile
import os

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('indexboot.html')

@app.route('/makesearch', methods=['POST'])
def makesearch():
	rowDim = int(request.form['rowDim'])
	colDim = int(request.form['colDim'])
	words = request.form['words'].strip().split(', ')
	wordSearch = makeWordSearch(words, rowDim, colDim)
	filename = 'testout'
	directory = os.path.dirname(os.path.realpath(__file__))
	directory = matrixToLatexFile(wordSearch, colDim, filename, directory)
	return jsonify({'sent to' : directory})

if __name__ == '__main__':
	app.run()