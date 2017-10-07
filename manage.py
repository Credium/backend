import os

from flask_script import Manager, Shell
import pytest

from app import create_app, db
from app.account.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def runserver():
    app.run()


@manager.command
def test():
    pytest.main(['-x', 'tests'])


@manager.command
def shell():
    def make_shell_context():
        return dict(app=app, db=db, User=User)
    Shell(make_context=make_shell_context).run(False, False, False, False)


@manager.command
def create_all():
    tables_before = set(db.engine.table_names())
    db.create_all()
    tables_after = set(db.engine.table_names())
    created_tables = tables_after - tables_before
    for table in created_tables:
        print('Created table: {}'.format(table))


if __name__ == "__main__":
    manager.run()
