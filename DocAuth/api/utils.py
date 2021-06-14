import hashlib
import string
from functools import wraps
from flask import request, current_app
from marshmallow import ValidationError
import jwt

from .models import User

DATE_FORMAT = "%Y-%m-%d"

hex_digits = set(string.hexdigits)

def is_hex(s):
    return all(c in hex_digits for c in s)

def token_required(admin=False):
    def token_wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.args.get("token")

            if not token:
                return {"message" : "Token is missing"}, 403

            try:
                data = jwt.decode(token, current_app.config["SECRET_KEY"], "HS256")
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return {"message" : "Token is invalid"}, 403

            if admin:
                is_admin = User.query.filter_by(username=data["user"]).first().admin
                if not is_admin:
                    return {"message" : "Restricted"}, 403

            return f(*args, **kwargs, user=data["user"])
        return decorated
    return token_wrapper

def validate_json(schema):
    """
    Validates json schemas for POST and PUT requests.
    It's ignored for other requests
    """
    def decorated(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.method in ["POST", "PUT"]:
                try:
                    # Validate request body against schema data types
                    data = schema.load(request.json)
                except ValidationError as err:
                    # Return a nice message if validation fails
                    return err.messages, 400
                return f(*args, **kwargs, validated_json_data=data)
            return f(*args, **kwargs)
        return wrapper
    return decorated

def pw_hashf(pw):
    return hashlib.sha256(pw.encode()).hexdigest()
