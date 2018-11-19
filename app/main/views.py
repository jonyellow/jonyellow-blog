import os
from time import time, strftime, localtime

from flask import render_template, request, redirect, session, url_for

#导入蓝图程序--main   用于构建路由
from . import main
#导入实体类，db 用于操作数据库
from ..import db
from ..models import *


#定义主页的访问路由,处理主业务逻辑：

BASEDIR = '\\'.join(os.path.abspath(__file__).split('\\')[:-2])

#访问主页--index.html
@main.route('/')
def do_index():
    #获得topic
    topics = Topic.query.all()
    if 'username' in session:
        user = User.query.filter_by(loginname = session['username']).first()
    return render_template('index.html', params = locals())

#登录页面
@main.route('/login',methods = ['GET', 'POST'])
def do_login():
    if request.method == 'GET':
        #返回登录界面
        return render_template('login.html')
    else:
        #登录信息提交过来，进行验证
        username = request.form.get('username')
        pwd = request.form.get('password')
        user = User.query.filter_by(loginname = username).first()
        if user:
            if pwd == user.upwd:
                # session['uid'] = user.id
                session['username'] = user.loginname
                resp = redirect('/')
                return resp
            else:
                return render_template('login.html', params='pwderror')
        else:
            return render_template('login.html', params = 'nameerror')

#退出当前登录
@main.route('/logout')
def do_logout():
    del session['username']
    Referer = request.headers.get('Referer')
    return redirect(Referer)

#注册页面
@main.route('/register', methods = ['GET', 'POST'])
def do_register():
    if request.method == 'GET':
        loginname = request.args.get('username')
        if loginname:
            ifuser = User.query.filter_by(loginname=loginname).first()
            if ifuser:
                return 'error'
            else:
                return 'right'
        return render_template('register.html')
    else:
        loginname = request.form.get('username')
        email = request.form.get('email')
        url = request.form.get('url')
        pwd = request.form.get('password')
        user = User()
        user.loginname = loginname
        user.uname = loginname
        user.email = email
        user.url = url
        user.upwd = pwd
        db.session.add(user)
        referer = request.form.get('source_url')
        session['username'] = loginname
        if referer:
            return redirect(referer)
        return redirect('/')


#博客信息
@main.route('/info', methods = ['GET', 'POST'])
def do_info():
    if request.method == 'GET':
        # 获得topic
        if 'username' in session:
            user = User.query.filter_by(loginname=session['username']).first()
        topic_id = request.args.get('topic_id')
        topic = Topic.query.filter_by(id=topic_id).first()
     #每阅读一次，阅读量加一
        topic.read_num += 1
        db.session.add(topic)
        return render_template('info.html', params = locals())
    else:
        data = request.form
        content = data.get('content')
        topic_id = data.get('article1')
        user_id = data.get('article2')
        #创建reply实例
        rep = Reply()
        if user_id:
            rep.user_id = int(user_id)
        else:
            return redirect('/login')
        rep.content = content
        rep.reply_time = strftime('%Y-%m-%d %X', localtime())
        rep.topic_id = int(topic_id)
        db.session.add(rep)
        url = '/info?topic_id=' + topic_id
        return redirect(url)

#发表博客
@main.route('/release', methods = ['GET', 'POST'])
def do_release():
    if request.method == 'GET':
        if 'username' in session:
            user = User.query.filter_by(loginname=session['username']).first()
            return render_template('release.html', params = locals())
        else:
            return redirect('/login')
    else:
        #获取发表的博客信息
        newtopic = request.form
        title = newtopic.get('title')
        pub_date = strftime('%Y-%m-%d %X', localtime())
        content = newtopic.get('editor')
        blogtype = newtopic.get('list')
        user_id = newtopic.get('article')
        #获取上传的文件 限一个文件，并以上传时间重命名
        f = request.files.get('imgfile')
        #创建Topic类的实例
        topic = Topic()
        if f:
            newfilename = strftime('%Y-%m-%d%H%M%S', localtime()) + os.path.splitext(f.filename)[1]
            # 将f保存到static文件夹下
            fpath = BASEDIR + '\static\img\\' + newfilename
            f.save(fpath)
            topic.images = 'img\\' + newfilename  # 将上传的文件名字保存到对应的topic的images属性下。
        topic.title = title
        topic.pub_date = pub_date
        topic.content = content
        topic.blogtype_id = blogtype
        topic.user_id = user_id
        db.session.add(topic)
        Referer = request.headers.get('Referer')
        return redirect(Referer)


#photo
@main.route('/photo')
def do_photo():
    if 'username' in session:
        user = User.query.filter_by(loginname=session['username']).first()
    return render_template('photo.html', params = locals())

#time
@main.route('/time')
def do_time():
    if 'username' in session:
        user = User.query.filter_by(loginname=session['username']).first()
        u_id = user.id
        topics = Topic.query.order_by('Topic.id desc').filter_by(user_id = u_id)
        return render_template('time.html', params = locals())
    else:
        return redirect('/')