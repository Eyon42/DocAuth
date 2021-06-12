# Spec
Database: SQLite
ORM: SQLAlchemy
Migrations: Alembic with flask-migrate

# Database migrations
Migration Workflow

From this point on you have a project that is fully enabled to use database migrations. The normal migration process goes as follows:

1. You will make some changes to your models in your Python source code.
2. You will then run flask db migrate to generate a new database migration for these changes.
3. You will finally apply the changes to the database by running flask db upgrade.

This cycle repeats every time new changes to the database schema are needed.
[Source](https://blog.migflauelgrinberg.com/post/how-to-add-flask-migrate-to-an-existing-project)

## commands

```
flask db init
flask db migrate
flask db upgrade
```