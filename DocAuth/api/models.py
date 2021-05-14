from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from DocAuth.extensions import db


class Signature(db.Model):
    __tablename__ = "signature"

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    file_id = Column(Integer, ForeignKey('file.file_hash'), primary_key=True)
    sign_date = Column(Date, nullable=False, default=datetime.now())

    document = relationship("Document", back_populates="signers")
    signer = relationship("User", back_populates="signed_files")

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
    files = relationship("Document", backref="owner")
    signed_files = relationship("Signature", back_populates="signer")


class Document(db.Model):
    """
    This class represents the data for each file checked on the database.
    """
    __tablename__ = "file"
    file_hash = Column(String(64), nullable=False, unique=True, primary_key=True)
    filename = Column(String(100), nullable=False)
    date_added = Column(Date, nullable=False, default=datetime.now())
    date_expire = Column(Date)
    is_contract = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('user.id'))
    signers = relationship("Signature", back_populates="document")
