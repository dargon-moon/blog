"""__author__ = 李厅康"""
from flask import Blueprint, make_response, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash,check_password_hash
import tkinter
import tkinter.messagebox

# 蓝图，管理路由地址
# 第一步：生成蓝图对象
from back.models import User, Article, ArticleType, db
from utils.functions import is_login

blue = Blueprint('first', __name__)

# 后台主页
@blue.route('/system/')
@is_login
def system():
    return render_template('back/index.html')


# 注册
@blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        # 模拟注册功能
        # 获取页面中传递的参数
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if username and password and password2:
            # 先判断该账号是否被注册过
            user = User.query.filter(User.username == username).first()
            print(user.username)
            if user and user.is_delete == 0:
                # 判断该账号已经被注册过
                error = '该账号已注册，请更换账号'
                return render_template('back/register.html', error=error)
            elif not user:
                if password2 == password:
                    # 保存数据
                    user = User()
                    user.username = username
                    user.password = generate_password_hash(password)
                    user.save()
                    return redirect(url_for('first.session_login'))
                else:
                    # 密码错误
                    error = '两次密码不一致'
                    return render_template('back/register.html', error=error)
            elif user.is_delete == 1:
                if password == password2:

                    user.password = generate_password_hash(password)
                    user.is_delete = 0
                    user.save()
                    return redirect(url_for('first.session_login'))
                else:
                    # 密码错误
                    error = '两次密码不一致'
                    return render_template('back/register.html', error=error)
        else:
            error = '请填写完整的信息'
            return render_template('back/register.html', error=error)


# 登录
@blue.route('/session_login/', methods=['GET', 'POST'])
def session_login():
    if request.method == 'GET':
        return render_template('/back/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter(User.username == username).first()
            if not user or user.is_delete == 1:
                error = '该账号不存在，请注册'
                return render_template('/back/login.html', error=error)
            if user.is_delete == 0 and not check_password_hash(user.password, password):
                error = '密码错误，请修改密码'
                return render_template('/back/login.html', error=error)
            # 账号和密码匹配正确，跳转到首页
            session['user_id'] = user.id
            return redirect(url_for('first.system'))
        else:
            error = '请填写完整的登录信息'
            return render_template('/back/login.html', error=error)


#退出
@blue.route('/logout/', methods=['GET'])
@is_login
def logout():
    del session['user_id']
    return redirect(url_for('first.login'))


# 获取分类
@blue.route('/a_type/', methods=['GET', 'POST'])
@is_login
def a_type():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/category_list.html', types=types)


# 添加分类
@blue.route('/add_type/', methods=['GET', 'POST'])
@is_login
def add_type():
    if request.method == 'GET':
        return render_template('back/category_add.html')
    if request.method == 'POST':
        atype = request.form.get('atype')
        if atype:
            # 保存分类信息
            art_type = ArticleType()
            art_type.t_name = atype
            db.session.add(art_type)
            db.session.commit()
            return redirect(url_for('first.a_type'))
        else:
            error = '请填写分类信息'
            return render_template('back/category_add.html', error=error)


# 删除分类
@blue.route('/del_type/<int:id>/', methods=['GET'])
def del_type(id):
    # 删除分类
    atype = ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('first.a_type'))


# 文章列表
@blue.route('/article_list/', methods=['GET'])
@is_login
def article_list():
    articles = Article.query.all()
    return render_template('back/article_list.html', articles=articles)


# 添加文章
@blue.route('/article_add/', methods=['GET', 'POST'])
@is_login
def article_add():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/article_detail.html', types=types)
    if request.method == 'POST':
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('my-editormd-html-code')
        if title and desc and category and content:
            # 保存
            art = Article()
            art.title = title
            art.desc = desc
            art.contect = content
            art.type = category
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('first.article_list'))
        else:
            error = '请填写完整的文章信息'
            return render_template('back/article_detail.html', error=error)


# 删除文章
@blue.route('/del_article/<int:id>/', methods=['GET'])
# 删除文章
def del_article(id):
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('first.article_list'))


# 修改文章
@blue.route('/compile_article/<int:id>/',methods=['GET', 'POST'])
# 编辑文章
def compile_article(id):
    if request.method == 'GET':
        article = Article.query.get(id)
        types = ArticleType.query.all()
        return render_template('back/article_compile.html', article=article, types=types)
    if request.method == 'POST':
        article = Article.query.get(id)
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('my-editormd-html-code')
        if title and desc and category and content:
            # 保存

            article.title = title
            article.desc = desc
            article.contect = content
            article.type = category
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('first.article_list'))
        else:
            error = '请填写完整的文章信息'
            return render_template('back/article_detail.html', error=error)


# 用户信息
@blue.route('/user_message/', methods=['GET'])
@is_login
def user_message():
    users = User.query.all()
    return render_template('back/user_list.html', users=users)


# 注销用户
@blue.route('/user_del/<int:id>/',methods=['GET'])
def user_del(id):
    user = User.query.get(id)
    del session['user_id']
    user.is_delete = 1
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('first.session_login'))


# 修改密码
@blue.route('/user_alter/<int:id>', methods=['GET','POST'])
def user_alter(id):
    if request.method == 'GET':
        user = User.query.get(id)
        return render_template('back/user_alter.html', user=user)
    if request.method == 'POST':
        user = User.query.get(id)
        oldpassword = request.form.get('oldpassword')
        newpassword = request.form.get('newpassword')
        newpassword2 = request.form.get('newpassword2')
        if not check_password_hash(user.password, oldpassword):
            error = '原密码错误请输入正确的密码'
            return render_template('back/user_alter.html',error=error)
        elif newpassword and newpassword2:
            if newpassword != newpassword2:
                error = '两次新密码不一致，请重新输入'
                return render_template('back/user_alter.html', error=error)
            else:
                del session['user_id']
                user.password = generate_password_hash(newpassword)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('first.session_login'))
        else:
            error = '新密码不能为空！'
            return render_template('back/user_alter.html', error=error)