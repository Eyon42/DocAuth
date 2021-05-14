from datetime import datetime
from flask import Blueprint, jsonify, request, current_app
import jwt

from DocAuth.extensions import db
from .models import Document, User, Signature
from .schemas import reg_user_schema, doc_schema
from .utils import token_required, pw_hashf, is_hex, validate_json

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/files/<file_hash>", methods=["GET"])
def getFiles(file_hash):
    doc = db.session.get(Document, file_hash)

    if not doc:
        return jsonify({"message" : "Invalid Hash"}), 400

    return jsonify(doc_schema.dump(doc)), 200


@api.route("/files", methods=["POST"])
@token_required
@validate_json(doc_schema)
def postFiles(user, validated_json_data):
    data = validated_json_data

    # Chech if hash is valid.
    if len(data["file_hash"]) != 64 or not is_hex(data["file_hash"]):
        return jsonify({"message" : "Invalid Hash"})
    possible_dup = db.session.get(Document, data["file_hash"])
    if possible_dup is not None:
        return jsonify({"message" : "Hash already exists", "id" : possible_dup.id})

    # The user variable comes from the token_required decorator
    owner_id, = db.session.query(User.id).filter_by(username=user).first()

    doc = Document(**data, owner_id=owner_id)
    db.session.add(doc)
    db.session.commit()

    return jsonify(doc_schema.dump(doc)), 201


@api.route("/files/<file_hash>/signature", methods=["PUT"])
@token_required
def signFile(user, file_hash):
    document = db.session.get(Document, file_hash)

    if document:
        if document.is_contract:
            signer = db.session.query(User).filter_by(username=user).first()
            signature = Signature(document=document, signer=signer)
            db.session.add(signature)
            db.session.commit()

            return jsonify({"message" : "Signed file"}), 201
        return jsonify({"message" : "The file is not signable"}), 400
    return "Not found", 404

@api.route("/register", methods=["POST"])
@validate_json(reg_user_schema)
def register(validated_json_data):

    data = validated_json_data

    exists = db.session.query(User.id).filter_by(username=data["username"]).first() is not None
    if exists:
        return jsonify({"message" : "Username already exists"}), 400

    data["passwd_hash"] = pw_hashf(data.pop("password"))
    new_user = User(**data)

    db.session.add(new_user)
    db.session.commit()

    # Log the user in
    token = jwt.encode({"user" : data["username"],
                        "exp" : datetime.utcnow() + current_app.config["JWT_TOKEN_TIMEOUT"]},
                       current_app.config["SECRET_KEY"])

    return jsonify({"message" : "Registered Succefully! You are now logged in",
                    "token" : token}), 201


@api.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if auth:
        username = auth.username
        password = auth.password
    elif request.json:
        username = request.json["username"]
        password = request.json["password"]
    else:
        return jsonify({"message" : "Auth failed. No credentials provided"}), 401

    # search username
    userpass = db.session.query(User.passwd_hash).filter_by(username=username).first()[0]
    # verify password
    if pw_hashf(password) == userpass:
        token = jwt.encode({"user" : username,
                    "exp" : datetime.utcnow() + current_app.config["JWT_TOKEN_TIMEOUT"]},
                current_app.config["SECRET_KEY"])

        return jsonify({"token" : token}), 200

    return jsonify({"message" : "Incorrect Password/Username"}), 401


@api.route("/test/auth", methods=["GET"])
@token_required
def auth_check(user):
    return jsonify({"Message" : "If you can see this, you are logged in"})
