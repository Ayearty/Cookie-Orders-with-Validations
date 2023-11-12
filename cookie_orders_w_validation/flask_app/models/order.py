from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

class Order:
    DB="cookie_orders"
    def __init__( self , data ):
        self.id = data['id']
        self.customer_name = data['customer_name']
        self.cookie_type = data['cookie_type']
        self.number_of_boxes = data['number_of_boxes']

    @staticmethod
    def validate_order(order):
        is_valid = True
        if order["customer_name"] == "" or order["cookie_type"] == "" or order["number_of_boxes"] == "":
            flash("All fields required.")
            is_valid = False
        elif len(order['customer_name']) < 2:
            flash("Name must be at least 2 characters.")
            is_valid = False
        elif len(order['cookie_type']) < 2:
            flash("Cookie type must be at least 2 characters.")
            is_valid = False
        elif int(order["number_of_boxes"]) < 0:
            flash("Boxes cannot have a negative number.")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data ):
        query = """INSERT INTO cookie_orders (customer_name,cookie_type,number_of_boxes) 
        VALUES (%(customer_name)s,%(cookie_type)s,%(number_of_boxes)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cookie_orders;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def edit(cls,data):
        query = """UPDATE cookie_orders 
                SET customer_name=%(customer_name)s,cookie_type=%(cookie_type)s,number_of_boxes=%(number_of_boxes)s
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_one(cls, data):
        query  = """SELECT * FROM cookie_orders WHERE id = %(id)s"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    