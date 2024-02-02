from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from forms import SignUpForm, SignInForm, ContactForm
import shelve, customer
from werkzeug.security import generate_password_hash

# Configure app
app = Flask(__name__)

# Configure session
app.secret_key = 'hello'
app.config["SESSION_PERMANENT"] = False

# route for root path
@app.route('/')
def home():
    return render_template('home.html')

# route for sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    sign_up = SignUpForm(request.form)
    if request.method == 'POST' and sign_up.validate():
        customers_dict = {}
        db = shelve.open('customer_db')
        email = request.form['email']

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer_db.")

        # validate if user account already exits
        for users in customers_dict:
            user = SignUpForm.account_validate(email)
            # if email address is already in use
            if user:
                db.close()
                return render_template('signUp_fail.html', form=sign_up)
            # if email address not in use
            if not user:
                break

        hashed_password = generate_password_hash(sign_up.password.data)
        user = customer.Customer(sign_up.first_name.data, sign_up.last_name.data, sign_up.email.data, hashed_password)
        customers_dict[user.get_customer_id()] = user
        db['Customers'] = customers_dict

        db.close()

        return redirect(url_for('signin'))
    return render_template('signUp.html', form=sign_up)

# route for customers to log in
@app.route('/signin',  methods=['GET', 'POST'])
def signin():
    sign_in = SignInForm(request.form)
    if request.method == 'POST' and sign_in.validate():
        customers_dict = {}
        db = shelve.open('customer_db')
        email = sign_in.email.data
        password = sign_in.password.data

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer_db.")

        if sign_in.account_authenticate(email, password):
            session["user"] = email
            return render_template('home.html', form=sign_in)
        else:
            return render_template('signIn_fail.html', form=sign_in)
        
    return render_template('signIn.html', form=sign_in)

# route for customer to sign out
@app.route('/signout')
def signout():
    try:
        session["user"] = None
        return redirect("/")
    except:
        return render_template("forbidden.html")

# route to display customers
@app.route('/displayCustomers')
def display_customers():
    customers_dict = {}
    db = shelve.open('customer_db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        user = customers_dict.get(key)
        customers_list.append(user)

    return render_template('displayCustomers.html', count=len(customers_list), users_list=customers_list)

@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_user_form = SignUpForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        db = shelve.open('customer_db', 'w')
        users_dict = db['Customers']
        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_email(update_user_form.email.data)
        user.set_password(update_user_form.password.data)
        db['Customers'] = users_dict
        db.close()

        return redirect(url_for('display_customers'))
    else:
        users_dict = {}
        db = shelve.open('customer_db', 'r')
        users_dict = db['Customers']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.email.data = user.get_email()
        update_user_form.password.data = user.get_password()

        return render_template('updateCustomer.html', form=update_user_form)
    
# Route to delete user
@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('customer_db', 'w')
    users_dict = db['Customers']

    users_dict.pop(id)

    db['Customers'] = users_dict
    db.close()

    return redirect(url_for('display_customers'))

@app.route('/signin/admin')
def admin_page():
    try:
        if session["user"] == "admin.refiber@gmail.com":
            return render_template("admin.html")
        else:
            return render_template("forbidden.html")
    except:
        return render_template("forbidden.html")


# Route for contact us page
@app.route('/contactUs', methods=['GET', 'POST'])
def contact_us():
    contact_us = ContactForm(request.form)
    if request.method == 'POST' and contact_us.validate():
            return render_template('contactSubmission.html')
    return render_template('contactUs.html', form=contact_us)

# remove CSRF protection for the time being
app.config['WTF_CSRF_ENABLED'] = False

if __name__ == '__main__':
    app.run(port=8080)
