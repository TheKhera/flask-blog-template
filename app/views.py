from flask import render_template, Flask, jsonify, request, flash, redirect, url_for
from app import app
from .forms import MyRegForm
import json
import os
import hashlib

USER = None

@app.route('/')
@app.route('/homepage')
def index():
    return render_template('homepage.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = MyRegForm(request.form)
    if request.method == 'POST' and form.validate():
        data = [form.username.data, form.email.data, form.password.data]
        fileExist = os.path.isfile('database/USER/' + form.username.data + '.json')
        if fileExist == True:
            USER = form.username.data
            return redirect(url_for('no_register'))
        else:
            fileTest = open('database/USER/' + form.username.data + '.json', 'w')
            
            # Conver password in md5
            m = hashlib.md5()
            m.update(form.password.data)

            jsonData = [
                {
                    'username':form.username.data,
                    'email':form.email.data,
                    'password':m.hexdigest()
                }
            ]
            
            json.dump(jsonData, fileTest)
            fileTest.close()
            flash("Grazie per la tua registrazione...")
            return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/no_reg')
def no_register():
    return render_template('no_register.html', nickname=USER)

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
