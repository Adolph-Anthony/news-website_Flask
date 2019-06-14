import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from redis import StrictRedis
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, generate_csrf

#可以用来指定session保存位置
from flask_session import Session
from config import config

#初始化数据库
#在flask里很多扩展都可以先初始化扩展的对象,然后再去调用init_app方法去初始化
from info.utils.common import do_index_class

db = SQLAlchemy()

#变量的注释
redis_store = None  #type:StrictRedis

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
    #从对象中得到
    app.config.from_object(config[config_name])
    #初始化数据库
    db.init_app(app)
    #初始化redis 存储对象
    global redis_store
    redis_store = StrictRedis(host = config[config_name].REDIS_HOST,port = config[config_name].REDIS_PORT,decode_responses=True)
    #开启当前项目CSRF 保护,只做服务器验证
    #帮助我们做了 从cookie中取出随机值,从表单中取出随机值,然后进行对比,响应校验结果
    #我们需要做:1.在返回响应的时候,往cookie中添加一个csrf_token,2.并且在表单中添加一个隐藏的csrf_token
    #而我们登录注册不是使用的表单,而是使用一个ajax请求的时候带上csrf_token这个随机值就可以了
    CSRFProtect(app)
    #设置Session保存指定位置
    Session(app)
    #添加一个自定义过滤器
    app.add_template_filter(do_index_class,"index_class")


    @app.after_request
    def after_request(response):
        #生成一个随机的csrf_token
        csrf_token = generate_csrf()
        #设置一个cookie
        response.set_cookie("csrf_token",csrf_token)
        return response


    #注册蓝图
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    return app