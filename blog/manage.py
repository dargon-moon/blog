"""__author__ = 李厅康"""


import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from back.models import db
from back.views import blue
from web.views import web_blue

app = Flask(__name__)

# 第二步：管理蓝图
app.register_blueprint(blueprint=blue, url_prefix='/back')
app.register_blueprint(blueprint=web_blue, url_prefix='/web')


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:199417qaz@47.102.129.57:3306/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# 加密
app.secret_key = 'sd134215sadwe'


# 配置session信息
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='47.102.129.57', port=6379,password='199417qaz')
Session(app)

manage = Manager(app)
if __name__ == '__main__':
    manage.run()
