from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel



#define our resource
#every resource has to be a class
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type = float,
    required = True,
    help = "This field cannot bbe left blank")

    parser.add_argument('store_id',
    type = int,
    required = True,
    help = "every item needs a store id")
    
    @jwt_required()
    #method like get post delete and so on
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': "item not found"}
    


    def post(self,name):
        
        if ItemModel.find_by_name(name):
            return {"message" : "An item with name '{}' already exists.".format(name)},400

        data = Item.parser.parse_args()

        #data = request.get_json()  # force = True silence = True
        item = ItemModel(name,data['price'],data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message":"An error occured inserting item"}, 500 #internal server error
        
        return item.json(),201



    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": 'item deleted'}

    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item is None:

            item = ItemModel(name,data['price'],data['store_id'])
        else:
            item.price = data['price']
        item.save_to_db()
            
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items' : [item.json() for item in ItemModel.query.all()]}
       