from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

user_bp = Blueprint("user", __name__, url_prefix="/api/auth")
# 原from app import db, User已在两个函数内部导入

@user_bp.route("/register", methods=["POST"])
def register():
    from app import db, User  # 导入1
    try:
        data = request.get_json()
        username = data.get("student_id")
        password = data.get("password")
        name = data.get("name")
        major = data.get("major")

        if not username or not password:
            return jsonify({"success": False, "msg": "Username and password are required"})

        if User.query.filter_by(username=username).first():
            return jsonify({"success": False, "msg": "Username already exists"})

        hashed_pw = generate_password_hash(password)
        new_user = User(
            username=username,
            password=hashed_pw,
            name=name,
            major=major
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"success": True, "msg": "Register success"})

    except Exception as e:
        db.session.rollback()
        print(f"Registration failed: {str(e)}")
        return jsonify({"success": False, "msg": f"Register failed: {str(e)}"})

@user_bp.route("/login", methods=["POST"])
def login():
    from app import db, User  # 导入2
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"success": False, "msg": "Invalid username or password"})

        return jsonify({
            "success": True,
            "msg": "Login success",
            "token": "token_" + str(uuid.uuid4()),
            "user": {"student_id": user.username,
                     "id": user.id,
                     "name": user.name,
                     "major": user.major}
        })

    except Exception as e:
        return jsonify({"success": False, "msg": f"Login failed: {str(e)}"})

