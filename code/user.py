import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        # Execute need a tuple in parameters
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        # Execute need a tuple in parameters
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


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
        if User.find_by_username(data['username']):
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
