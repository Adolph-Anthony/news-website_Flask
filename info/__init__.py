from flask import Flask
from redis import StrictRedis
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

#可以用来指定session保存位置
from flask_session import Session
from config import config

#初始化数据库
#在flask里很多扩展都可以先初始化扩展的对象,然后再去调用init_app方法去初始化
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    #初始化数据库
    db.init_app(app)
    #初始化redis 存储对象
    redis_store = StrictRedis(host = config[config_name].REDIS_HOST,port = config[config_name].REDIS_PORT)
    #开启当前项目CSRF 保护,只做服务器验证
    CSRFProtect(app)
    #设置Session保存指定位置
    Session(app)

    return app