from flask import render_template, Flask, jsonify, request
from app import app
import json

@app.route('/')
@app.route('/homepage')
def index():
	return render_template('homepage.html')

@app.route('/posteditor')
def posteditor():
	return render_template('post_editor.html')

@app.route('/About')
def about():
	return render_template('about.html', title='About')

@app.route('/_test_save')
def test_save():
    autore = request.args.get('autore', 0, type=str)
    data = request.args.get('data', 0, type=str)
    titolo = request.args.get('titolo', 'Titolo Post', type=str)
    corpo = request.args.get('corpo', 0, type=str)
    
    data = [
        {'autore': autore,
         'data': data,
         'titolo': titolo,
         'corpo': corpo
         }
    ]

    
    filePostOpen = open('database/POST/#_nPost.txt', 'r')

    nPostStr = filePostOpen.read()
    nPost = int(nPostStr)
    nPost += 1
    filePostOpen.close()

    with open('database/POST/pst_ ' + str(nPost) + '.json', 'w') as outputFile:
        json.dump(data, outputFile)
    outputFile.close()

    filePostOpen2 = open('database/POST/#_nPost.txt', 'w')
    filePostOpen2.write(str(nPost))
    filePostOpen2.close()

    return jsonify(result="Post pubblicato!")
