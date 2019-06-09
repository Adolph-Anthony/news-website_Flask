from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


class Config(object):
    '''项目的配置'''
    DEBUG = True
    SQLALCHEMY_DATABASE_URI= "mysql://root:mysql@127.0.0.1:3306/website"
    SQLALCHEMY_TRACK_MODIFICATIONS = Flask

app = Flask(__name__)
app.config.from_object(Config)

#初始化数据库
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
