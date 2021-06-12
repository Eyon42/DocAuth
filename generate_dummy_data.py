from DocAuth import create_app
from DocAuth.extensions import db

from tests.generate_test_data import create_fake_users, create_fake_files, create_fake_signatures

def create_fake_data():
    app = create_app()

    with app.app_context():

        # Fake user accounts
        create_fake_users(5, db)

        create_fake_files(10, db, commit=True, is_contract=True)
        create_fake_files(5, db, commit=True)
        # Fake files
        create_fake_signatures(8, db)

        # Fake signatures
        create_fake_signatures(13, db)

if __name__ == "__main__":
    create_fake_data()
