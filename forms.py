from flask_wtf import Form
from wtforms import StringField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.simple import PasswordField


class LoginForm(Form):
    user_id = IntegerField('ID:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


class BooklistForm(Form):
    submit = SubmitField('New')


class BookForm(Form):
    isbn = IntegerField('ISBN: ', validators=[DataRequired()])
    title = StringField('Title:', validators=[DataRequired()])
    price = DecimalField('Price: ', validators=[DataRequired()])
