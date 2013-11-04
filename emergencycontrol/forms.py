from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, Email, URL


class LoginForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember me', default=False)


class SignupForm(Form):
    username = TextField('Username', validators=[Required()])
    email = TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    password_confirm = PasswordField('Password Confirmation', validators=[Required()])
    remember = BooleanField('Remember me', default=False)


class PersonForm(Form):
    name = TextField('Person name', validators=[Required()])
    phone = TextField('Phone', validators=[Required()])
    image_url = TextField('Photo url', validators=[Required(), URL()])
