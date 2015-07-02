from wtforms import Form, BooleanField, TextField, PasswordField, validators

class MyRegForm(Form):
    username = TextField('Username',[validators.Length(min=6, max=32,message='Username deve essere lungo da 6 a 32 caratteri.')])
    email = TextField('Indirizzo E-mail', [validators.Length(min=6, max=35)])
    password = PasswordField('Nuova Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Le Password devono essere identiche')
    ])
    confirm = PasswordField('Ripeti Password')
