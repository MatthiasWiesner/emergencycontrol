from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, Email, URL


class PersonForm(Form):
    name = TextField('Person name', validators=[Required()])
    phone = TextField('Phone', validators=[Required()])
    picture = TextField('Photo url', validators=[Required(), URL()])
