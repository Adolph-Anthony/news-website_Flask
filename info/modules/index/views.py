from flask import current_app
from flask import render_template

from info import redis_store
from . import index_blu
@index_blu.route('/')
def hello_world():
    #向redis中保存一个值
    return render_template("news/index.html")

#加载favicon.ico图标
#send_static_file是flask把静态文件从静态文件夹发送到浏览器
@index_blu.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")