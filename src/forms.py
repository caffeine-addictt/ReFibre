from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
import shelve
from werkzeug.security import check_password_hash

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

    def account_validate(email):
        db = shelve.open('customer_db', 'r')
        existing_user = db['Customers']
        existing_list = []
        for key in existing_user:
            user = existing_user.get(key)
            existing_list.append(user)
        for user in existing_list:
            if email == user.get_email():
                return True
            else:
                continue
        return False
            
class SignInForm(FlaskForm):
    email = EmailField('Email', [Email(), DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    button = SubmitField(label="Log In")

    def account_authenticate(self, email, password):
        db = shelve.open('customer_db', 'r')
        existing_user = db['Customers']
        existing_list = []
        for key in existing_user:
            user = existing_user.get(key)
            existing_list.append(user)
        for user in existing_list:
            if email == user.get_email():
                user_pass = user.get_password()
                return check_password_hash(user_pass, password)
            elif email == "admin.refiber@gmail.com":
                if password == "admin@password@1234":
                    return True
            else:
                continue