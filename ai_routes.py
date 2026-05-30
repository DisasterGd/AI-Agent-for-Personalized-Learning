from flask import Blueprint, request, make_response
import requests
import json
from dotenv import load_dotenv
import os

# 加载 .env 环境变量
load_dotenv()

ai_bp = Blueprint("ai", __name__, url_prefix="/api")


@ai_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    user_id = data.get("user_id")

    if not user_msg:
        return make_response(json.dumps({"code": 400, "msg": "请输入内容"}), 400)

    # 读取DeepSeek密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")

    try:
        # DeepSeek V4 Pro 官方接口
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-v4-pro",  # 满血版固定填这个
            "messages": [{"role": "user", "content": user_msg}],
            "temperature": 0.7
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        print("DeepSeek状态码:", resp.status_code)
        res = resp.json()

        if resp.status_code == 200 and "choices" in res:
            ai_response = res["choices"][0]["message"]["content"]
        else:
            ai_response = f"调用失败: {resp.status_code} {res}"

    except Exception as e:
        print("DeepSeek报错详情:", str(e))
        ai_response = "服务暂时异常，请稍后再试"

        # 【新增】保存对话到数据库（延迟导入，避免循环依赖）
        if user_id:
            from app import db, ChatRecord
            new_record = ChatRecord(
                user_id=user_id,
                query=user_msg,
                response=ai_response
            )
            db.session.add(new_record)
            db.session.commit()

    # 返回前端格式不变
    result = {"choices": [{"message": {"content": ai_response}}]}
    return make_response(json.dumps(result, ensure_ascii=False), 200,
                         {"Content-Type": "application/json; charset=utf-8"})

