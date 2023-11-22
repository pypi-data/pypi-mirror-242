from functools import wraps
import jwt
from flask import request, current_app
from innkaupalisti import store


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers['Authorization'].split(' ')[1]
            data = jwt.decode(
                    token,
                    current_app.config['SECRET_KEY'],
                    algorithms=['HS256'])
            user = store.User().get_by_username(data['username'])
            return f(user, *args, **kwargs)
        except KeyError:
            return '', 401

    return decorated
