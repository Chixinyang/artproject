# coding:utf-8

from datetime import datetime
from functools import wraps
from flask import Flask, render_template, redirect, flash, Response, session, url_for, request
from forms import LoginForm, RegisterForm, ArtAddForm, ArtEditForm
from models import User, db, Art
from verification_code import Verify_Code
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
# 查看 分页类的成员
# from flask_sqlalchemy import Pagination
import os

app = Flask(__name__)
# 添加CSRF secret
app.config["SECRET_KEY"] = "123456"
app.config["UP_PATH"] = os.path.join(os.path.dirname(__file__), "static{0}userlogo".format(os.sep))


# 定义访问控制装饰器，实现访问页面的控制
def Access_Control(func):
    @wraps(func)
    def user_access_control(*args, **kwargs):
        if "username" not in session.keys():
            print("username not in session ")
            flash("请先登陆", "login first")
            # return redirect("/login/")
            return redirect(url_for("login", next=request.url))
        else:
            return func(*args, **kwargs)

    return user_access_control


# 定义路由
@app.route("/", methods=["GET", "POST"])
def index():
    return redirect("/login/")


# 登录
@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        session.__setitem__("username", data["name"])
        print("登录成功" + session.__getitem__("username"))
        flash("登录成功！", "login ok")
        return redirect("/art/list/1")
    return render_template("login.html", title="登录", form=form)  # 渲染模板


# 注册
@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data  # data是一个字典类型
        # 保存数据
        user = User(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            addtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(user)
        db.session.commit()
        # 定义一个会话闪现
        flash("注册成功,请登录", "register ok")
        return redirect("/login/")
    else:
        flash("哎呦，貌似注册还没成功", "register err")
    return render_template("register.html", title="注册", form=form)  # 渲染模板


# 退出(302跳转到登录界面)
@app.route("/logout/", methods=["GET"])
@Access_Control
def logout():
    if "username" in session.keys():
        print(session["username"])
        session.__delitem__("username")
    return redirect("/login/")  # 渲染模板


# 文章列表
@app.route("/art/list/<int:page_num>", methods=["GET"])
@Access_Control
def art_list(page_num):
    if not page_num:
        page_num = 1
    showlog(page_num)

    user = User.query.filter_by(name=session["username"]).first()
    showlog(user.id)

    page_data = Art.query.filter_by(
        user_id=user.id
    ).order_by(
        Art.addtime.desc()
    ).paginate(page=page_num, per_page=1)

    if "username" in session.keys():
        username = session["username"]
    else:
        username = "游客"
    return render_template("art_list.html", title="文章列表", username=username, page_data=page_data)  # 渲染模板


# 编辑文章
@app.route("/art/edit/<int:id>", methods=["GET", "POST"])
@Access_Control
def art_edit(id):
    values = CombinedMultiDict([request.files, request.form])
    form = ArtEditForm(values)
    art = Art.query.get_or_404(int(id))
    old_logo = art.logo
    form.art_id.data = int(id)
    if request.method == "GET":
        # 获取cate
        choices = {
            '1': "科技",
            '2': "搞笑",
            '3': "军事"
        }
        for key, value in choices.items():
            if value == art.cate:
                form.cate.data = int(key)
        form.content.data = art.content
        showlog(key + " :" + art.cate)
    else:
        if form.validate_on_submit():
            showlog("验证通过")
            data = form.data
            art.title = data["title"]
            art_cate = [(1, "科技"), (2, "搞笑"), (3, "军事")]
            art.cate = art_cate[data["cate"] - 1][1]
            art.content = data["content"]
            if type(form.logo.data) == type("str"):
                art.logo = old_logo
                pass
            else:
                # 获取logo文件并改名
                logo_source_filepath = secure_filename(form.logo.data.filename)
                logo = change_logo_name(str(logo_source_filepath))
                # logo保存到本地
                if not os.path.exists(app.config["UP_PATH"]):
                    os.mkdir(app.config["UP_PATH"])
                logo_path = os.path.join(app.config["UP_PATH"], logo)
                form.logo.data.save(logo_path)
                # 删除旧的logo
                old_logo_path = os.path.join(app.config["UP_PATH"], old_logo)
                showlog("new :" + logo_path + " old:" + old_logo_path)
                os.remove(old_logo_path)
                art.logo = logo
            db.session.add(art)
            db.session.commit()
            flash("文章编辑成功", "art edit ok")
        else:
            showlog("编辑失败")
    return render_template("art_edit.html", title="编辑文章", form=form, art=art)  # 渲染模板


# 发布文章
@app.route("/art/add/", methods=["GET", "POST"])
@Access_Control
def art_add():
    values = CombinedMultiDict([request.files, request.form])
    form = ArtAddForm(values)

    if form.validate_on_submit():
        data = form.data
        # 获取logo文件并改名
        logo_source_filepath = secure_filename(form.logo.data.filename)
        logo = change_logo_name(str(logo_source_filepath))
        # logo保存到本地
        if not os.path.exists(app.config["UP_PATH"]):
            os.mkdir(app.config["UP_PATH"])
        logo_path = os.path.join(app.config["UP_PATH"], logo)
        showlog(type(logo_source_filepath))
        showlog(logo_source_filepath)
        showlog(logo)
        showlog(logo_path)
        # showlog(data["logo"]+" "+form.logo.data.filename)

        form.logo.data.save(logo_path)
        # 保存Art入库
        user = User.query.filter_by(name=session["username"]).first()

        art_cate = [(1, "科技"), (2, "搞笑"), (3, "军事")]
        cate = art_cate[data["cate"] - 1][1]
        showlog(cate)
        art = Art(
            title=data["title"],
            cate=cate,
            user_id=user.id,
            logo=logo,
            content=data["content"],
            addtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(art)
        db.session.commit()
        flash("文章发布成功", "art add ok")
        return redirect("/art/list/1")
    else:
        print("验证失败")

    if "username" in session.keys():
        username = session["username"]
    else:
        username = "游客"
    return render_template("art_add.html", title="文章发布", form=form, username=username)  # 渲染模板


# 删除文章
@app.route("/art/del/<int:id>", methods=["GET"])
@Access_Control
def art_del(id):
    art = Art.query.get_or_404(int(id))  # 注意这里的一定要转成int类型
    art_logo_path = os.path.join(app.config["UP_PATH"], art.logo)
    os.remove(art_logo_path)
    showlog("删除logo :{}".format(art_logo_path))
    db.session.delete(art)
    db.session.commit()
    flash("成功删除文章《{}》".format(art.title), "art del ok")
    return redirect("/art/list/1")


# return render_template("art_delete.html")  # 渲染模板


# 验证码
@app.route("/verifycode/", methods=["GET"])
def verifycode():
    # 创建验证码
    verifycode = Verify_Code()
    verifycode.create_verification_code()
    # 读取图片的二进制编码
    with open(verifycode.image_path, mode='rb') as f:
        image = f.read()
    session.__setitem__("verifycode", verifycode.chars)
    print(session["verifycode"])
    # 以图片的格式返回
    return Response(image, mimetype='jpeg')


# 更改用户上传logo的文件名便于保存
def change_logo_name(filepath):
    # source_name = os.path.splitext(filepath)  # 提取路径文件名
    newname = "{0}_{1}_{2}".format(session["username"], datetime.now().strftime("%Y%m%d%H%M%S"), filepath)
    return newname


# 调试使用
import inspect


def showlog(str):
    print("{0} : {1}".format(inspect.stack()[1][3], str))


if __name__ == "__main__":
    # debug=True 调试模式自动运行修改后的文件
    app.run(debug=True, host="127.0.0.1", port=8080)
