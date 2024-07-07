from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from forms import SignUpForm, SignInForm, ContactForm, CreateBuyerForm, CreditCardDetail, RewardPoints, Customer_details_form, CreditCardForm, ChangePassword
import shelve, customer, uuid, transaction
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from cart import ShoppingCart


# Configure app
app = Flask(__name__)

# Configure session
app.secret_key = 'hello'
app.config["SESSION_PERMANENT"] = False
products = []
cart = {}

# route for root path
@app.route('/')
def home():
    try:
        if session["user"] == "admin.refiber@gmail.com":
            pass
    except:
        session["user"] = None
    return render_template('info_page/home.html')

# Route for contact us page
@app.route('/contactUs', methods=['GET', 'POST'])
def contact_us():
    contact_us = ContactForm(request.form)
    if request.method == 'POST' and contact_us.validate():
            return render_template('contactSubmission.html')
    return render_template('info_page/contactUs.html', form=contact_us)

# route for sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    sign_up = SignUpForm(request.form)
    if request.method == 'POST' and sign_up.validate():
        db = shelve.open('customer_db', 'c')
        db["Customers"] = db.get("Customers", {})
        db["last_id"] = db.get('last_id', 0)
        email = request.form['email']

        # validate if user account already exits
        if SignUpForm.account_validate(email):
            db.close()
            return render_template('signin_signup/signUp_fail.html', form=sign_up)

        hashed_password = generate_password_hash(sign_up.password.data)
        db['last_id'] += 1
        user = customer.Customer(db['last_id'], sign_up.first_name.data, sign_up.last_name.data, sign_up.email.data, hashed_password)
        db['Customers'] = {
            **db['Customers'], 
            user.customer_id: user
        }
        db.close()

        return redirect(url_for('signin'))
    return render_template('signin_signup/signUp.html', form=sign_up)

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
            return render_template('info_page/home.html', form=sign_in)
        else:
            return render_template('signin_signup/signIn_fail.html', form=sign_in)
        
    return render_template('signin_signup/signIn.html', form=sign_in)

# route for customer to sign out
@app.route('/signout')
def signout():
    try:
        session["user"] = None
        return redirect("/")
    except:
        return render_template("error_page/forbidden.html")

# Rachel's part
# Route for admin page
@app.route('/admin')
def admin_page():
    try:
        if session["user"] == "admin.refiber@gmail.com":
            customers_dict = {}
            db = shelve.open('customer_db', 'r')
            customers_dict = db['Customers']
            transactions_dict = db['Transactions']
            db.close()

            customers_list = []
            for key in customers_dict:
                user = customers_dict.get(key)
                customers_list.append(user)
            
            transactions_list = []
            for key in transactions_dict:
                trans = transactions_dict.get(key)
                transactions_list.append(trans)

            return render_template("admin_account/admin.html", count=len(customers_list), count_trans=len(transactions_list), users_list=customers_list, trans_list=transactions_list)
        else:
            return render_template("error_page/forbidden.html")
    except:
        return render_template("error_page/forbidden.html")

# Route for updating users rewards points
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

        return render_template('admin_account/reward_points.html', form=update_reward_form)

# Route for deleting customer on admin page
@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customer_db', 'w')
    customers_dict = db['Customers']

    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('admin_page'))

# Keefe's part
# Route for shop
@app.route('/shop')
def display_items():
    return render_template('shop/men.html')

  
@app.route('/shop/women')
def display_women_items():
    return render_template('shop/women.html')

  
@app.route('/shop/new-arrivals')
def display_new_arrivals():
    return render_template('shop/newArrivals.html')

 
@app.route('/shop/men')
def display_men_items():
    return render_template('shop/men.html')


@app.route('/cart', methods=['GET', 'POST'])
def view_cart():
    global cart
    if request.method == 'POST':
        id: int = int(request.form.get('id'))
        name = request.form.get('product-name')
        price = float(request.form.get('price'))
        image_url = request.form.get('image_url')
        cart[id] = {
            'product_name': name,
            'product_price': price,
            'image_url': image_url
        }
        return redirect(url_for('checkout_details'))

    total_price = sum(product_info['product_price'] for product_info in cart.values()) if cart else 0.0
    return render_template('shop/cart.html', cart=cart, total_price=total_price)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    global cart
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart = session.get('cart', [])
        cart.append(product)
        session['cart'] = cart
    return redirect(url_for('shop'))


@app.route('/remove_from_cart')
def remove_from_cart():
    try:
        id = int(request.args.get("id"))
    except ValueError:
        return "INVALID_ID_SUPPLIED", 400

    if id in cart:
        del cart[id]

    return redirect(url_for("checkout_details"))

