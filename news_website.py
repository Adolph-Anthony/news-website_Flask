from flask import session
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from info import app,db


manager = Manager(app)
#将app与db关联
Migrate(app,db)
#将迁移命令添加到manager中
manager.add_command("db",MigrateCommand)

manager = Manager(app)
@app.route('/')
def hello_world():
    session["name"] = "itheima"
    return 'Hello World!'


if __name__ == '__main__':
    manager.run()
