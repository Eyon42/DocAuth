from flask import request, jsonify, current_app
import jwt
import hashlib
from functools import wraps
import string

hex_digits = set(string.hexdigits)

def is_hex(s):
     return all(c in hex_digits for c in s)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get("token")

        if not token:
            return jsonify({"message" : "Token is missing"}), 403

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], "HS256")
        except Exception:
            return jsonify({"message" : "Token is invalid"}), 403

        return f(*args, **kwargs, user=data["user"])
    return decorated

def pw_hashf(pw):
    return hashlib.sha256(pw.encode()).hexdigest()