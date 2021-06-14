"""
This is an instance of the DocAuth app without the api module.
It is meant to serve as an interface for the celery worker to access
the database.
"""
from flask import Flask

from DocAuth.extensions import db, migrate, ma

def create_app(test_config=None):
    # app
    app = Flask(__name__)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("../DocAuth/settings.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    db.init_app(app)
    ma.init_app(app)

    if not app.config["TESTING"]:
        migrate.init_app(app, db)

    return app