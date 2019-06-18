from flask import abort, jsonify
from flask import current_app
from flask import g
from flask import render_template
from flask import request
from flask import session

from info import constants, db
from info.models import News, User, Comment, CommentLike
from info.modules.news import news_blu

from info.utils.common import user_login_data
from info.utils.response_code import RET

@news_blu.route("/comment_like",methods = ["POST"])
@user_login_data
def comment_like():
    '''
    评论点赞
    参数名	    类型	    是否必须	参数说明
    comment_id	int	    是	    评论id
    news_id	    int	    是	    新闻id
    action	    string	是	    点赞操作类型：add(点赞)，remove(取消点赞)
    :return:
    '''
    comment_id = request.json.get("comment_id")
    news_id = request.json.get("news_id")
    action = request.json.get("action")
    print(comment_id,news_id,action)
    user = g.user
    if not all([news_id,comment_id,action]):
        return jsonify(errno=RET.PARAMERR,errmsg = "参数错误")

    if action not in (["add","remove"]):
        return jsonify(errno=RET.PARAMERR,errmsg = "参数错误")

    try:
        comment_id = int(comment_id)
        news_id = int(news_id)
    except Exception as e:
        current_app.logger.error(e)
        print(3)

        return jsonify(errno=RET.PARAMERR,errmsg = "参数错误")
    comment = None
    try:
        comment = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)
    if not comment:
        return jsonify(errno = RET.NODATA,errmsg = "评论不存在")
    try:
        if action=="add" :
            comment_like_model  = CommentLike.query.filter(CommentLike.user_id==user.id,CommentLike.comment_id==comment.id).first()
            if not comment_like_model:
                comment_like_model=CommentLike()
                comment_like_model.user_id = user.id
                comment_like_model.comment_id = comment.id
                db.session.add(comment_like_model)
                comment.like_count +=1


        else:
            #取消点赞评论
            comment_like_model  = CommentLike.query.filter(CommentLike.user_id==user.id,CommentLike.comment_id==comment.id).first()
            if comment_like_model:
                db.session.delete(comment_like_model)
                comment.like_count -=1
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg = "请先登录")

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="数据库操作失败")

    return jsonify(errno = RET.OK,errmsg="成功")
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

    return jsonify(errno = RET.OK,errmsg ="ok",data=comment.to_dict())

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

    comments = []
    #去查询评论数据
    try:
        comments= Comment.query.filter(Comment.news_id == news_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)
    comment_dict_list = []
    comments_ids = []
    if g.user:
        try:
            # 需求:当前用户在当前新闻里面都点赞了哪些评论
            # 1. 查询出 当前 新闻的所有评论 (comments) 所有的评论ID   [1,2,3,4,5]
            comments_ids = [comment.id for comment in comments]
            print("comments_ids")
            # 2. 再查询当前评论中哪些评论被当前用户所点赞  (CommentLike) 查询comment_id 在第一步的评论id列表内的所有数据,CommentLike.user_id == g.user.id
            Comment_likes = CommentLike.query.filter(CommentLike.comment_id.in_(comments_ids),
                                                     CommentLike.user_id == g.user.id).all()
            print("Comment_likes")
            # 3. 取到所有被点赞的评论id,第二步查询出来是一个[CommentLike] --> [3,5]
            comments_ids = [comment_like.comment_id for comment_like in Comment_likes]

        except Exception as e:
            current_app.logger.error(e)

    for comment in comments:
        comment_dict = comment.to_dict()
        comment_dict["is_like"] = False
        if comment.id in comments_ids:
            comment_dict["is_like"] = True
        comment_dict_list.append(comment_dict)

    data = {
        "user": user.to_dict() if user else None,
        "news":news.to_dict(),
        "news_dict_li": news_dict_li,
        "is_collected":is_collected,
        "comments":comment_dict_list
    }



    return render_template("news/detail.html",data = data)