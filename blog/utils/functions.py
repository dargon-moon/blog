"""__author__ = 李厅康"""

# 装饰器的条件
# 1.外出函数嵌套内层函数
# 2.外层函数返回内层函数
# 3.内层函数调用外层函数的参数
from functools import wraps

from flask import session, render_template, redirect, url_for

from back.models import ArticleType, Article, User


def is_login(func):
    @wraps(func)
    def check():
        try:
            session['user_id'] and User.is_delete == 0
            return func()
        except:
            return redirect(url_for('first.session_login'))
    return check

