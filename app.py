from flask import Flask, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
import sys
from datetime import datetime
from resource_routes import resource_bp
from path_routes import path_bp

sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
CORS(app, resources=r"/*", supports_credentials=True)


# 数据模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    major = db.Column(db.String(50), nullable=True)
    learning_style = db.Column(db.String(50))
    knowledge_level = db.Column(db.String(50))


class ChatRecord(db.Model):
    __tablename__ = 'chat_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # ✅ 新增这一行


# ✅ 新建 UserProfile 表（存储6维画像）
class UserProfile(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    knowledge_base = db.Column(db.String(50))  # 知识基础
    cognitive_style = db.Column(db.String(50))  # 认知风格
    weak_points = db.Column(db.Text)  # 易错短板（存JSON数组）
    learning_preference = db.Column(db.String(50))  # 学习偏好
    goal_level = db.Column(db.String(50))  # 目标层级
    active_time = db.Column(db.String(50))  # 活跃时段
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LearningResource(db.Model):
    __tablename__ = 'learning_resource'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resource_type = db.Column(db.String(50))
    content = db.Column(db.Text, nullable=False)


class LearningPath(db.Model):
    __tablename__ = 'learning_path'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    path_content = db.Column(db.Text, nullable=False)


# ✅ 保留这个：在启动时自动创建/检查表
with app.app_context():
    db.create_all()

# 注册蓝图
from user_routes import user_bp
from ai_routes import ai_bp
from views.ai_views import views_bp
from profile_routes import profile_bp

app.register_blueprint(user_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(views_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(resource_bp)
app.register_blueprint(path_bp)


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/index')
def index_page():
    return render_template('index.html')


# 初始化建表函数
def init_db():
    with app.app_context():
        db.create_all()
        print("✅ 数据库全部数据表创建成功")


# @app.route('/ping')
# def ping():
#     return "pong"


if __name__ == '__main__':
    # init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
