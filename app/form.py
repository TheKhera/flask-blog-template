from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class MyPostEditForm(Form):
	titolo = StringField('Titolo', validators=[DataRequired()])
	autore = StringField('Autore', validators=[DataRequired()])
	corpo = TextAreaField('Post', validators=[DataRequired()])