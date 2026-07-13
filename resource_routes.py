from flask import Blueprint, request, jsonify
import time,json


resource_bp = Blueprint("resource", __name__, url_prefix="/api/resource")


@resource_bp.route("/generate", methods=["POST"])
def generate_resources():
    from app import db, LearningResource
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "msg": "请求体必须为 JSON"}), 400

    user_id = data.get("user_id")
    topic = data.get("topic", "面向对象编程")
    # ... 后续代码

    # 模拟生成耗时
    time.sleep(1.5)

    # 根据 topic 替换占位符
    mock_resources = {
        "doc": {
            "title": f"{topic} 核心概念解析",
            "content": f"这是一份关于 {topic} 的详细讲解文档。\n\n## 1. {topic} 的定义\n{topic} 是计算机科学中的重要概念...\n\n## 2. 应用场景\n在软件开发中，{topic} 广泛应用于..."
        },
        "mindmap": {
            "nodes": [
                {"id": "1", "label": topic, "children": [
                    {"id": "2", "label": f"{topic} 的核心原理"},
                    {"id": "3", "label": f"{topic} 的实战案例"},
                    {"id": "4", "label": f"{topic} 的常见误区"}
                ]}
            ]
        },
        "exercises": [
            {"question": f"以下关于 {topic} 的说法，哪一个是正确的？",
             "options": ["选项A：描述1", "选项B：描述2", "选项C：描述3", "选项D：描述4"], "answer": "B"},
            {"question": f"{topic} 的核心思想是什么？", "options": ["思想A", "思想B", "思想C", "思想D"], "answer": "A"}
        ],
        "code": {
            "language": "python",
            "content": f"# {topic} 示例代码\nclass {topic.replace(' ', '')}Example:\n    def __init__(self):\n        print('初始化 {topic}')\n    \n    def run(self):\n        print('执行 {topic} 逻辑')\n        return True"
        },
        "video_script": {
            "scenes": [
                {"scene": 1, "duration": "0:00-0:30", "visual": f"{topic} 概念图",
                 "narration": f"大家好，今天我们学习 {topic}..."},
                {"scene": 2, "duration": "0:30-1:30", "visual": f"{topic} 流程演示",
                 "narration": f"首先，我们来看 {topic} 的核心步骤..."},
                {"scene": 3, "duration": "1:30-2:30", "visual": f"{topic} 案例实战",
                 "narration": f"接下来，通过一个实际案例深入理解 {topic}"}
            ]
        }
    }
    # 保存到数据库（可选，非阻塞）
    try:
        new_res = LearningResource(
            user_id=user_id,
            resource_type="doc",
            content=json.dumps(mock_resources)  # 存整个 JSON
        )
        db.session.add(new_res)
        db.session.commit()
    except Exception as e:
        print(f"⚠️ 资源保存失败: {e}")
    return jsonify({
        "code": 200,
        "msg": "资源生成成功",
        "data": mock_resources,
        "topic": topic
    })
