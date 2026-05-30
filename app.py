from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
import sys

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
    # 👇 只在这里加两个字段，不影响你原来的数据
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


# 注册蓝图
from user_routes import user_bp
from ai_routes import ai_bp
from views.ai_views import views_bp

app.register_blueprint(user_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(views_bp)


# 初始化建表
# def init_db():
#     with app.app_context():
#         db.create_all()
#         print("✅ 数据库表创建成功")
# 初始化建表函数
def init_db():
    with app.app_context():
        db.create_all()
        print("✅ 数据库全部数据表创建成功")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

