from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, ValidationError, validators, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
import shelve
from werkzeug.security import check_password_hash
import re

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', [Length(min=1, max=150), Regexp('^[a-zA-Z]+$', message="Username must contain only alphabetic characters."), DataRequired()])
    last_name = StringField('Last Name', [Length(min=1, max=150), Regexp('^[a-zA-Z]+$', message="Username must contain only alphabetic characters."), DataRequired()], )
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

class ContactForm(FlaskForm):
    first_name = StringField('First Name', [Length(min=1, max=150), Regexp('^[a-zA-Z]+$', message="Username must contain only alphabetic characters."), DataRequired()])
    last_name = StringField('Last Name', [Length(min=1, max=150), Regexp('^[a-zA-Z]+$', message="Username must contain only alphabetic characters."), DataRequired()])
    email = EmailField('Email', [Email(), DataRequired()])
    message = TextAreaField('Remarks', [Length(min=10, message="Message must contain more than 5 letters"), DataRequired()])
    button = SubmitField(label='Submit')

def is_valid_address(form, field):
    address = field.data

    # Check if the address contains at least one digit and one letter
    if not any(char.isdigit() for char in address) or not any(char.isalpha() for char in address):
        raise validators.ValidationError('Invalid address. Address should be street - city - country')

    # Check if the address is not too short
    if len(address) < 10:
        raise validators.ValidationError('Invalid address. Address must be at least 10 characters long.')
    
def contains_only_digits(form, field):
    value = field.data

    # Check if the value contains only digits
    if not value.isdigit():
        raise validators.ValidationError(f'Invalid input. {field.label.text} must contain only digits.')
    
def credit_digit(form, field):
    credit = field.data

    if len(credit) < 16:
        raise validators.ValidationError('Invalid Credit Number. Must be 16 digits')
    
def cvv_digit(form, field):
    cvv = field.data

    if len(cvv) < 4:
        raise validators.ValidationError('Invalid CVV Number. Must be 3- or 4- digits')
    
def valid_expiry_date(form, field):
    expiry = field.data

    # Check if the expiry date is in the format MM/YYYY
    if not re.match(r"^(0[1-9]|1[0-2])\/20\d{2}$", expiry):
        raise validators.ValidationError('Invalid expiry date format. Please use MM/YYYY.')    

class CreateBuyerForm(FlaskForm):
    username = StringField('Full name', [validators.Length(min=1, max=60), validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=1, max=60), validators.DataRequired(), is_valid_address])
    code = StringField('Postal code', [validators.Length(min=1, max=60), validators.DataRequired(), contains_only_digits])
    pnumber = StringField('Phone number', [validators.Length(min=1, max=60), validators.DataRequired(), contains_only_digits])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])

class CreditCardDetail(FlaskForm):
    nameID = StringField('Name ID',[validators.Length(min=1, max= 60), validators.DataRequired()])
    credit = StringField('Credit Card Number',[validators.Length(min=1, max= 60), validators.DataRequired(), credit_digit, contains_only_digits])
    expiry = StringField('Expiry Date (MM/YYYY)',[validators.Length(min=7, max= 7), validators.DataRequired(), valid_expiry_date])
    cvv = StringField('CVV',[validators.Length(min=1, max= 60), validators.DataRequired(), cvv_digit, contains_only_digits])