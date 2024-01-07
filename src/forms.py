from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import shelve

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', [Length(min=1, max=150), DataRequired()])
    last_name = StringField('Last Name', [Length(min=1, max=150), DataRequired()])
    email = EmailField('Email', [Email(), DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long'),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password')
    button = SubmitField(label='Create Now')
  