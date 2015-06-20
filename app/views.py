from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
	listPost = [ #Falsi array dei post
		{
			'autore': 'AdminTest',
			'title': 'Test title',
			'body': 'Semplice prova'
		},
		{
			'autore': 'AdminTest',
			'title': 'Test title 2',
			'body': 'Test Alpha'
		}
	]
	return render_template('index.html', title='Test Page', posts=listPost)

@app.route('/About')
def about():
	return render_template('about.html', title='About')