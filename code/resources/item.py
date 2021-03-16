from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    # permet de vérifier le format des données et d'obliger la présence de certains paramètres
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="this field cannot be left blank"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 400

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500
            # internal server error
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data["price"])
        else:
            item.price = data["price"]

        item.save_to_db()

        return item.json(), 201


class ItemList(Resource):
    def get(self):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        cursor.execute(query)

        items = []

        for row in cursor:
            items.append({"name": row[0], "price": row[1]})

        connection.close()

        return items, 201
