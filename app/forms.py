from wtforms import Form, BooleanField, TextField, PasswordField, validators

class MyRegForm(Form):
    username = TextField('Username', [validators.Length(min=6, max=32)])
    email = TextField('Indirizzo E-mail', [validators.Length(min=6, max=35)])
    password = PasswordField('Nuova Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Le Password devono essere identiche')
    ])
    confirm = PasswordField('Ripeti Password')
