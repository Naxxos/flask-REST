from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="You have to specify a username"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="You have to specify a password"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        # Vérification que l'utilisateur n'est pas déjà inscrit
        if UserModel.find_by_username(data['username']):
            return {"message": "An item with name \
                '{}' already exists.".format(data['username'])}, 400

        # data is a dict with keys username/password
        # as described by the parser.
        # user = UserModel(**data)

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201
