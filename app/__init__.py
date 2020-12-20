import click
from flask.cli import with_appcontext
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app

from config import set_config

db = SQLAlchemy()
migration = Migrate()


@click.command(name='create_db', help='In theory it build the database')
@with_appcontext
def db_creation():
    current_app.config.from_object(set_config())
    db.create_all()


def create_app(config=None):
    app = Flask(__name__)
    try:
        app.config.from_object(config)
    except:
        print('Error in loading the configuration.')
        return None
    db.init_app(app)
    with app.app_context():
        # TODO tests
        # TODO migration
        migration.init_app(app, db)
        # TODO register blueprint
        from app.main import main
        app.register_blueprint(main)
        # TODO add command to do things on the database
        app.cli.add_command(db_creation)
    return app
