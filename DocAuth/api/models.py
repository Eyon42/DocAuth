from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import PickleType

from DocAuth.extensions import db


# Metadata Tables


signature_permissions = Table('signature_permission', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('file_id', Integer, ForeignKey('file.file_hash'))
)


# Data Tables


class User(db.Model):
    """
    Can be created as a regular user(No Org) or Org user
    But
    """
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    passwd_hash = Column(String(64), nullable=False)
    register_date = Column(Date, nullable=False, default=datetime.now())
    is_org = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)

    verification = relationship("VerificationData")

    files = relationship("Document", back_populates="owner")

    signed_files = relationship("Signature", back_populates="signer")
    allowed_files_to_sign = relationship("Document",
                                         secondary=signature_permissions,
                                         back_populates="allowed_signers")


class Document(db.Model):
    """
    This class represents the data for each file checked on the database.
    """
    __tablename__ = "file"
    file_hash = Column(String(64), nullable=False, unique=True, primary_key=True)
    filename = Column(String(100), nullable=False)
    date_added = Column(Date, nullable=False, default=datetime.now())
    date_expire = Column(Date)

    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship("User", back_populates="files")

    # Contract stuff
    is_contract = Column(Boolean, default=False)
    whitelist_signers = Column(Boolean, default=False)
    signers = relationship("Signature", back_populates="document")
    allowed_signers = relationship("User",
                                   secondary=signature_permissions,
                                   back_populates="allowed_files_to_sign")


class Signature(db.Model):
    __tablename__ = "signature"

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    file_id = Column(Integer, ForeignKey('file.file_hash'), primary_key=True)
    sign_date = Column(Date, nullable=False, default=datetime.now())

    document = relationship("Document", back_populates="signers")
    signer = relationship("User", back_populates="signed_files")


class VerificationData(db.Model):
    __tablename__ = "verification_data"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    type = Column(String(50), nullable=False)
    data = Column(PickleType, nullable=False)
    status = Column(String(50), nullable=False) # Can be "In Process", "Verified" or "Expired"
    request_date = Column(Date, nullable=False, default=datetime.now())
    verification_date = Column(Date)
