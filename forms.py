from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    login = StringField('login', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=3,max=30)])
