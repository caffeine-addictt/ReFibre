from flask import Flask, render_template, request, redirect, url_for
from forms import SignUpForm
import shelve, customer


app = Flask(__name__)

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

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        user = customer.Customer(sign_up.first_name.data, sign_up.last_name.data, sign_up.email.data, sign_up.password.data)
        customers_dict[user.get_customer_id()] = user
        db['Customers'] = customers_dict

        db.close()

        return redirect(url_for('display_customers'))
    return render_template('signUp.html', form=sign_up)

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

# remove CSRF protection for the time being
app.config['WTF_CSRF_ENABLED'] = False

if __name__ == '__main__':
    app.run(port=8080)