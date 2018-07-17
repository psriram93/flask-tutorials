import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",type = float,required = True,help = "Price is a mandatory field")
    @jwt_required()
    def get(self,name):
        # item = next(filter(lambda x: x['name']==name,items), None)
        # return {'item': item}, 200 if item else 404
        item = Item.find_by_name(name)
        if item:
            return item
        return {"message": "item not found"},404

    @classmethod
    def find_by_name(cls,name):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cur.execute(query,(name,))
        row = result.fetchone()
        conn.close()
        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    @classmethod
    def insert(cls,item):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        query = "INSERT INTO items VALUES (?,?)"
        cur.execute(query,(item["name"],item["price"]))
        conn.commit()
        conn.close()

    @classmethod
    def update(cls,item):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        query = "UPDATE items SET price=? WHERE name = ?"
        cur.execute(query,(item["price"],item["name"]))
        conn.commit()
        conn.close()
    
    def post(self,name):
        # if next(filter(lambda x: x['name']==name,items), None):
        #     return {'message': "An item with name '{}' already exists".format(name)},400
        
        # data = request.get_json()
        if Item.find_by_name(name):
            return {"message": "item with name '{}' already exists".format(name)},400
        data = Item.parser.parse_args()
        item = {'name':name,'price':data['price']}
        try:
            Item.insert(item)
        except:
            return {"message": "An error occured in in inserting the item"},500
        return {"message": "An item with name '{}' and price '{}' has been created".format(item["name"],item["price"])},201
    
    def delete(self,name):
        # global items
        # items = list(filter(lambda x: x['name']!=name,items))
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        query = "DELETE FROM items WHERE name=?"
        cur.execute(query,(name,))
        conn.commit()
        conn.close()
        return {"message": "Item deleted"}

    def put(self,name):
        # data = request.get_json()
        data = Item.parser.parse_args()

        item = Item.find_by_name(name)
        updated_item = {"name":name,"price": data["price"]}
        if item is None:
            try:
                Item.insert(updated_item)
            except:
                {"message": "An error occured while inserting the item"},500
        else:
            try:
                Item.update(updated_item)
            except:
                {"message": "An error occured while updating the item"},500
        return item
    
class ItemList(Resource):
    def get(self):
        # return {'items':items}
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        query = "SELECT * FROM items"
        result = cur.execute(query)
        items = []
        for row in result:
            items.append({"name": row[0],"price": row[1]})
        conn.close()

        return {"items":items}
