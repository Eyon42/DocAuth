from flask import Flask

from .api.endpoints import api
from .extensions import db, migrate

def create_app(config_file="settings.py"):
    # app
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    app.register_blueprint(api)

    db.init_app(app)
    migrate.init_app(app, db)

    return app