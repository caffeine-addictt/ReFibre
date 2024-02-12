class Transaction():
    def __init__(self, customer_email, trans_id, item_price, item_revenue):
        self.customer_email = customer_email
        self.trans_id = trans_id
        self.item_price = item_price
        self.item_revenue = item_revenue
    
    # Accessor method
    def get_cust_email(self):
        return self.customer_email
    def get_trans_id(self):
        return self.trans_id
    def get_item_price(self):
        return self.item_price
    def get_item_revenue(self):
        return self.item_revenue
    
    # Mutator methods
    def set_trans_id(self, trans_id):
        self.trans_id = trans_id
    def set_item_price(self, item_price):
        self.item_price = item_price
    def set_item_revenue(self, item_revenue):
        self.item_revenue = item_revenue
