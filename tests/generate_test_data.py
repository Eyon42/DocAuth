from datetime import datetime
import random
import hashlib
from faker import Faker


from DocAuth import create_app
from DocAuth.extensions import db
from DocAuth.api.models import Signature, User, Document
from DocAuth.api.utils import pw_hashf

fake = Faker()


def create_fake_users(n, database, commit=True, is_org=False):
    """
    Creates n fake users and add them to the database
    If commit (default=True), commits the changes.
    Must be run inside an app context
    """
    passwords = {}

    for _ in range(n):
        name = fake.first_name()
        username = name.lower()+fake.postcode().replace(" ","").lower()
        passwd = fake.password()
        passwords[username] = passwd
        passwd_hash = pw_hashf(passwd)
        register_date = fake.date_between(start_date="-2y", end_date="today")
        user = User(name=name, username=username, passwd_hash=passwd_hash,
                    register_date=register_date, is_org=is_org)

        database.session.add(user)

    if commit:
        database.session.commit()
    return passwords


def create_fake_file_hash():
    """
    Creates a random sha256 hash
    """
    return hashlib.sha256(fake.binary()).hexdigest()


def create_fake_files(n, database, commit=True, is_contract=False):
    """
    Creates n fake files and add them to the database
    If commit (default=True), commits the changes.
    Must be run inside an app context
    """
    user_ids = [i[0] for i in database.session.query(User.id).all()]
    file_ids = []

    for _ in range(n):
        filename = fake.file_name()
        file_hash = create_fake_file_hash()
        if random.random() > 0.8:
            date_expire = fake.date_between(start_date="today", end_date="+30y")
        else:
            date_expire = None

        owner_id = random.choice(user_ids)

        date_added = fake.date_between_dates(database.session.get(User, owner_id).register_date,
                                             datetime.now())

        doc = Document(filename=filename, file_hash=file_hash, is_contract=is_contract,
                        date_expire=date_expire, owner_id=owner_id, date_added=date_added)
        database.session.add(doc)
        file_ids.append(doc.file_hash)

    if commit:
        database.session.commit()

    return file_ids


def create_fake_signatures(n, database, commit=True):
    """
    Creates (at most) n fake signatures and add them to the database
    If commit (default=True), commits the changes.
    Must be run inside an app context
    """
    contracts = database.session.query(Document.file_hash).filter_by(is_contract=True).all()
    contract_hashes = [i[0] for i in contracts]
    user_ids = [i[0] for i in database.session.query(User.id).all()]

    for _ in range(n):
        document = database.session.get(Document, random.choice(contract_hashes))
        signer = database.session.get(User, random.choice(user_ids))

        earliest_date = max(document.date_added, signer.register_date)

        sign_date = fake.date_between_dates(earliest_date, datetime.now())

        pos_dup = database.session.get(Signature, (signer.id, document.file_hash))
        if pos_dup is None:
            sig = Signature(document=document, signer=signer, sign_date=sign_date)
            database.session.add(sig)

    if commit:
        database.session.commit()
    return


if __name__ == "__main__":
    create_fake_data()
