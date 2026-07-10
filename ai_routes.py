from flask import Blueprint, request, Response, stream_with_context, make_response, jsonify
from openai import OpenAI
from config import Config
from services.rag_service import rag_chat
from app import db, User, ChatRecord
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

ai_bp = Blueprint("ai", __name__, url_prefix="/api")


# ================= 独立 SSE 生成器函数（方案三） =================
def generate_sse_events(user_msg, user_id):
    """
    独立的 SSE 事件生成器
    :param user_msg: 用户消息
    :param user_id: 用户ID（字符串，可能是 "guest"）
    :yield: SSE 格式的数据流
    """
    # 1. 推送“检索中”状态
    yield f"data: {json.dumps({'type': 'step', 'content': '🔍 正在知识库中检索相关内容...'})}\n\n"

    try:
        # 2. 调用 RAG 检索 + 大模型生成
        answer, source_docs = rag_chat(user_msg, top_k=2)
    except Exception as e:
        error_msg = f"RAG 服务异常: {str(e)}"
        print(f"❌ {error_msg}")
        yield f"data: {json.dumps({'type': 'error', 'content': error_msg})}\n\n"
        return

    # 3. 推送引用来源
    sources = [doc.metadata.get("file_name", "未知文档") for doc in source_docs]
    yield f"data: {json.dumps({'type': 'sources', 'content': sources})}\n\n"

    # 4. 推送“生成回答”状态
    yield f"data: {json.dumps({'type': 'step', 'content': '✍️ 正在生成回答...'})}\n\n"

    # 5. 模拟流式逐词推送
    words = answer.split(' ')
    total = len(words)
    for idx, word in enumerate(words):
        chunk = word + (' ' if idx < total - 1 else '')
        yield f"data: {json.dumps({'type': 'text', 'content': chunk})}\n\n"
        time.sleep(0.05)  # 打字速度控制

    # 6. 保存对话记录到数据库（在流式结束后）
    try:
        if user_id and user_id != "guest":
            user_id_int = int(user_id)
            user_exists = User.query.get(user_id_int)
            if user_exists:
                new_record = ChatRecord(
                    user_id=user_id_int,
                    query=user_msg,
                    response=answer
                )
                db.session.add(new_record)
                db.session.commit()
                print(f"✅ 对话记录已保存 (user_id={user_id_int})")
    except ValueError:
        print(f"⚠️ 无效的 user_id 格式: {user_id}，跳过保存")
    except Exception as e:
        print(f"❌ 数据库保存失败: {str(e)}")

    # 7. 异步触发画像更新（不阻塞用户）
    try:
        import threading
        from profile_routes import async_update_profile
        if user_id and user_id != "guest":
            threading.Thread(
                target=async_update_profile,
                args=(int(user_id), user_msg, answer),
                daemon=True
            ).start()
            print(f"🔄 已触发画像更新任务 (user_id={user_id})")
    except Exception as e:
        print(f"⚠️ 触发画像更新失败: {e}")

    # 8. 发送完成信号（done 放在最后）
    yield f"data: {json.dumps({'type': 'done'})}\n\n"


# ================= 路由接口 =================
@ai_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    user_id = data.get("user_id", "guest")

    if not user_msg:
        return make_response(jsonify({"code": 400, "msg": "请输入内容"}), 400)

    # 返回 SSE 流式响应，调用独立的生成器函数
    return Response(
        stream_with_context(generate_sse_events(user_msg, user_id)),
        mimetype='text/event-stream'
    )
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

