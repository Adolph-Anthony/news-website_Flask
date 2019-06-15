import functools
#公用的自定义工具类
from flask import current_app
from flask import g
from flask import session

from info.models import User


def do_index_class(index):
    '''
    返回制定索引对应的类名
    :return:
    '''
    if index == 0:
        return "first"
    elif index ==1:
        return "second"
    elif index==2:
        return "third"

    return ""

def user_login_data(f):
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        user_id = session.get("user_id", None)
        user = None
        if user_id:
            # 去数据库里查询指定id的模型
            try:
                user = User.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)
        g.user = user
        return f(*args,**kwargs)

    return wrapper




# def query_user_data():
#     # 显示用户是否登录的逻辑
#     # 取到用户id
#     user_id = session.get("user_id", None)
#     user = None
#     if user_id:
#         # 去数据库里查询指定id的模型
#         try:
#             user = User.query.get(user_id)
#         except Exception as e:
#             current_app.logger.error(e)
#         return user