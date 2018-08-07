# coding=utf-8
import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# 配置应用连接的数据库
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@127.0.0.1:3306/art"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/art?charset=utf8"
# 追踪信号的修改并反馈
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)  # 定义db对象，实例化app连接关系型数据库数据库
"""定义表模型"""
"""
会员模型
id 
name 
pwd 
addtime
"""


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(20), nullable=False)  # 昵称 ,不允许为空
    pwd = db.Column(db.String(100), nullable=False)  # 密码
    addtime = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 注册时间

    def __repr__(self):  # 访问返回数据
        return "<User {}>".format(self.name)


"""
文章模型
id
title
cate 分类
author
logo 封面
content
addtime 
"""


class Art(db.Model):
    __tablename__ = "art"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(100), nullable=False)  # 不允许为空
    cate = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    logo = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    addtime = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 注册时间

    def __repr__(self):  # 访问返回数据
        return "<Art {}>".format(self.title)


def testrole():
    # 测试能够插入数据
    user = User(
        name=u'超级管理员',
        pwd="123"
    )
    db.session.add(user)
    db.session.commit()


def testadmin():
    # 测试能够插入数据
    from werkzeug.security import generate_password_hash
    admin = Admin(
        name="cccmovie",
        pwd=generate_password_hash("ccc"),
        is_supper=0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()


if __name__ == '__main__':
    testrole()
    # 在mysql中创建数据库
    #db.create_all()
