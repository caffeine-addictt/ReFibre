from users import User
import shelve

class Customer(User):
    def __init__(self, firstname, lastname, email, password):
        self.customer_id = self.generate_cust_id()
        super().__init__(email, password)
        self.firstname = firstname
        self.lastname = lastname
        self.pnumber = None
        self.gender = None
        self.postal_code = None
        self.address = None
        self.date_of_birth = None
        self.reward_point = None
        self.card_name = None
        self.card_number = None
        self.expiration_date = None
        self.cvv = None

    # Function for generating user ID with persistant storage
    @staticmethod
    def generate_cust_id():
        users_id = {}
        db = shelve.open('customer_db')  # Open or create a shelf file
        try: 
            users_id = db["UserID"]
        except:
            print("Error in retrieving UserID from customer_db.")
        last_id = users_id.get('last_id', 0)  # Retrieve last assigned user_id or initialize to 0
        new_id = last_id + 1  # Increment user_id
        users_id['last_id'] = new_id  # Update the last_id in the shelf
        db['UserID'] = users_id
        db.close()
        return new_id
    
    # Accessor method
    def get_customer_id(self):
        return self.customer_id
    def get_first_name(self):
        return self.firstname
    def get_last_name(self):
        return self.lastname
    def get_pnumber(self):
        return self.pnumber
    def get_gender(self):
        return self.gender
    def get_postal_code(self):
        return self.postal_code
    def get_address(self):
        return self.address
    def get_date_of_birth(self):
        return self.date_of_birth
    def get_reward_point(self):
        return self.reward_point
    def get_card_name(self):
        return self.card_name
    def get_card_number(self):
        return self.card_number
    def get_expiration_date(self):
        return self.expiration_date
    def get_cvv(self):
        return self.cvv
    
    
    
    # Mutator methods
    def set_customer_id(self, customer_id):
        self.customer_id = customer_id
    def set_first_name(self, firstname):
        self.firstname = firstname
    def set_last_name(self, lastname):
        self.lastname = lastname
    def set_pnumber(self, pnumber):
        self.pnumber = pnumber
    def set_gender(self, gender):
        self.gender = gender
    def set_postal_code(self, postal_code):
        self.postal_code = postal_code
    def set_address(self, address):
        self.address = address
    def set_date_of_birth(self, date_of_birth):
        self.date_of_birth = date_of_birth
    def set_reward_point(self, reward_point):
        self.reward_point = reward_point
    def set_card_name(self, card_name):
        self.card_name = card_name
    def set_card_number(self, card_number):
        self.card_number = card_number
    def set_expiration_date(self, expiration_date):
        self.expiration_date = expiration_date
    def set_cvv(self, cvv):
        self.cvv = cvv