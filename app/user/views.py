#针对用户业务逻辑处理的视图函数，和路由的定义。
from . import user

#用来处理用户登录验证，与login.html对应。
@user.route('/user')
def users_index():
    return 'user index'