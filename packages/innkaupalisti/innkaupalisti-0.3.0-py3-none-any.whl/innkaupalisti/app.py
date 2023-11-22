import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        # default database
        app.config['SQLALCHEMY_DATABASE_URI'] =\
                'sqlite:///database.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # FLASK_*
        app.config.from_prefixed_env()
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    api = Api(app)
    import innkaupalisti.store  # noqa: F401
    with app.app_context():
        db.create_all()
        from . import cli  # noqa: F401

    from .list import Lists, List, ListItems, ListItem
    from .login import Token
    api.add_resource(Token, '/api/v0/login/token')
    api.add_resource(Lists, '/api/v0/lists')
    api.add_resource(List, '/api/v0/lists/<name>')
    api.add_resource(ListItems, '/api/v0/lists/<name>/items')
    api.add_resource(ListItem, '/api/v0/lists/<list_name>/items/<item_name>')

    return app
