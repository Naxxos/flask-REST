from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "The store '{}' \
                    already exist".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured while \
                    creating the store'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            StoreModel.delete_from_db(name)

        return {'message': 'Store deleted'}, 201


class StoreList(Resource):
    def get(self):
        #list(map(lambda store : store.json(), StoreModel.query.all()))
        return {'stores': [store.json() for store in StoreModel.query.all()]}
