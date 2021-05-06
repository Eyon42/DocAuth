from flask import Blueprint, jsonify, request, current_app
from datetime import datetime, timedelta
import jwt

from ..models import Document, User, Signature
from ..extensions import db
from .utils import token_required, pw_hashf, is_hex

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/files/<id>", methods=["GET"])
def getFiles(id):
    if id:
        doc = db.session.get(Document, id)
    elif request.args.get("hash"):
        doc = db.session.query(Document).filter_by(file_hash=request.args.get("hash")).first()[0]
    else: 
        return jsonify({"message" : "No hash or file ID given"}), 400

    return jsonify({"filename" : doc.filename}), 200


@api.route("/files", methods=["POST"])
@token_required
def postFiles(user):
    filename = request.args["filename"]
    file_hash = request.args["hash"]
    if file_hash and filename:

        # Chech if hash is valid.
        if len(file_hash) != 64 or not is_hex(file_hash):
            return jsonify({"message" : "Invalid Hash"})
        possible_dup = db.session.query(Document.id).filter_by(file_hash=file_hash).first()
        if possible_dup is not None:
            return jsonify({"message" : "Hash already exists", "id" : possible_dup.id})

        if request.args.get("expire_date"):
            date_expire = request.args["expire_date"]
        else:
            date_expire = None

        owner_id, = db.session.query(User.id).filter_by(username=user).first() # The user variable comes from the token decorator

        doc = Document(filename=filename, file_hash=file_hash, date_expire=date_expire, owner_id=owner_id)
        db.session.add(doc)
        db.session.commit()

        return jsonify({"id" : doc.id}), 200

    return jsonify({"message" : "Please provide a hash and filename on the query"}), 400


@api.route("/files/<file_id>/signature", methods=["PUT"])
@token_required
def signFile(user, file_id):
    document = db.session.get(Document, file_id)
    signer = db.session.query(User).filter_by(username=user).first()
    signature = Signature(document=document, signer=signer)
    db.session.add(signature)
    db.session.commit()

    return jsonify({"message" : "Signed file"}), 200


@api.route("/register", methods=["POST"])
def register():
    username = request.json["user"]
    
    exists = db.session.query(User.id).filter_by(username=username).first() is not None
    if exists:
        return jsonify({"message" : "Username already exists"}), 400

    try:
        password = pw_hashf(request.json["password"])
        new_user = User(name=request.json["name"], username=username, passwd_hash=password)
    except Exception:
        return jsonify({"message" : "Missing fields for registering",
                        "username" : username, "password" : bool(password), "Name" : request.json["name"]}), 400

    db.session.add(new_user)
    db.session.commit()

    # Log the user in
    token = jwt.encode({"user" : username,
                        "exp" : datetime.utcnow() + current_app.config["JWT_TOKEN_TIMEOUT"]},
                       current_app.config["SECRET_KEY"])

    return jsonify({"message" : "Registered Succefully! You are now logged in",
                    "token" : token}), 200
    

@api.route("/login", methods=["GET"])
def login():
    auth = request.authorization
    if auth:
        # search username
        userpass = db.session.query(User.passwd_hash).filter_by(username=auth.username).first()[0]
        # verify password
        if pw_hashf(auth.password) == userpass:
            token = jwt.encode({"user" : auth.username,
                        "exp" : datetime.utcnow() + current_app.config["JWT_TOKEN_TIMEOUT"]},
                       current_app.config["SECRET_KEY"])

            return jsonify({"token" : token})

    return jsonify({"message" : "Auth failed"}), 401


@api.route("/test/auth", methods=["GET"])
@token_required
def test_auth():
    return jsonify({"Message" : "If you can see this, you are logged in"})


@api.route("/test/unauth", methods=["GET"])
def test_unauth():
    return jsonify({"Message" : "Everyone should be able to see this"})

