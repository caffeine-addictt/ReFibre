from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from forms import SignUpForm, SignInForm, ContactForm, CreateBuyerForm, CreditCardDetail, RewardPoints
import shelve, customer
from customer import Customer
from werkzeug.security import generate_password_hash
from checkout import User, Banking
import uuid

# Configure app
app = Flask(__name__)

# Configure session
app.secret_key = 'hello'
app.config["SESSION_PERMANENT"] = False

# route for root path
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/confirmation_page')
def thank_you_for_purchase():
    # Generate a random purchase ID
    purchase_id = str(uuid.uuid4())[:15]

    # Render the thank you page with the purchase ID
    return render_template('lastpage.html', purchase_id=purchase_id)

@app.route('/checkout', methods=['GET','POST'])
def personal_detail():
    create_buyer_form = CreateBuyerForm(request.form)
    if request.method == 'POST' and create_buyer_form.validate():
        buyers_dict = {}
        db = shelve.open('buyers_db')

        try:
            buyers_dict = db['Buyers','w']
        except:
            print("Error in retrieving Buyers from buyers_db.")

        user = User(create_buyer_form.username.data, create_buyer_form.address.data, create_buyer_form.code.data, create_buyer_form.pnumber.data, create_buyer_form.email.data)
        buyers_dict[user.get_username()] = user
        db['Buyers'] = buyers_dict

        db.close()
        return redirect(url_for('banking_detail'))
    return render_template('checkout.html', form=create_buyer_form)

@app.route('/checkout1', methods=['GET','POST'])
def banking_detail():
    create_banking_details = CreditCardDetail(request.form)
    if request.method == 'POST' and create_banking_details.validate():
        details_dict = {}
        db = shelve.open('details_db')

        try:
            details_dict = db['Details','w']
        except:
            print("Error in retrieving Details from details_db.")
    
        user = Banking(create_banking_details.nameID.data, create_banking_details.credit.data, create_banking_details.expiry.data, create_banking_details.cvv.data)
        details_dict[user.get_nameID()] = user
        db['Details'] = details_dict

        db.close()
        return redirect(url_for('display_buyers'))
    return render_template('checkout1.html', form=create_banking_details)

@app.route('/confirm')
def display_buyers():
    buyers_dict = {}
    db = shelve.open('buyers_db', 'r')
    buyers_dict = db['Buyers']
    db.close()

    buyers_list = []
    for key in buyers_dict:
        user = buyers_dict.get(key)
        buyers_list.append(user)

    details_dict = {}
    db = shelve.open('details_db', 'r')
    details_dict = db['Details']
    db.close()

    details_list = []
    for key in details_dict:
        user = details_dict.get(key)
        details_list.append(user)

    return render_template('confirm.html', count=len(buyers_list), users_list=buyers_list, banking_list=details_list)



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
    
@app.route('/reward_points/<int:id>/', methods=['GET', 'POST'])
def update_reward_points(id):
    update_reward_form = RewardPoints(request.form)
    if request.method == 'POST' and update_reward_form.validate():
        db = shelve.open('customer_db', 'w')
        customers_dict = db['Customers']
        customer = customers_dict.get(id)
        customer.set_reward_point(update_reward_form.reward_point.data)
        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('admin_page'))
    else:
        customers_dict = {}
        db = shelve.open('customer_db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_reward_form.reward_point.data = customer.get_reward_point()

        return render_template('reward_points.html', form=update_reward_form)


    
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
            customers_dict = {}
            db = shelve.open('customer_db', 'r')
            customers_dict = db['Customers']
            db.close()

            customers_list = []
            for key in customers_dict:
                user = customers_dict.get(key)
                customers_list.append(user)

            return render_template("admin.html", count=len(customers_list), users_list=customers_list)
        else:
            return render_template("forbidden.html")
    except:
        return render_template("forbidden.html")
    
@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customer_db', 'w')
    customers_dict = db['Customers']

    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('admin_page'))



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
