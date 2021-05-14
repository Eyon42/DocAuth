from DocAuth.extensions import ma
from .models import User, Document


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    name = ma.auto_field()
    username = ma.auto_field()
    register_date = ma.auto_field()
    is_org = ma.auto_field()


class RegisterSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ("username", "password", "name")


class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Document
        include_fk = True

user_schema = UserSchema()
doc_schema = DocumentSchema()
reg_user_schema = RegisterSchema()
