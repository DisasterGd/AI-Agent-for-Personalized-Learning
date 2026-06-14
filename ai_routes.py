from flask import Blueprint, request, make_response, jsonify
from openai import OpenAI
from config import Config
import json
from dotenv import load_dotenv
import os

load_dotenv()

ai_bp = Blueprint("ai", __name__, url_prefix="/api")


@ai_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    user_id = data.get("user_id", "guest")

    if not user_msg:
        return make_response(jsonify({"code": 400, "msg": "请输入内容"}), 400)

    try:
        client = OpenAI(
            api_key=Config.DEEPSEEK_API_KEY,
            base_url=Config.DEEPSEEK_BASE_URL
        )

        # 开启流式输出
        stream_response = client.chat.completions.create(
            model=Config.DEEPSEEK_MODEL_NAME,
            messages=[{"role": "user", "content": user_msg}],
            stream=True,
            temperature=0.7
        )

        # 逐块接收并拼接完整回复
        full_response = ""
        for chunk in stream_response:
            # 流式响应中，每个 chunk 的 choices[0].delta.content 包含新内容
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta.content:
                    content_piece = delta.content
                    full_response += content_piece
                    # 如果你需要实时推送给前端，可以在这里通过 WebSocket 或 SSE 发送

        ai_response = full_response if full_response else "未获取到有效回复"

    except Exception as e:
        print("DeepSeek报错:", str(e))
        ai_response = "服务暂时异常，请稍后再试"

    # 保存到数据库（处理 user_id 类型问题，见错误2）
    try:
        # 只有当 user_id 是有效的整数时才保存
        if user_id and user_id != "guest":
            # 确保 user_id 是整数
            user_id_int = int(user_id)
            # 可选：检查该用户是否存在
            from app import User
            user_exists = User.query.get(user_id_int)
            if user_exists:
                new_record = ChatRecord(
                    user_id=user_id_int,
                    query=user_msg,
                    response=ai_response
                )
                db.session.add(new_record)
                db.session.commit()
    except ValueError:
        print(f"无效的 user_id 格式: {user_id}，跳过保存")
    except Exception as e:
        print("数据库保存失败:", str(e))

    result = {"choices": [{"message": {"content": ai_response}}]}
    return make_response(jsonify(result), 200, {"Content-Type": "application/json; charset=utf-8"})
# from flask import Blueprint, request, make_response
# import requests
# import json
# from dotenv import load_dotenv
# import os
#
# # 加载 .env 环境变量
# load_dotenv()
#
# ai_bp = Blueprint("ai", __name__, url_prefix="/api")
#
#
# @ai_bp.route("/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     user_msg = data.get("message", "")
#     user_id = data.get("user_id")
#
#     if not user_msg:
#         return make_response(json.dumps({"code": 400, "msg": "请输入内容"}), 400)
#
#     # 读取DeepSeek密钥
#     api_key = os.getenv("DEEPSEEK_API_KEY")
#
#     try:
#         # DeepSeek V4 Pro 官方接口
#         url = "https://api.deepseek.com/v1/chat/completions"
#         headers = {
#             "Authorization": f"Bearer {api_key}",
#             "Content-Type": "application/json"
#         }
#         payload = {
#             "model": "deepseek-v4-pro",  # 满血版固定填这个
#             "messages": [{"role": "user", "content": user_msg}],
#             "temperature": 0.7
#         }
#
#         resp = requests.post(url, json=payload, headers=headers, timeout=30)
#         print("DeepSeek状态码:", resp.status_code)
#         res = resp.json()
#
#         if resp.status_code == 200 and "choices" in res:
#             ai_response = res["choices"][0]["message"]["content"]
#         else:
#             ai_response = f"调用失败: {resp.status_code} {res}"
#
#     except Exception as e:
#         print("DeepSeek报错详情:", str(e))
#         ai_response = "服务暂时异常，请稍后再试"
#
#         # 【新增】保存对话到数据库（延迟导入，避免循环依赖）
#         if user_id:
#             from app import db, ChatRecord
#             new_record = ChatRecord(
#                 user_id=user_id,
#                 query=user_msg,
#                 response=ai_response
#             )
#             db.session.add(new_record)
#             db.session.commit()
#
#     # 返回前端格式不变
#     result = {"choices": [{"message": {"content": ai_response}}]}
#     return make_response(json.dumps(result, ensure_ascii=False), 200,
#                          {"Content-Type": "application/json; charset=utf-8"})

