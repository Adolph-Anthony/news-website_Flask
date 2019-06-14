from flask import current_app
from flask import render_template
from flask import session

from info import redis_store
from info.models import User
from . import index_blu
@index_blu.route('/')
def index():
    '''
    显示首页
    1.如果用户已经登录,将当前登录用户数据传到模板中,以供显示
    :return:
    '''
    #取到用户id
    user_id = session.get("user_id",None)
    user = None
    if user_id:
        #去数据库里查询指定id的模型
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    data = {
        "user":user.to_dict() if user else None
    }

    return render_template("news/index.html",data = data)

#加载favicon.ico图标
#send_static_file是flask把静态文件从静态文件夹发送到浏览器
@index_blu.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")