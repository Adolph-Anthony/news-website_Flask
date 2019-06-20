from flask import current_app
from flask import g, jsonify
from flask import redirect
from flask import render_template
from flask import request

from info import constants
from info.modules.profile import profile_blu
from info.templates.image_storage import storage
from info.utils.common import user_login_data
from info.utils.response_code import RET


@profile_blu.route("/pic_info", methods=["POST", "GET"])
@user_login_data
def pic_info():
    user = g.user
    if request.method == "GET":
        data = {

            "user": user.to_dict()
        }
        return render_template("news/user_pic_info.html", data=data)
    # 如果是 POST表示修改头像
    # 1.取到上传的图片
    try:
        avatar = request.files.get("avatar").read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    # 2.上传图片
    try:
        key = storage(avatar)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传图片失败")

    user.avatar_url = key
    return jsonify(errno = RET.OK,errmsg = "OK",avatar_url = constants.QINIU_DOMIN_PREFIX + key )

@profile_blu.route("/base_info", methods=["POST", "GET"])
@user_login_data
def base_info():
    if request.method == "GET":
        data = {

            "user": g.user.to_dict()
        }
        return render_template("news/user_base_info.html", data=data)

    '''
    修改用户数据
    传入参数
    参数名	    类型  	是否必须	参数说明
    nick_name	string	是	    昵称
    signature	string	是	    签名
    gender	    string	是	    性别, MAN / WOMEN

    传出参数
    参数名	    类型	    是否必须	参数说明
    errno	    int	    是	    错误码
    errmsg	    string	是	    错误信息
    '''
    # 1.取到传入的参数
    nick_name = request.json.get("nick_name")
    signature = request.json.get("signature")
    gender = request.json.get("gender")

    # 2.校验参数
    if not all([nick_name, signature, gender]):
        return jsonify(errno=RET.PARAMERR, error="参数错误")
    if gender not in (["MAN", "WOMEN"]):
        return jsonify(errno=RET.PARAMERR, error="参数错误")
    # 保存参数
    user = g.user
    user.signature = signature
    user.nick_name = nick_name
    user.gender = gender
    # user已经存在并且会自动commit()

    return jsonify(errno=RET.OK, errmsg="OK")


@profile_blu.route("/info")
@user_login_data
def user_info():
    user = g.user

    # 没有登录重定向到首页
    if not user:
        return redirect("/")

    data = {

        "user": user.to_dict()
    }
    return render_template("news/user.html", data=data)
