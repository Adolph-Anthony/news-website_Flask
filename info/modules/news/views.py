from flask import abort, jsonify
from flask import current_app
from flask import g
from flask import render_template
from flask import request
from flask import session

from info import constants, db
from info.models import News, User, Comment
from info.modules.news import news_blu

#127.0.0.1:5000/news/1
from info.utils.common import user_login_data
from info.utils.response_code import RET

@news_blu.route("/news_comment",methods = ["POST"])
@user_login_data
def comment():
    '''
    评论新闻或者回复某条新闻
    参数名	        类型	    是否必须	参数说明
    news_id	        int	    是	    新闻id
    comment_conent	string	是	    评论内容
    parent_id	    int	    否	    回复的评论的id
    :return:
    '''
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR,errmsg = "用户未登录")
    #1.取到请求参数
    news_id = request.json.get("news_id")
    comment_conent= request.json.get("comment")
    parent_id = request.json.get("parent_id")

    #2.判断参数
    if not all([news_id,comment_conent]):
        return jsonify(errno=RET.PARAMERR,errmsg = "参数错误")
    try:
        news_id = int(news_id)
        if parent_id:
            parent_id = int(parent_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg = "参数错误")

    # 3.查询新闻,判断新闻是否存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg = "数据查询错误")

    if not news :
        return jsonify(errno=RET.NODATA,errmsg = "未查询到数据")

    #3.初始化评论模型,并且赋值
    comment = Comment()
    comment.user_id = user.id
    comment.news_id = news_id
    comment.content = comment_conent
    if parent_id:
        comment.parent_id = parent_id

    # 添加到数据库
    #为什么要自己去commit()
    #因为return的时候需要用的comment的 id
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()

    return jsonify(errno = RET.OK,errmsg ="ok",comment=comment.to_dict())

@news_blu.route("/newscollect",methods =["POST"])
@user_login_data
def collect_news():
    '''
    收藏新闻
    1.接收参数
    2.判断参数
    3.查询新闻,判断新闻是否存在
    :return:
    '''

    # 判断用户是否存在
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR,errmsg = "用户未登录")
    # 1.接收参数

    news_id = request.json.get("news_id")
    #收藏的状态
    action = request.json.get("action")
    print(news_id,action)
    # 2.判断参数
    if not all([news_id,action]):
        return jsonify(errno=RET.PARAMERR,errmsg = "参数错误")

    if action not in ["collect","cancel_collect"]:
        return jsonify(errno=RET.PARAMERR,errmsg = "参数错误")

    try:
        news_id = int(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg = "参数错误")
    # 3.查询新闻,判断新闻是否存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg = "数据查询错误")

    if not news :
        return jsonify(errno=RET.NODATA,errmsg = "未查询到数据")
    # 4.收藏与取消收藏
    if action=="cancel_collect":
        #取消收藏
        if news in user.collection_news:
            user.collection_news.remove(news)
    else:
        #收藏
        if news not in user.collection_news:
            #添加到用户新闻收藏列表
            user.collection_news.append(news)

    return jsonify(errno=RET.OK, errmsg="操作成功 ")


@news_blu.route("/<int:news_id>")
@user_login_data
def news_detail(news_id):
    '''
    新闻详情
    :param news_id:
    :return:
    '''
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

    #查询新闻数据
    news = None
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger(e)
    if not news:
        # TODO 报404错误,404错误统一显示页面后续在处理
        abort(404)

    #更新新闻的点击次数
    news.clicks += 1

    is_collected = False

    # 如果用户已登录
    if user:
    #collection_news后面可以不用加all(),SQLAlchemy什么时候用到什么时候调用
    #判断用户是否收藏当前新闻,如果收藏
        if news in user.collection_news:

            is_collected = True





    data = {
        "user": user.to_dict() if user else None,
        "news":news.to_dict(),
        "news_dict_li": news_dict_li,
        "is_collected":is_collected

    }



    return render_template("news/detail.html",data = data)