# Dean's part
# Route for user_details
@app.route('/userdetails')
def display_user_info():
    customers_dict = {}
    db = shelve.open('customer_db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    user_info = []

    # Iterate over customers_dict to create a list of all customers
    for key in customers_dict:
        user = customers_dict.get(key)
        customers_list.append(user)

    # Filter the user whose email matches the email stored in the session
    for user in customers_list:
        if session["user"] == user.get_email():
            user_info.append(user)  # Append the matching user to user_info
            break  # Exit the loop once a match is found

    # Now user_info contains the user whose email matches the one stored in the session

    return render_template('user_account/user_details.html', users_list=user_info)


# route to user update
@app.route('/user_update/<int:id>/', methods=['GET', 'POST'])
def user_update(id):
    user_details_form = Customer_details_form(request.form)
    if request.method == 'POST' and user_details_form.validate():
        db = shelve.open('customer_db', 'w')
        users_dict = db['Customers']
        user = users_dict.get(id)
        user.set_first_name(user_details_form.first_name.data)
        user.set_last_name(user_details_form.last_name.data)
        user.set_email(user_details_form.email.data)
        user.set_gender(user_details_form.gender.data)
        user.set_postal_code(user_details_form.postal_code.data)
        user.set_address(user_details_form.address.data)
        user.set_date_of_birth(user_details_form.date_of_birth.data)
        db['Customers'] = users_dict
        db.close()

        return redirect(url_for('display_user_info'))
    else:
        users_dict = {}
        db = shelve.open('customer_db', 'r')
        users_dict = db['Customers']
        db.close()

        user = users_dict.get(id)
        user_details_form.first_name.data = user.get_first_name()
        user_details_form.last_name.data = user.get_last_name()
        user_details_form.email.data = user.get_email()
        user_details_form.gender.data = user.get_gender()
        user_details_form.postal_code.data = user.get_postal_code()
        user_details_form.address.data = user.get_address()
        user_details_form.date_of_birth.data = user.get_date_of_birth()


        return render_template('user_account/user_update.html', form= user_details_form)
    
# route to user billing    
@app.route('/userbilling')  # Change the route here
def display_user_billing():
    customers_dict = {}
    db = shelve.open('customer_db', 'r')
    customers_dict = db['Customers']
    transactions_dict = db["Transactions"]
    db.close()

    customers_list = []
    user_info = []

    for key in customers_dict:
        user = customers_dict.get(key)
        customers_list.append(user)

    # Filter the user whose email matches the email stored in the session
    for user in customers_list:
        if session["user"] == user.get_email():
            user_info.append(user)  # Append the matching user to user_info
            break  # Exit the loop once a match is found
    
    user_trans_list = []

    # Iterate over transactions_dict and filter transactions by user email
    for key in transactions_dict:
        transaction = transactions_dict.get(key)
        if session.get("user") == transaction.get_cust_email():
            user_trans_list.append(transaction)

    return render_template('user_account/user_billing.html', users_list=user_info, trans_list=user_trans_list)

# route to payment method
@app.route('/edit_payment_method/<int:id>/', methods=['GET', 'POST'])
def add_payment_method(id):
    user_payment_form = CreditCardForm(request.form)
    if request.method == 'POST' and user_payment_form.validate():
        db = shelve.open('customer_db', 'w')
        users_dict = db['Customers']
        user = users_dict.get(id)
        user.set_card_name(user_payment_form.name.data)
        user.set_card_number(user_payment_form.card_number.data)
        user.set_expiration_date(user_payment_form.expiration_date.data)
        user.set_cvv(user_payment_form.cvv.data)
        db['Customers'] = users_dict
        db.close()

        return redirect(url_for('display_user_billing'))
    else:
        users_dict = {}
        db = shelve.open('customer_db', 'r')
        users_dict = db['Customers']
        db.close()

        user = users_dict.get(id)
        user_payment_form.name.data = user.get_card_name()
        user_payment_form.card_number.data = user.get_card_number()
        user_payment_form.expiration_date.data = user.get_expiration_date()
        user_payment_form.cvv.data = user.get_cvv()

        return render_template('user_account/add_payment_method.html', form=user_payment_form)

# route to display user security
@app.route('/usersecurity')
def display_user_security():
    customers_dict = {}
    db = shelve.open('customer_db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    user_info = []

    for key in customers_dict:
        user = customers_dict.get(key)
        customers_list.append(user)

    # Filter the user whose email matches the email stored in the session
    for user in customers_list:
        if session["user"] == user.get_email():
            user_info.append(user)  # Append the matching user to user_info
            break  # Exit the loop once a match is found

    return render_template('user_account/user_security.html', users_list=user_info)

@app.route("/update_security/<int:id>/", methods=['GET', 'POST'])
def update_user_security(id):
    user_pass_form = ChangePassword(request.form)
    if request.method == 'POST' and user_pass_form.validate():
        db = shelve.open('customer_db', 'w')
        users_dict = db['Customers']
        user = users_dict.get(id)
        hashed_password = generate_password_hash(user_pass_form.password.data)
        user.set_password(hashed_password)
        db['Customers'] = users_dict
        db.close()

        return redirect(url_for('display_user_security'))
    else:
        return render_template('user_account/edit_security.html', form=user_pass_form)

#Ji wei's part
# Route for confirming user purchase details
@app.route('/checkout_details')
def checkout_details():
    customers_dict = {}
    db = shelve.open('customer_db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    user_info = []

    for key in customers_dict:
        user = customers_dict.get(key)
        customers_list.append(user)

    # Filter the user whose email matches the email stored in the session
    for user in customers_list:
        if session["user"] == user.get_email():
            user_info.append(user)  # Append the matching user to user_info
            break  # Exit the loop once a match is found
    global cart
    total_price = sum(product_info['product_price'] for product_info in cart.values()) if cart else 0.0

    return render_template('checkout/checkout_details.html', cart=cart, total_price=total_price, users_list=user_info)

# Route for confirming user personal info
@app.route('/checkout/<int:id>/', methods=['GET','POST'])
def personal_detail(id):
    checkout_personalinfo_form = CreateBuyerForm(request.form)
    if request.method == 'POST' and checkout_personalinfo_form.validate():
        db = shelve.open('customer_db', 'w')
        customers_dict = db['Customers']
        user = customers_dict.get(id)
        user_id = user.get_customer_id()
        user.set_first_name(checkout_personalinfo_form.username.data)
        user.set_address(checkout_personalinfo_form.address.data)
        user.set_postal_code(checkout_personalinfo_form.code.data)
        user.set_pnumber(checkout_personalinfo_form.pnumber.data)
        user.set_email(checkout_personalinfo_form.email.data)
        db['Customers'] =  customers_dict
        db.close()


        return redirect(url_for('banking_detail', id=user_id))
    else:
        customers_dict = {}
        db = shelve.open('customer_db', 'r')
        customers_dict = db['Customers']
        db.close()

        user = customers_dict.get(id)
        checkout_personalinfo_form.username.data = user.get_first_name()
        checkout_personalinfo_form.address.data = user.get_address()
        checkout_personalinfo_form.code.data = user.get_postal_code()
        checkout_personalinfo_form.pnumber.data = user.get_pnumber()
        checkout_personalinfo_form.email.data = user.get_email()

        return render_template('checkout/checkout.html', form=checkout_personalinfo_form)

# Route for confirming user payment method checkout
@app.route('/checkout1/<int:id>/', methods=['GET','POST'])
def banking_detail(id):
    banking_details_form = CreditCardDetail(request.form)
    if request.method == 'POST' and banking_details_form.validate():
        db = shelve.open('customer_db', 'w')
        customers_dict = db['Customers']
        user = customers_dict.get(id)
        user_id = user.get_customer_id()
        user.set_card_name(banking_details_form.nameID.data)
        user.set_card_number(banking_details_form.credit.data)
        user.set_expiration_date(banking_details_form.expiry.data)
        user.set_cvv(banking_details_form.cvv.data)
        db['Customers'] =  customers_dict
        db.close()

        return redirect(url_for('display_buyers', id=user_id))
    else:
        customers_dict = {}
        db = shelve.open('customer_db', 'r')
        customers_dict = db['Customers']
        db.close()
        
        user = customers_dict.get(id)
        banking_details_form.nameID.data = user.get_card_name()
        banking_details_form.credit.data = user.get_card_number()
        banking_details_form.expiry.data = user.get_expiration_date()
        banking_details_form.cvv.data = user.get_cvv()

        return render_template('checkout/checkout_banking.html', form=banking_details_form)

# Route for confirming user details for checkout
@app.route('/confirm/<int:id>/')
def display_buyers(id):
    global cart
    users_dict = {}
    db = shelve.open('customer_db', 'r')
    users_dict = db["Customers"]
    
    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)
    
    customers_list = []
    user_info = []

    for key in users_dict:
        user = users_dict.get(key)
        customers_list.append(user)

    # Filter the user whose email matches the email stored in the session
    for user in customers_list:
        if session["user"] == user.get_email():
            user_info.append(user)  # Append the matching user to user_info
            break  # Exit the loop once a match is found

    return render_template('checkout/confirm.html', users_list=users_list, customer_list=user_info)

# Route for confirmation page
@app.route('/confirmation_page/<int:id>/')
def thank_you_for_purchase(id):
    global cart
    # Generate a random purchase ID
    purchase_id = str(uuid.uuid4())[:15]
    db = shelve.open('customer_db')
    customers_dict = db['Customers']
    email = session["user"]
    print(email)
    db["Transactions"] = db.get("Transactions", {}) 
    item_price = sum(product_info['product_price'] for product_info in cart.values()) if cart else 0.0
    total_price = item_price + 10

    trans_info = transaction.Transaction(email, purchase_id, item_price, total_price)
    db['Transactions'] = {
            **db['Transactions'], 
            trans_info.trans_id: trans_info
        }
    db.close()

    # Render the thank you page with the purchase ID
    return render_template('checkout/lastpage.html', purchase_id=purchase_id)

# debugging purposes
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

    return render_template('debug/displayCustomers.html', count=len(customers_list), users_list=customers_list)

# Route to update customer
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

        return render_template('debug/updateCustomer.html', form=update_user_form)
    
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

# remove CSRF protection for the time being
app.config['WTF_CSRF_ENABLED'] = False

if __name__ == '__main__':
    app.run(port=8080)