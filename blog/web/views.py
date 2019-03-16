"""__author__ = 李厅康"""


from flask import Blueprint, render_template, url_for, request

from back.models import Article, User, ArticleType

web_blue = Blueprint('web', __name__)


@web_blue.route('/index/',methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        articles = Article.query.limit(8).all()
        user = User.query.all()
        types = ArticleType.query.all()
        return render_template('web/home.html', articles=articles, user=user, types=types)


@web_blue.route('/article/<int:id>')
def article(id):
    types = ArticleType.query.all()
    articles = Article.query.get(id)
    return render_template('web/article.html', articles=articles,types=types)


@web_blue.route('/article_type/<int:id>')
def article_type(id):
    articles = Article.query.filter(id == Article.type).all()
    user = User.query.all()
    types = ArticleType.query.all()
    return render_template('web/article_type.html',articles=articles, user=user, types=types)

@web_blue.route('/about/')
def about():
    return render_template('web/about.html')