import json

from marshmallow import Schema, fields, decorators

from DocAuth.extensions import ma
from .models import User, Document, VerificationData


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    name = ma.auto_field()
    username = ma.auto_field()
    register_date = ma.auto_field()
    is_org = ma.auto_field()


class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Document
        include_fk = True


class VerificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VerificationData
        include_fk = True

    @decorators.post_dump
    def deserialize_pickle_bin(self, data, **kwargs):
        # pylint: disable=unused-argument
        # For some reason, marshmallow serializes the dict to a string.
        # So this is nesessary.
        data["data"] = json.loads(data["data"].replace("'", "\""))
        return data

# Useful validators

class RegisterSchema(Schema):
    username = fields.Str()
    password = fields.Str()
    name = fields.Str()

# Verification data schemas

ver_data_validators = dict()

class PhoneVerData(Schema):
    number = fields.Str()
ver_data_validators["phone"] = PhoneVerData()

class EmailVerData(Schema):
    mail = fields.Str()
ver_data_validators["e-mail"] = EmailVerData()

class WebsiteVerData(Schema):
    site = fields.Str()
ver_data_validators["website"] = WebsiteVerData()

class PhoneInterviewVerData(Schema):
    interviewer_name = fields.Str()
    interviewer_contact = fields.Str()
    notes = fields.Str()
ver_data_validators["phone-interview"] = PhoneInterviewVerData()

# Instanciate all

user_schema = UserSchema()
doc_schema = DocumentSchema()
reg_user_schema = RegisterSchema()
verification_schema = VerificationSchema()
