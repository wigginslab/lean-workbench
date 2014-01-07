from flask.ext.security import current_user, AnonymousUser
from functools import wraps
from flask import abort

def authenticate_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
    	print args
    	print kwargs
        if current_user and current_user.is_authenticated():
            return func(*args, **kwargs)
        abort(401)

    return wrapper
