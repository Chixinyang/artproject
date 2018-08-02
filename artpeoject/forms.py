# coding=utf-8
from flask_wtf import FlaskForm
from flask_wtf.file import file_required
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from models import User
from flask import session
from werkzeug.security import check_password_hash

"""
登录表单：
 name
 pwd
 登录按钮
"""


class LoginForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码"
        }
    )
    '''
    code = StringField(
        label="验证码",
        validators=[
            DataRequired("不能为空"),
        ],
        description="验证码",
        render_kw={
            "class": "form-control",
            "placeholder": "验证码"
        }
    )
    '''
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary",
            "href": "/art/list/1"
        }
    )

    ''' 去掉登录部分的验证码验证
    def validate_code(self, field):
        code = field.data
        if session.__getitem__("verifycode") != code:
            print(session.__getitem__("verifycode"), code)
            raise ValidationError("验证码错误")
    '''

    def validate_pwd(self, field):
        pwd = field.data
        user = User.query.filter_by(name=self.name.data).first()
        if not user or not check_password_hash(user.pwd, pwd):
            raise ValidationError("用户名不存在或密码错误")


"""
注册表单
name
pwd
repwd
验证码
注册按钮
"""


class RegisterForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[
            DataRequired("不能为空"),
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("不能为空"),
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码"
        }
    )
    repwd = PasswordField(
        label="再次输入密码",
        validators=[
            DataRequired("不能为空"),
            EqualTo('pwd', message="密码不一致")
        ],
        description="再次输入密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请再次输入密码"
        }
    )
    code = StringField(
        label="验证码",
        validators=[
            DataRequired("不能为空"),
        ],
        description="验证码",
        render_kw={
            "class": "form-control",
            "placeholder": "验证码"
        }
    )
    submit = SubmitField(
        "注册",
        render_kw={
            "class": "btn btn-success",
            "href": "/login/"
        }
    )

    def validate_name(self, field):
        name = field.data
        user_cont = User.query.filter_by(name=name).count()
        if user_cont > 0:
            raise ValidationError("账号已存在！")

    def validate_code(self, field):
        code = field.data
        if not session.__getitem__("verifycode"):
            raise ValidationError("没有验证码")
        elif session.__getitem__("verifycode") != code:
            print(session.__getitem__("verifycode"), code)
            raise ValidationError("验证码错误")


"""
发布文章表单
title
cate
logo
content
发布按钮 
"""


class ArtAddForm(FlaskForm):
    title = StringField(
        label="标题",
        validators=[
            DataRequired("标题不能为空"),
        ],
        description="标题",
        render_kw={
            "class": "form-control",
            "placeholder": "标题"
        }
    )
    cate = SelectField(
        label="分类",
        validators=[
            DataRequired("分类不能为空"),
        ],
        description="分类",
        choices=[(1, "科技"), (2, "搞笑"), (3, "军事")],
        default=2,
        coerce=int,  # 强制要求类型分类选项类型为int
        render_kw={
            "class": "form-control",
            "placeholder": "分类"
        }
    )
    logo = FileField(
        label="封面",
        validators=[
            #DataRequired("封面不能为空"),
           file_required("封面不能为空"),
        ],
        description="封面",
        render_kw={
            "class": "form-control-file"
        }
    )
    content = TextAreaField(
        label="内容",
        validators=[
            DataRequired("内容不能为空"),
        ],
        description="内容",
        render_kw={
            "style": "height : 200px",
            "id": "content"
        }

    )
    submit = SubmitField(
        "发布文章",
        render_kw={
            "class": "btn btn-success",
            "style": "margin-top : 10px",
            "href": "/art/list/1"
        }
    )