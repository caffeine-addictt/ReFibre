class User():
    def __init__(self, username, address, code, pnumber, email):
        self.__username = username
        self.__address = address
        self.__code = code
        self.__pnumber = pnumber
        self.__email = email

    def get_username(self):
        return self.__username
    
    def get_address(self):
        return self.__address
    
    def get_code(self):
        return self.__code
    
    def get_pnumber(self):
        return self.__pnumber
    
    def get_email(self):
        return self.__email

    def set_username(self, username):
        self.__username = username

    def set_address(self, address):
        self.__address = address

    def set_code(self, code):
        self.__code = code

    def set_pnumber(self, pnumber):
        self.__pnumber = pnumber      

    def set_email(self, email):
        self.__email = email

class Banking():
    def __init__(self, nameID, credit, expiry, cvv):
        self.__nameID = nameID
        self.__credit = credit
        self.__expiry = expiry
        self.__cvv = cvv

    def get_nameID(self):
        return self.__nameID
    
    def get_credit(self):
        return self.__credit
    
    def get_expiry(self):
        return self.__expiry
    
    def get_cvv(self):
        return self.__cvv
    
    def set_nameID(self, nameID):
        self.__nameID = nameID

    def set_credit(self, credit):
        self.__credit = credit

    def set_expiry(self, expiry):
        self.__expiry = expiry

    def set_cvv(self, cvv):
        self.__cvv = cvv

    