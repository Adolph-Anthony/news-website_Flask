from flask import Flask ,session
from flask_script import Manager
from redis import StrictRedis
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
#可以用来指定session保存位置
from flask_session import Session
from flask_migrate import Migrate,MigrateCommand
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

#初始化数据库
db = SQLAlchemy(app)
#初始化redis 存储对象
redis_store = StrictRedis(host = Config.REDIS_HOST,port = Config.REDIS_PORT)
#开启当前项目CSRF 保护,只做服务器验证
CSRFProtect(app)
#设置Session保存指定位置
Session(app)

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
