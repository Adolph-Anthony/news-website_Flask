from flask import Flask
from redis import StrictRedis
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

#可以用来指定session保存位置
from flask_session import Session
from config import config

app = Flask(__name__)
app.config.from_object(config["development"])

#初始化数据库
db = SQLAlchemy(app)
#初始化redis 存储对象
redis_store = StrictRedis(host = config["development"].REDIS_HOST,port = config["development"].REDIS_PORT)
#开启当前项目CSRF 保护,只做服务器验证
CSRFProtect(app)
#设置Session保存指定位置
Session(app)