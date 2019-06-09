from flask import Flask ,session
from flask_script import Manager
from redis import StrictRedis
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
#可以用来指定session保存位置
from flask_session import Session
from flask_migrate import Migrate,MigrateCommand


class Config(object):
    '''项目的配置'''
    DEBUG = True

    SECRET_KEY = "Wub8dLQfSWgqpyEkUieJVzYX1bVY61/cE1npjbJhlzm57qTPpnDzn3Yvu2j2DMGU"

    #数据库添加配置
    SQLALCHEMY_DATABASE_URI= "mysql://root:mysql@127.0.0.1:3306/website"
    SQLALCHEMY_TRACK_MODIFICATIONS = Flask

    #Redis 的 配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    #Session保存配置
    SESSION_TYPE = "redis"
    #开启session签名
    SESSION_USE_SIGNER = True
    #制定Session 保存的 redis
    SESSION_REDIS = StrictRedis(host= REDIS_HOST,port=REDIS_PORT)
    #设置session需要过期
    SESSION_PERMANENT = False
    #设置过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2




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
