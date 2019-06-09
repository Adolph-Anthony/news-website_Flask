from flask import Flask
from redis import StrictRedis
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

class Config(object):
    '''项目的配置'''
    DEBUG = True

    #数据库添加配置
    SQLALCHEMY_DATABASE_URI= "mysql://root:mysql@127.0.0.1:3306/website"
    SQLALCHEMY_TRACK_MODIFICATIONS = Flask

    #Redis 的 配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379


app = Flask(__name__)
app.config.from_object(Config)

#初始化数据库
db = SQLAlchemy(app)
#初始化redis 存储对象
redis_store = StrictRedis(host = Config.REDIS_HOST,port = Config.REDIS_PORT)
#开启当前项目CSRF 保护,只做服务器验证
CSRFProtect(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
