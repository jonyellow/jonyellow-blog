#对整个应用程序做初始化操作
#负责创建flask应用以及各种配置
#创建数据库实例
#创建蓝图 Blueprint 关联其他业务程序

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()
#创建数据库实例 通过一个函数创建qpp
def create_app():
    app = Flask(__name__)

    #有关配置
    #连接数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/blog'
    #设置数据库操作自动提交
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    #启动调试模式
    app.config['DEBUG'] = True
    #设置session的密匙
    app.config['SECRET_KEY'] = 'whenIwasalittleboy'
    #使用app初始化db
    db.init_app(app)


    #使用蓝图关联程序,使得主程序开启后可以直接访问他们的路由，运行视图处理函数
    #关联main
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    #关联 user
    from .user import user as users_blueprint
    app.register_blueprint(users_blueprint)

    return app