from flask import render_template

from info.modules.news import news_blu

#127.0.0.1:5000/news/1
@news_blu.route("/<int:news_id>")
def news_detail(news_id):
    '''
    新闻详情
    :param news_id:
    :return:
    '''
    data = {

    }
    return render_template("news/detail.html")