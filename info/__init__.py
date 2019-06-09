import logging
from logging.handlers import RotatingFileHandler

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

def setup_log(config_name):
    # 设置日志的记录等级
    logging.basicConfig(level=logging.DEBUG)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("/home/python/PycharmProjects/news_website/logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

def create_app(config_name):
    setup_log(config_name)
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