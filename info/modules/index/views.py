from flask import current_app, jsonify
from flask import render_template
from flask import request
from flask import session

from info import constants
from info import redis_store
from info.models import User, News
from info.utils.response_code import RET
from . import index_blu

@index_blu.route("/news_list")
def new_list():
    '''
    获取首页新闻数据
    :return:
    '''
    #1.获取参数
    #新闻的分类id
    cid = request.args.get("cid","1")
    page = request.args.get("page","1")
    per_page = request.args.get("per_page","10")
    print(cid)
    print(page)
    print(per_page)
    #2.校验参数
    try:
        page = int(page)
        cid = int(cid)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno= RET.PARAMERR,errmsg = "参数错误")
    filters = []
    if cid !=1:#查询的不是最新的数据
        #需要添加条件
        filters.append(News.category_id==cid)
    # 3.查询数据
    try:
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page,per_page,False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    #取到当前页数据
    news_model_list= paginate.items    #模型对象列表
    #总页数
    toral_page = paginate.pages
    #当前页
    current_page = paginate.page

    #将模型对象列表转成字典列表
    news_dict_li = []
    for news in news_model_list:
        news_dict_li.append(news.to_basic_dict())
    data = {
        "toral_page":toral_page,
        'current_page':current_page,
        'news_dict_li':news_dict_li

    }
    return jsonify(errno = RET.OK,errmsg= "OK",data = data)

@index_blu.route('/')
def index():
    '''
    显示首页
    1.如果用户已经登录,将当前登录用户数据传到模板中,以供显示
    :return:
    '''
    #显示用户是否登录的逻辑
    #取到用户id
    user_id = session.get("user_id",None)
    user = None
    if user_id:
        #去数据库里查询指定id的模型
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    #右侧的新闻排行逻辑
    news_list = []
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)
    news_dict_li = []
    #遍历对象列表,将对象的字典添加到字典列表中
    for news in news_list:
        news_dict_li.append(news.to_basic_dict())
    data = {
        "user":user.to_dict() if user else None,
        "news_dict_li":news_dict_li
    }
    return render_template("news/index.html",data = data)

#加载favicon.ico图标
#send_static_file是flask把静态文件从静态文件夹发送到浏览器
@index_blu.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")