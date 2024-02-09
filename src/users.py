import shelve

# User class
class User():
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    # Accessor method
    def get_email(self):
        return self.email
    def get_password(self):
        return self.password
    
    # Mutator methods
    def set_email(self, email):
        self.email = email
    def set_password(self, password):
        self.password = password