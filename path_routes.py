from flask import Blueprint, request, jsonify
import json,time

path_bp = Blueprint("path", __name__, url_prefix="/api/path")


@path_bp.route("/generate", methods=["POST"])
def generate_path():
    from app import db, LearningPath
    """
    生成个性化学习路径（Mock 版本）
    根据用户提供的 topic 生成步骤数组
    """
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "msg": "请求体必须为 JSON"}), 400

    user_id = data.get("user_id")
    topic = data.get("topic", "编程")
    goal = data.get("goal", f"掌握 {topic} 基础知识")

    # 模拟生成耗时
    time.sleep(1.0)

    # 根据 topic 动态生成步骤
    steps = [
        {"step": 1, "title": f"{topic} 基础入门", "description": f"了解 {topic} 的核心概念、历史背景和应用场景", "estimated_time": "2天"},
        {"step": 2, "title": f"{topic} 核心语法与实践", "description": f"掌握 {topic} 的关键语法和常用 API，完成第一个小示例", "estimated_time": "3天"},
        {"step": 3, "title": f"{topic} 进阶技巧", "description": f"深入学习 {topic} 的高级特性，结合实际场景优化代码", "estimated_time": "4天"},
        {"step": 4, "title": f"{topic} 综合项目实战", "description": f"独立完成一个完整的 {topic} 项目，巩固所学知识", "estimated_time": "5天"}
    ]

    # 构建路径 JSON
    path_content = {
        "topic": topic,
        "goal": goal,
        "steps": steps,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # 保存到数据库
    try:
        # 检查该用户是否已有路径，有则更新，无则新建
        existing = LearningPath.query.filter_by(user_id=user_id).first()
        if existing:
            existing.path_content = json.dumps(path_content, ensure_ascii=False)
            print(f"✅ 路径已更新 (user_id={user_id})")
        else:
            new_path = LearningPath(
                user_id=user_id,
                path_content=json.dumps(path_content, ensure_ascii=False)
            )
            db.session.add(new_path)
            print(f"✅ 路径已创建 (user_id={user_id})")
        db.session.commit()
    except Exception as e:
        print(f"⚠️ 路径保存失败: {e}")

    return jsonify({
        "code": 200,
        "msg": "路径生成成功",
        "data": path_content
    })


@path_bp.route("/get", methods=["GET"])
def get_path():
    from app import db, LearningPath
    """
    查询用户的学习路径
    """
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"code": 400, "msg": "缺少 user_id 参数"}), 400

    try:
        path_record = LearningPath.query.filter_by(user_id=user_id).first()
        if not path_record:
            return jsonify({
                "code": 404,
                "msg": "该用户暂无学习路径，请先生成",
                "data": None
            })

        # 解析 JSON
        path_content = json.loads(path_record.path_content)
        return jsonify({
            "code": 200,
            "msg": "获取路径成功",
            "data": path_content
        })
    except Exception as e:
        return jsonify({"code": 500, "msg": f"查询失败: {str(e)}"}), 500