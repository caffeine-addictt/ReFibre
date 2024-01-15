from users import User

class Admin(User):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.__email = "admin.refiber@gmail.com"
        self.__password = "admin@password@1234"


        