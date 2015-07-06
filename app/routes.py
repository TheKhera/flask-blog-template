from flask import *
from flask import request
from functools import wraps
from app import app
from .form import MyPostEditForm
import json
from pprint import pprint

def save_postJson(t, a, c):
    jsonData = [
        {
            'titolo':t,
            'autore':a,
            'corpo':c
        }
    ]

    # Ricaviamo il numero dei post ed add aggiugiamo 1
    nPostFile = open('database/POST/#_nPost.txt', 'r')
    nPost = nPostFile.read()
    nPostFile.close()
    nPost = int(nPost)
    nPost += 1

    # Salviamo jsonData in json file
    with open('database/POST/' + str(nPost) + '_post.json', 'w') as f:
        json.dump(jsonData, f)
    f.close() # Non so se ci va ho no bho ?!

    # Aggiorniamo il numero dei post
    nPostFile = open('database/POST/#_nPost.txt', 'w')
    nPostFile.write(str(nPost))
    nPostFile.close()

def read_postJson():
    # Ricaviamo il numero dei post
    nPostFile = open('database/POST/#_nPost.txt', 'r')
    nPost = nPostFile.read()
    nPostFile.close()
    nPost = int(nPost)

    arrayTest = []

    x = 1
    while x <= nPost:
        with open('database/POST/' + str(x) + '_post.json') as dataJson:
            d = json.load(dataJson)
            dataJson.close()
            arrayTest.append(d)
            x += 1
    print type(arrayTest)
    print ''
    print ''
    y = 0
    arrayReturn = []
    while y < nPost:
        print arrayTest[y][0]
        arrayReturn.append(arrayTest[y][0])
        y += 1
    return arrayReturn

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Effetuare il login!')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@app.route('/home')
def home():
    arrayPost = read_postJson()
    return render_template('home.html', title='HomePage', session=session, posts=arrayPost)

@app.route('/admin_manage')
@login_required
def admin_manage():
    return render_template('admin_manage.html', title='HelloTestPage', session=session)

@app.route('/post_edit', methods=('GET', 'POST'))
@login_required
def post_edit():
    form = MyPostEditForm()
    if form.validate_on_submit():
        titolo = form.titolo.data
        autore = form.autore.data
        corpo = form.corpo.data

        print titolo
        print autore
        print corpo

        # Codifichiamo tutti con utf-8

        titolo = titolo.encode('UTF-8', 'strict')
        autore = autore.encode('UTF-8', 'strict')
        corpo = corpo.encode('UTF-8', 'strict')


        print titolo
        print autore
        print corpo

        # Inviamo il risulato ad uno script che si occumera di salvare il post
        risposta = save_postJson(titolo, autore, corpo)

        if risposta == True:
            return redirect(url_for('admin_manage'))
        else:
            return redirect(url_for('post_edit'))
    return render_template('post_editor.html', form=form, session=session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USER'] or request.form['password'] != app.config['PASS']:
            error = 'Username o Password Errati.'
        else:
            session['logged_in'] = True # Impostiamo che nella sessione l'utente ha effetuato l'acesso
            session['username'] = request.form['username'] # Inseriamo anche il nome che verra visulizatto
            return redirect(url_for('admin_manage'))
    return render_template('login.html', error=error, title='Accedi')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Disconesso con successo!')
    return redirect(url_for('login'))
