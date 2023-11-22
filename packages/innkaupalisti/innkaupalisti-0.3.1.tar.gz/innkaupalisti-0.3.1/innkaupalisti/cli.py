import click
from flask import current_app
from flask.cli import AppGroup
from innkaupalisti.app import db
import innkaupalisti.store as store


user_cli = AppGroup('user')


@user_cli.command('create')
@click.argument('name')
@click.argument('password')
def create_user(name, password):
    with current_app.app_context():
        store.User().create(name, password)
        db.session.commit()


current_app.cli.add_command(user_cli)
