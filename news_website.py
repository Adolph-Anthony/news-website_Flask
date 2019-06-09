from flask import current_app
from flask import session
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
import logging
from info import db, create_app

#news_website.py是程序启动入口,不存放业务逻辑


#通过指定的配置名字创建对应配置的app
#工厂方法
app = create_app("development")
manager = Manager(app)

#将app与db关联
Migrate(app,db)
#将迁移命令添加到manager中
manager.add_command("db",MigrateCommand)

manager = Manager(app)



if __name__ == '__main__':
    manager.run()
