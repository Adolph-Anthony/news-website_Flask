from flask import g
from flask import redirect
from flask import render_template
from flask import request

from info.modules.profile import profile_blu
from info.utils.common import user_login_data


@profile_blu.route("/base_info",methods= ["POST","GET"])
@user_login_data
def base_info():
    if request.method == "GET":
        data = {

            "user": g.user.to_dict()
        }
        return render_template("news/user_base_info.html",data=data)
    # TODO 修改用户数据
    if request.method == "POST":
        pass


@profile_blu.route("/info")
@user_login_data
def user_info():
    user = g.user

    # 没有登录重定向到首页
    if not user:
        return redirect("/")

    data = {

        "user":user.to_dict()
    }
    return render_template("news/user.html",data = data)