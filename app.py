from flask import Flask, render_template, request, jsonify
from wordsearchfunctions import makeWordSearch, matrixToLatexFile

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
	matrixToLatexFile(wordSearch, colDim)
	return jsonify({'sent' : 'complete'})

if __name__ == '__main__':
	app.run()