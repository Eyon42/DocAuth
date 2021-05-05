from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Boolean
from datetime import datetime, timedelta
from functools import wraps
import os
import jwt
import hashlib

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'secret-key'

db = SQLAlchemy(app)


class User(db.Model):
    """
    Can be created as a regular user(No Org) or Org user
    But 
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    passwd_hash = Column(String(64), nullable=False)
    register_date = Column(Date, nullable=False)
    is_org = Column(Boolean, default=False)
    # files


class Document(db.Model):
    """
    This class represents the data for each file checked on the database.
    """
    id = Column(Integer, primary_key=True)
    filename = Column(String(100), nullable=False)
    file_hex_hash = Column(String(64), nullable=False)
    date_added = Column(Date, nullable=False)
    date_expire = Column(Date)
    is_contract = Column(Boolean)
    # owner = Just one nullable=False
    # signers = For contracts can be null


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get("token")

        if not token:
            return jsonify({"message" : "Token is missing"}), 403

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], "HS256")
        except Exception:
            return jsonify({"message" : "Token is invalid"}), 403

        return f(*args, **kwargs)
    return decorated

def pw_hashf(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

@app.route("/file_hash/<file_hash>", methods=["GET"])
def checkFile(file_hash):
    pass

@app.route("/file_hash", methods=["POST"])
def registerFile():
    # Auth

    # Check if the hash is valid
    if len(request.json["file_hex_hash"]) != 64:
        return jsonify({"response" : "Invalid SHA256 Hash"})

    # Create database entry
    args = dict(**request.json, date_added=datetime.today())
    new_file = Document(**args)
    db.session.add(new_file)
    db.session.commit()

    # Return confirmation
    return jsonify(args), 200


@app.route("/sign/{file_id}{file_hash}", methods=["PUT"])
def signFile():
    pass


@app.route("/register", methods=["POST"])
def register():
    username = request.json["user"]
    
    exists = db.session.query(User.id).filter_by(name=username).first() is not None
    if exists:
        return jsonify({"message" : "Username already exists"}), 400

    try:
        password = pw_hashf(request.json["password"])
        new_user = User(name=request.json["name"], username=username, passwd_hash=password, register_date=datetime.today())
    except Exception:
        return jsonify({"message" : "Missing fields for registering",
                        "username" : username, "password" : bool(password), "Name" : request.json["name"]}), 400

    db.session.add(new_user)
    db.session.commit()

    # Log the user ins
    token = jwt.encode({"user" : username, "exp" : datetime.utcnow() + timedelta(minutes=30)}, app.config["SECRET_KEY"])

    return jsonify({"message" : "Registered Succefully! You are now logged in",
                    "token" : token}), 200
    

@app.route("/login", methods=["GET"])
def login():
    auth = request.authorization
    if auth:
        # search username
        userpass = db.session.query(User.passwd_hash).filter_by(username=auth.username).first()[0]
        # verify password
        if pw_hashf(auth.password) == userpass:
            token = jwt.encode({"user" : auth.username, "exp" : datetime.utcnow() + timedelta(minutes=30)}, app.config["SECRET_KEY"])

            return jsonify({"token" : token})

    return jsonify({"message" : "Auth failed"}), 401


@app.route("/test/auth", methods=["GET"])
@token_required
def test_auth():
    return jsonify({"Message" : "If you can see this, you are logged in"})

@app.route("/test/unauth", methods=["GET"])
def test_unauth():
    return jsonify({"Message" : "Everyone should be able to see this"})


if __name__ == "__main__":
    app.run(debug=True)