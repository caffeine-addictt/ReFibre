import shelve

# User class
class User():
    def __init__(self, email, password):
        self.__email = email
        self.__password = password
    
    # Accessor method
    def get_email(self):
        return self.__email
    def get_password(self):
        return self.__password
    
    # Mutator methods
    def set_email(self, email):
        self.__email = email
    def set_password(self, password):
        self.__password = password