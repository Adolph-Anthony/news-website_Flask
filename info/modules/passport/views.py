
from flask import abort
from flask import current_app
from flask import make_response
from flask import render_template
from flask import request

from info import constants, redis_store
from info.utils.captcha.captcha import captcha
from . import passport_blu

@passport_blu.route('/image_code')
def get_image_code():
    '''
    生成图片验证码并且返回
    1.取到参数
    2.判断参数是否有值
    3.生成图片验证码
    4.保存图片验证码文字到redis
    5.返回验证码图片
    :return:
    '''
    # 1.取到参数
    #args:渠道url?后面的参数
    image_code_id = request.args.get("imageCodeId",None)
    # 2.判断参数是否有值
    if not image_code_id:
        return abort(403)

    # 3.生成图片验证码
    name,text,image = captcha.generate_captcha()

    # 4.保存图片验证码文字到redis
    try:
        redis_store.set("ImageCodeId"+image_code_id,text,constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)
    # 5.返回验证码图片
    response = make_response(image)
    response.headers["Content-Type"] = "image/jpg"
    return response
