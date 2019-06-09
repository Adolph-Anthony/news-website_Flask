from redis import StrictRedis
import logging
class Config(object):
    '''项目的配置'''

    SECRET_KEY = "Wub8dLQfSWgqpyEkUieJVzYX1bVY61/cE1npjbJhlzm57qTPpnDzn3Yvu2j2DMGU"

    #数据库添加配置
    SQLALCHEMY_DATABASE_URI= "mysql://root:mysql@127.0.0.1:3306/website"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Redis 的 配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    #Session保存配置
    SESSION_TYPE = "redis"
    #开启session签名
    SESSION_USE_SIGNER = True
    #制定Session 保存的 redis
    SESSION_REDIS = StrictRedis(host= REDIS_HOST,port=REDIS_PORT)
    #设置session需要过期
    SESSION_PERMANENT = False
    #设置过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2

    #设置日志等级
    LOG_LEVEL = logging.DEBUG

class DevelopmentConfig(Config):
    '''开发环境下的配置'''
    DEBUG = True
    LOG_LEVEL = logging.ERROR

class ProductionConfig(Config):
    '''生产环境下的配置'''
    DEBUG = False


class TestingConfig(Config):
    '''单元测试环境下的配置'''
    DEBUG = True
    TESTING = True




config = {
    "development":DevelopmentConfig,
    "production":ProductionConfig,
    "testing":TestingConfig
}



