from flask import render_template

from info import redis_store
from . import index_blu
@index_blu.route('/')
def hello_world():
    #向redis中保存一个值
    return render_template("news/index.html")
