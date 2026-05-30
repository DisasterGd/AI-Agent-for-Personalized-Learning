from flask import Blueprint, make_response, jsonify, request
import json
from sqlalchemy import text

# 蓝图创建
views_bp = Blueprint("views", __name__)

# 导入配置和数据库 + 模型
from config import Config


# 原from app import db, ChatRecord, LearningResource, LearningPath, User已在函数内部分别导入


# 健康检查
@views_bp.route("/")
def health_check():
    data = {
        "code": 200,
        "msg": "Software Cup backend is running, connected to Cherry Studio personalized learning agent",
        "vector_db_path": Config.VECTOR_DB_PATH
    }
    return make_response(
        json.dumps(data, ensure_ascii=False),
        200,
        {"Content-Type": "application/json; charset=utf-8"}
    )


# 数据库测试
@views_bp.route("/db/test")
def db_test():
    from app import db  # 导入1
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"code": 200, "msg": "Database connection success!"})
    except Exception as e:
        return jsonify({"code": 500, "msg": f"Database connection failed: {str(e)}"})


# 向量库路径
@views_bp.route("/vector/path")
def get_vector_path():
    return jsonify({
        "code": 200,
        "data": {
            "vector_db_path": Config.VECTOR_DB_PATH,
            "knowledge_base_path": Config.KNOWLEDGE_BASE_PATH
        }
    })


# 查询对话历史
@views_bp.route("/chat/history")
def chat_history():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"code": 400, "msg": "user_id is required"})

    from app import ChatRecord  # 导入2
    records = ChatRecord.query.filter_by(user_id=user_id).order_by(ChatRecord.id.desc()).all()
    res = []
    for r in records:
        res.append({
            "id": r.id,
            "user_msg": r.query,
            "ai_response": r.response,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else None
        })
    return jsonify({"code": 200, "data": res})


# 查询学习资源
@views_bp.route("/resource/list")
def resource_list():
    user_id = request.args.get("user_id")

    from app import LearningResource  # 导入3
    resources = LearningResource.query.filter_by(user_id=user_id).all()
    data = [{"id": r.id, "type": r.resource_type, "content": r.content} for r in resources]
    return jsonify({"code": 200, "data": data})


# 查询学习路径
@views_bp.route("/path/detail")
def path_detail():
    user_id = request.args.get("user_id")

    from app import LearningPath  # 导入4
    path = LearningPath.query.filter_by(user_id=user_id).first()
    if not path:
        return jsonify({"code": 404, "msg": "No path"})
    return jsonify({"code": 200, "data": {"id": path.id, "content": path.path_content}})

