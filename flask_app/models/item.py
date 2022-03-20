from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Item:
    db_name = 'everyclosetwardrobe'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.clothing_top = db_data['clothing_top']
        self.clothing_bottom = db_data['clothing_bottom']
        self.underwear_swim = db_data['underwear_swim']
        self.pajamas = db_data['pajamas']
        self.shoes_socks = db_data['shoes_socks']
        self.accessory = db_data['accessory']
        self.buying_date = db_data['buying_date']
        self.item_image_url = db_data['item_image_url']
        self.description = db_data['description']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO items (user_id, clothing_top, clothing_bottom, underwear_swim, pajamas, shoes_socks, accessory, buying_date, item_image_url, description) VALUES (%(user_id)s,%(clothing_top)s,%(clothing_bottom)s,%(underwear_swim)s,%(pajamas)s,%(shoes_socks)s,%(accessory)s,%(buying_date)s,%(item_image_url)s,%(description)s);"
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
        query = "UPDATE items SET clothing_top=%(clothing_top)s, clothing_bottom=%(clothing_bottom)s, underwear_swim=%(underwear_swim)s, pajamas=%(pajamas)s, shoes_socks=%(shoes_socks)s, accessory=%(accessory)s, buying_date=%(buying_date)s, item_image_url=%(item_image_url)s, description=%(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM items WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_item(item):
        is_valid = True
        # if item['category'] =="":
        #     is_valid = False
        #     flash("Category must be selected", "item")
        # if item['sub_category'] =="":
        #     is_valid = False
        #     flash("Sub-category must be selected", "item")
        # if len(item['description']) < 3:
        #     is_valid = False
        #     flash("Description must be at least 3 characters", "item")
        if item['buying_date'] == "":
            is_valid = False
            flash("Please enter a date", "item")
        return is_valid