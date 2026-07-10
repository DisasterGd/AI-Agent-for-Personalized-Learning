from flask import Blueprint, request, jsonify
from app import db, UserProfile
import json
import threading

profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")


@profile_bp.route("/update", methods=["POST"])
def update_profile():
    """更新用户6维画像（覆盖更新）"""
    data = request.get_json()
    user_id = data.get("user_id")
    profile = data.get("profile")  # 字典：{knowledge_base, cognitive_style, ...}

    if not user_id or not profile:
        return jsonify({"code": 400, "msg": "缺少 user_id 或 profile"})

    # 检查必需维度
    required = ["knowledge_base", "cognitive_style", "weak_points", "learning_preference", "goal_level", "active_time"]
    missing = [k for k in required if k not in profile]
    if missing:
        return jsonify({"code": 400, "msg": f"缺少维度: {', '.join(missing)}"})

    try:
        # 查找是否存在
        existing = UserProfile.query.filter_by(user_id=int(user_id)).first()
        if existing:
            # 覆盖更新
            for key in required:
                setattr(existing, key, profile.get(key))
        else:
            # 新建
            new_profile = UserProfile(user_id=int(user_id), **profile)
            db.session.add(new_profile)
        db.session.commit()
        return jsonify({"code": 200, "msg": "画像更新成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "msg": f"更新失败: {str(e)}"})


# 供 ai_routes 调用的辅助函数（异步触发）
def async_update_profile(user_id, user_msg, answer):
    """
    异步调用画像更新（在后台线程中执行）
    """
    # 需要算法同学提供 extract_profile 函数
    try:
        from services.profile_agent import extract_profile
        profile_data = extract_profile(user_msg, answer)
        if profile_data:
            # 调用自身的接口更新数据库
            import requests
            requests.post(
                "http://127.0.0.1:5000/api/profile/update",
                json={"user_id": user_id, "profile": profile_data},
                timeout=5
            )
    except Exception as e:
        print(f"⚠️ 画像更新失败: {e}")