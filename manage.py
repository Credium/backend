import os

from flask_script import Manager, Shell
import pytest

from app.application import create_app, db, admin
from app.account.models import User, PublisherInfo, Follow
from app.demand.models import MeetingDemand, PersonDemand
from app.meeting.models import AbcMeeting, Participate

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
        return dict(app=app,
                    db=db,
                    admin=admin,
                    User=User,
                    PublisherInfo=PublisherInfo,
                    Follow=Follow,
                    MeetingDemand=MeetingDemand,
                    PersonDemand=PersonDemand,
                    Meeting=Meeting,
                    Participate=Participate,
                    )
    Shell(make_context=make_shell_context).run(False, False, False, False)


@manager.command
def create_all():
    tables_before = set(db.engine.table_names())
    db.create_all()
    tables_after = set(db.engine.table_names())
    created_tables = tables_after - tables_before
    for table in created_tables:
        print('Created table: {}'.format(table))


@manager.option('-u', '--username', default='admin')
@manager.option('-p', '--password', default='admin')
def create_admin(username, password):
    user = User(username=username, password=password, type="admin")
    try:
        db.session.add(user)
        db.session.commit()
        print("Created admin user: {}".format(user))
    except BaseException as e:
        db.session.rollback()
        print("Fail to create admin user")
        print("Error message: {}".format(e))


if __name__ == "__main__":
    manager.run()
