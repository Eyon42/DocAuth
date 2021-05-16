# pylint: disable=redefined-outer-name

from datetime import datetime, timedelta
import pytest
import jwt

import DocAuth
from DocAuth.extensions import db as _db
from .generate_test_data import create_fake_users, create_fake_files, create_fake_file_hash

@pytest.fixture
def app():
    app = DocAuth.create_app(test_config={
        "SQLALCHEMY_DATABASE_URI" : "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS" : 0,
        "SECRET_KEY" : 'secret-key',
        "JWT_TOKEN_TIMEOUT" : timedelta(days=2),
        "TESTING" : True
    })

    yield app


# This fixture must be ran before any tests which make requests
# which access the database, even if it is not used directly by them.
@pytest.fixture(autouse=True)
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def sample_user(app, db):
    with app.app_context():
        password = create_fake_users(1, db)
        username, password = list(password.items())[0]
        token = jwt.encode({"user" : username,
                        "exp" : datetime.utcnow() + app.config["JWT_TOKEN_TIMEOUT"]},
                       app.config["SECRET_KEY"])

        return {"username" : username, "password":password, "token":token}

@pytest.fixture
def sample_file(app, db):
    with app.app_context():
        test_file = create_fake_files(1, db)[0]
    return test_file


@pytest.fixture
def sample_contract(app, db):
    with app.app_context():
        test_file = create_fake_files(1, db, is_contract=True)[0]
    return test_file


@pytest.fixture
def file_hash():
    return create_fake_file_hash()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
