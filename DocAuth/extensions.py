from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Start database
db = SQLAlchemy()
migrate = Migrate()