from flask import Blueprint

#创建蓝图对象
passport_blu = Blueprint("passport",__name__)
from . import views