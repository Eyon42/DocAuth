from datetime import datetime
from flask import Blueprint, request, current_app
from sqlalchemy.exc import NoResultFound
import jwt

from DocAuth.extensions import db
from .models import Document, User, Signature
from .schemas import reg_user_schema, doc_schema, verification_request
from .utils import token_required, pw_hashf, is_hex, validate_json

api = Blueprint("api", __name__, url_prefix="/api")

# Files

@api.route("/files/<file_hash>", methods=["GET"])
def getFiles(file_hash):
    doc = db.session.get(Document, file_hash)

    if not doc:
        return {"message" : "Invalid Hash"}, 404

    return doc_schema.dump(doc), 200


@api.route("/files", methods=["POST"])
@token_required
@validate_json(doc_schema)
def postFiles(user, validated_json_data):
    data = validated_json_data

    # Chech if hash is valid.
    if len(data["file_hash"]) != 64 or not is_hex(data["file_hash"]):
        return {"message" : "Invalid Hash"}, 400
    possible_dup = db.session.get(Document, data["file_hash"])
    if possible_dup is not None:
        return {"message" : "Hash already exists", "id" : possible_dup.file_hash}, 400

    # The user variable comes from the token_required decorator
    owner_id, = db.session.query(User.id).filter_by(username=user).first()

    doc = Document(**data, owner_id=owner_id)
    db.session.add(doc)
    db.session.commit()

    return doc_schema.dump(doc), 201


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

            return {"message" : "Signed file"}, 201
        return {"message" : "The file is not signable"}, 400
    return "Not found", 404


# Users

@api.route("/users/<user_id>", methods=["GET"])
def getUser(user_id):
    return {"message" : "WIP"}, 404


@api.route("/users/", methods=["GET"])
def searchUser():
    """
    Query arguments:
        - filter by : ["is_org", "register_date", "Verification type/level"]
    """
    return {"message" : "WIP"}, 404

# Verification
@api.route("/users/<user_id>/verification", methods=["GET"])
def showVerification(user_id):
    """
    List the user's account verifications.
    Only a user can access their own's verifications
    """
    return {"message" : "WIP"}, 404


@api.route("/users/<user_id>/verification/requests", methods=["GET", "POST"])
@token_required
@validate_json(verification_request)
def requestVerication(user, user_id, data=None):
    """
    GET: List the user's account verification requests.
    POST: Make a verification request.
    Only a user can access their own's verification requests
    """
    if request.method == "GET":
        pass
    else:
        pass
    return {"message" : "WIP"}, 404


# Auth
@api.route("/register", methods=["POST"])
@validate_json(reg_user_schema)
def register(validated_json_data):

    data = validated_json_data

    exists = db.session.query(User.id).filter_by(username=data["username"]).first() is not None
    if exists:
        return {"message" : "Username already exists"}, 400

    data["passwd_hash"] = pw_hashf(data.pop("password"))
    new_user = User(**data)

    db.session.add(new_user)
    db.session.commit()

    # Log the user in
    token = jwt.encode({"user" : data["username"],
                        "exp" : datetime.utcnow() + current_app.config["JWT_TOKEN_TIMEOUT"]},
                       current_app.config["SECRET_KEY"])

    return {"message" : "Registered Succefully! You are now logged in",
                    "token" : token}, 201


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
        return {"message" : "Auth failed. No credentials provided"}, 400

    # search username
    try:
        userpass = db.session.query(User.passwd_hash).filter_by(username=username).one()[0]
    except NoResultFound:
        userpass = None

    # verify password
    if pw_hashf(password) == userpass:
        token = jwt.encode({"user" : username,
                    "exp" : datetime.utcnow() + current_app.config["JWT_TOKEN_TIMEOUT"]},
                current_app.config["SECRET_KEY"])

        return {"token" : token}, 200

    return {"message" : "Incorrect Password/Username"}, 401


@api.route("/test/auth", methods=["GET"])
@token_required
def auth_check(user):
    # The user argument is nesessary even if it is not used by the endpoint.
    # It is sent as an argument by @token_required
    return {"Message" : "If you can see this, you are logged in"}
