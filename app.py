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
	save_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static')
	print('Saving to directory: ' + save_directory)
	matrixToLatexFile(wordSearch, colDim, filename, save_directory)
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	print('Current directory: ' + os.getcwd())
	return jsonify({'sent to' : save_directory})

if __name__ == '__main__':
	app.run(debug=True)