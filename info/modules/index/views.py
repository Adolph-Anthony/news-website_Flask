from info import redis_store
from . import index_blu
@index_blu.route('/')
def hello_world():
    #向redis中保存一个值
    redis_store.set("name","ka")
    return 'Hello World!'