#-*- coding=utf-8 -*-
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.models import *

manager = Manager(app)
migrate = Migrate(app, db)

app.jinja_env.globals['Post'] = Post

def make_shell_context():
    return dict(app=app, db=db)

@manager.command
def insert_admin():
    username='admin'
	#raw_input("please input the admin's username:")
    passwd='1234'
	#raw_input("please input the admin's password:")
    email='1234@qq.com'
	#raw_input("please input the admin's email:")
    user = User(email=email, username=username,password=passwd,)
    db.session.add(user)
    db.session.commit()


@manager.command
def init_data():
    db.drop_all()
    db.create_all()
    Role.insert_roles()

manager.add_command('Shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    # app.run(host='0.0.0.0',debug=True)