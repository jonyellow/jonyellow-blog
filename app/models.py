#用于创建模型类

#导入db 以及models
from . import db

#数据库结构已经在数据库中创建好了，所以最后不需要db.create_all()
#如果数据库中没有表结构，则需要使用db.create_all() 映射到数据库中。

#个人博客
class BlogType(db.Model):
    __tablename__ = 'blogtype'
    id = db.Column(db.Integer, primary_key = True)
    type_name = db.Column(db.String(20), nullable = False)
    topics = db.relationship('Topic', backref = 'blogtypes', lazy = 'dynamic')

#文章分类
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    cate_name = db.Column(db.String(50), nullable = False)
    topics = db.relationship('Topic', backref = 'categorys', lazy = 'dynamic')

#博客文章
class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    pub_date = db.Column(db.DateTime, nullable = False)
    read_num = db.Column(db.Integer, default = 0)
    content = db.Column(db.Text, nullable = False)
    images = db.Column(db.Text)
    blogtype_id = db.Column(db.Integer, db.ForeignKey('blogtype.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    replys = db.relationship('Reply', backref = 'topics', lazy = 'dynamic')


#用户信息表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    loginname = db.Column(db.String(50), nullable = False)
    uname = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    url = db.Column(db.String(200))
    upwd = db.Column(db.String(30), nullable = False)
    is_author = db.Column(db.SmallInteger, default = 0)
    topics = db.relationship('Topic', backref='users', lazy='dynamic')
    replys = db.relationship('Reply', backref = 'users', lazy = 'dynamic')
    voke_topics = db.relationship(
        'Topic',
        secondary='voke',
        backref=db.backref('voke_users', lazy='dynamic'),
        lazy='dynamic'
    )

#博客回复
class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    reply_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

#点赞 不用创建实体类，但是数据库中是有实体表的。
Voke = db.Table(
  'voke',
  db.Column('id',db.Integer,primary_key=True),
  db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
  db.Column('topic_id',db.Integer,db.ForeignKey('topic.id'))
)


