from flask_wtf import *
from wtforms import *
from wtforms.validators import *

class Login(FlaskForm):
    login = StringField('Login',validators=[DataRequired()])
    password = PasswordField('Hasło',validators=[DataRequired()])
    submit = SubmitField('Zaloguj')