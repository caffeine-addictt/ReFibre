from users import User
import shelve

class Customer(User):
    def __init__(self, firstname, lastname, email, password):
        self.__customer_id = self.generate_cust_id()
        super().__init__(email, password)
        self.__firstname = firstname
        self.__lastname = lastname
        self.__gender = None
        self.__postal_code = None
        self.__address = None
        self.__date_of_birth = None
        self.__reward_point = None

    # Function for generating user ID with persistant storage
    @staticmethod
    def generate_cust_id():
        user_db = shelve.open('user.db', 'c')  # Open or create a shelf file
        last_id = user_db.get('last_id', 0)  # Retrieve last assigned user_id or initialize to 0
        new_id = last_id + 1  # Increment user_id
        user_db['last_id'] = new_id  # Update the last_id in the shelf
        user_db.close()
        return new_id
    
    # Accessor method
    def get_customer_id(self):
        return self.__customer_id
    def get_first_name(self):
        return self.__firstname
    def get_last_name(self):
        return self.__lastname
    def get_gender(self):
        return self.__gender
    def get_postal_code(self):
        return self.__postal_code
    def get_address(self):
        return self.__address
    def get_date_of_birth(self):
        return self.__date_of_birth
    def get_reward_point(self):
        return self.__reward_point
    
    # Mutator methods
    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id
    def set_first_name(self, firstname):
        self.__firstname = firstname
    def set_last_name(self, lastname):
        self.__lastname = lastname
    def set_gender(self, gender):
        self.__gender = gender
    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code
    def set_address(self, address):
        self.__address = address
    def set_date_of_birth(self, date_of_birth):
        self.__date_of_birth = date_of_birth
    def set_reward_point(self, reward_point):
        self.__reward_point = reward_point