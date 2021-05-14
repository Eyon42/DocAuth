from flask import Flask

from .api.endpoints import api
from .extensions import db, migrate, ma

def create_app(test_config=None):
    # app
    app = Flask(__name__)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("settings.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    app.register_blueprint(api)

    db.init_app(app)
    ma.init_app(app)

    if not app.config["TESTING"]:
        migrate.init_app(app, db)

    return app
