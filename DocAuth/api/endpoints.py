from datetime import datetime
import re
from typing import ValuesView
from flask import Blueprint, request, current_app, jsonify
from sqlalchemy.exc import NoResultFound
from sqlalchemy import or_
import jwt

from DocAuth.extensions import db
from .models import Document, User, Signature
from .schemas import reg_user_schema, doc_schema, verification_request, user_schema, verification_schema
from .utils import token_required, pw_hashf, is_hex, validate_json, DATE_FORMAT

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

@api.route("/users/<int:user_id>", methods=["GET"])
def getUser(user_id):
    user = User.query.get(user_id)

    if user:
        return user_schema.dump(user), 200

    return {"message" : "User not found"}, 404


@api.route("/users/", methods=["GET"])
def searchUser():
    """
    Query arguments:
        - search : ["search"]
        - filter by : ["is_org", "register_date_from", "register_date_until", "verification"]
        - pagination : ["per_page", "page"]
    """

    args = request.args

    query = User.query

    if search_q := args.get("search"):
        query = query.filter(or_(
                *[
                    i.like(f"%{search_q}%")
                    for i in [
                        User.name,
                        User.username,
                    ]
                ]
            ))

    if args.get("is_org") == "True":
        query = query.filter_by(is_org=True)
    elif args.get("is_org") == "False":
        query = query.filter_by(is_org=False)

    # Maybe try to avoid duplication for date ranges
    if from_date_str := args.get("register_date_from"):
        try:
            from_date = datetime.strptime(from_date_str, DATE_FORMAT)
            query = query.filter(User.register_date >= from_date)
        except ValueError:
            return {"message" : f"Invalid date format, correct format is '{DATE_FORMAT}'"}

    if from_date_str := args.get("register_date_until"):
        try:
            until_date = datetime.strptime(from_date_str, DATE_FORMAT)
            query = query.filter(User.register_date <= until_date)
        except ValueError:
            return {"message" : f"Invalid date format, correct format is '{DATE_FORMAT}'"}

    # Verification filtering
    if v_types := args.get("verification"):
        query = query.filter(User.verification.in_(v_types))
    
    # Pagination
    if per_page := args.get("per_page"):
        per_page = int(per_page)
        if page := args.get("page"):
            page = int(page)
        else:
            page = 1
        
        pagination = query.paginate(per_page=per_page, page=page, error_out=True)
        
        return {
            "users" : [user_schema.dump(i) for i in pagination.items],
            "page" : page,
            "has_prev" : pagination.has_prev,
            "has_next" : pagination.has_next,
        }, 200

    # Flask does not jsonify lists automatically, like it does with dicts
    return jsonify([user_schema.dump(i) for i in query.all()]), 200

# Verification
@api.route("/users/<username>/verification", methods=["GET"])
@token_required
def showVerification(user, username):
    if user != username:
        return {"message" : f"You are not {username}"}, 401

    user = User.query.filter_by(username=user).first()
    """
    List the user's account verifications.
    Only a user can access their own's verifications
    """
    
    return {"verification:" : [verification_schema.dump(i) for i in user.verification]}, 404


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
    return {"message" : "WIP"}, 200


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
    return {"Message" : "If you can see this, you are logged in", "username":user}
