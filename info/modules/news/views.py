from flask import current_app
from flask import render_template
from flask import session

from info import constants
from info.models import News, User
from info.modules.news import news_blu

#127.0.0.1:5000/news/1
@news_blu.route("/<int:news_id>")
def news_detail(news_id):
    '''
    新闻详情
    :param news_id:
    :return:
    '''
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
        #查询新闻数据库里的按浏览量降序排行一页十个新闻
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)
    news_dict_li = []
    for news in news_list:
        news_dict_li.append(news.to_basic_dict())
    data = {
        "user": user.to_dict() if user else None,

        "news_dict_li": news_dict_li,

    }
    return render_template("news/detail.html",data = data)