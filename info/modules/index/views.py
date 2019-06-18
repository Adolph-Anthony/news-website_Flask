from flask import current_app, jsonify
from flask import g
from flask import render_template
from flask import request
from flask import session

from info import constants
from info import redis_store
from info.models import User, News, Category
from info.utils.common import user_login_data
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
        return jsonify(errno=RET.DATAERR, errmsg="数据查询错误")

    #取到当前页数据
    news_list= paginate.items    #模型对象列表
    #总页数
    total_page = paginate.pages
    #当前页
    current_page = paginate.page

    # 查询分类数据,通过末班的形式渲染
    news_dict_li = []
    #遍历对象列表,将对象的字典添加到字典列表中
    for news in news_list:
        news_dict_li.append(news.to_basic_dict())
        # print(news.to_basic_dict())
    data = {
        'total_page':total_page,
        'current_page':current_page,
        'news_dict_li':news_dict_li

    }
    return jsonify(errno = RET.OK,errmsg= "OK",data = data)

@index_blu.route('/')
@user_login_data
def index():
    '''
    显示首页
    1.如果用户已经登录,将当前登录用户数据传到模板中,以供显示
    :return:
    '''
    # #显示用户是否登录的逻辑
    # #取到用户id
    # user_id = session.get("user_id",None)
    # user = None
    # if user_id:
    #     #去数据库里查询指定id的模型
    #     try:
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)

    user = g.user

    #右侧的新闻排行逻辑
    news_list = []
    try:
        #查询新闻数据库里的按浏览量降序排行一页十个新闻
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)
    news_dict_li = []
    for news in news_list:
        news_dict_li.append(news.to_basic_dict())

    # 将模型对象列表转成字典列表
    categories = Category.query.all()
    category_li = []

    for category in categories:
        category_li.append(category.to_dict())


    data = {
        "user":user.to_dict() if user else None,
        "news_dict_li":news_dict_li,
        "category_li":category_li
    }
    return render_template("news/index.html",data = data)

#加载favicon.ico图标
#send_static_file是flask把静态文件从静态文件夹发送到浏览器
@index_blu.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("news/favicon.ico")