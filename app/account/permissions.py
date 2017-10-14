from functools import wraps

from flask import g, jsonify


def publisher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is not None and g.user.is_publisher:
            return f(*args, **kwargs)
        return jsonify("this user is not publisher"), 401
    return decorated_function
