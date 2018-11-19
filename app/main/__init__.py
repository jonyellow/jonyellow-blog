#main目录：包含主要业务逻辑的路由和视图
#__init__.py是对main进行初始化
from flask import Blueprint

#用@main.route()  取代 @app.route()
main = Blueprint('main',__name__)

from . import views
