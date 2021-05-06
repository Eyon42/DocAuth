from faker import Faker
from datetime import datetime
import random
import hashlib


from DocAuth import create_app
from DocAuth.extensions import db
from DocAuth.models import Signature, User, Document
from DocAuth.api.utils import pw_hashf

app = create_app()

fake = Faker()

passwords = {}

with app.app_context():

    # Fake user accounts
    for i in range(5):
        name = fake.first_name()
        username = name.lower()+fake.postcode().replace(" ","").lower()
        passwd = fake.password()
        passwords[username] = passwd
        passwd_hash = pw_hashf(passwd)
        register_date = fake.date_between(start_date="-2y", end_date="today")
        user = User(name=name, username=username, passwd_hash=passwd_hash, register_date=register_date)

        db.session.add(user)
    
    db.session.commit()
    user_ids = [i[0] for i in db.session.query(User.id).all()]

    # Fake files
    for i in range(10):
        filename = fake.file_name()
        file_hash = hashlib.sha256(fake.binary()).hexdigest()
        if random.random() > 0.8:
            date_expire = fake.date_between(start_date="today", end_date="+30y")
        else:
            date_expire = None
        
        if filename.split(".")[-1] in ["pdf", "jpeg", "doc", "pptx", "txt", "bmp", "jpg"]:
            is_contract = True
        else:
            is_contract = False

        owner_id = random.choice(user_ids)

        date_added = fake.date_between_dates(db.session.get(User, owner_id).register_date, datetime.now())

        doc = Document(filename=filename, file_hash=file_hash, is_contract=is_contract,
                        date_expire=date_expire, owner_id=owner_id, date_added=date_added)
        db.session.add(doc)
    
    db.session.commit()
    contract_hashes = [i[0] for i in db.session.query(Document.file_hash).filter_by(is_contract=True).all()]

    # Fake signatures
    for i in range(30):
        document = db.session.get(Document, random.choice(contract_hashes))
        signer = db.session.get(User, random.choice(user_ids))

        earliest_date = max(document.date_added, signer.register_date)

        sign_date = fake.date_between_dates(earliest_date, datetime.now())

        pos_dup = db.session.get(Signature, (signer.id, document.file_hash))
        if pos_dup is None:
            sig = Signature(document=document, signer=signer, sign_date=sign_date)
            db.session.add(sig)
    
    db.session.commit()