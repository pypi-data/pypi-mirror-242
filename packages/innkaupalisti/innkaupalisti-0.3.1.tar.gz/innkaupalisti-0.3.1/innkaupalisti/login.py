import jwt
from flask import request, current_app
from flask_restful import Resource

from innkaupalisti import store


class Token(Resource):
    def post(self):
        try:
            user = store.User().login(
                    request.json['username'],
                    request.json['password'])
            response = {
                    'username': user.username,
                    'token': jwt.encode(
                        {'username': user.username},
                        current_app.config['SECRET_KEY'],
                        algorithm='HS256'),
                    }
            return response, 200
        except AttributeError:
            return '', 404
