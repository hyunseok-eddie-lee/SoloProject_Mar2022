from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Item:
    db_name = 'items'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.category = db_data['category']
        self.description = db_data['description']
        self.sub_category = db_data['sub_category']
        self.item_image = db_data['item_image']
        self.buying_date = db_data['buying_date']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO items (category, description, sub_category, item_image, buying_date, user_id) VALUES (%(category)s,%(description)s,%(sub_category)s,%(item_image)s,%(buying_date)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM items;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_items = []
        for row in results:
            print(row['buying_date'])
            all_items.append( cls(row) )
        return all_items

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM items WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE items SET category=%(category)s, description=%(description)s, sub_category=%(sub_category)s, item_image=%(item_image)s, buying_date=%(buying_date)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM items WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_item(item):
        is_valid = True
        if item['category'] =="":
            is_valid = False
            flash("Category must be selected", "item")
        if item['sub_category'] =="":
            is_valid = False
            flash("Sub-category must be selected", "item")
        if len(item['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters", "item")
        if item['buying_date'] == "":
            is_valid = False
            flash("Please enter a date", "item")
        return is_valid