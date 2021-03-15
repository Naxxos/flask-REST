import sqlite3
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
            return {"message": "An item with name '{}' already exists.".format(data['username'])}, 400

        # Connection après la vérif sinon elle peut ne jamais être close()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Si l'utilisateur n'existe pas dans la db, l'ajouter
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
