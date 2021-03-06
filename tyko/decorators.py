from functools import wraps
from flask import request
from flask import make_response
from flask import current_app as app


def validate_users(username, password):
    return username == app.config['USERNAME'] and \
           password == app.config['PASSWORD']


def authenticate(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not validate_users(auth.username, auth.password):
            resp = make_response("", 401)
            resp.headers["WWW-Authenticate"] = 'Basic realm="Login Required'
            return resp
        return func(*args, **kwargs)
    return decorated
