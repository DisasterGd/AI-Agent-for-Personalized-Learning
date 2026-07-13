# profile_agent.py
import random

# 记录每个用户的对话轮次（内存临时存储，演示用）
_user_session_counter = {}

def extract_profile(user_msg: str, answer: str, user_id: str = None):
    """
    保底方案：关键词扫描 + 轮次计数，生成动态画像
    """
    # 1. 轮次递增
    if user_id:
        _user_session_counter[user_id] = _user_session_counter.get(user_id, 0) + 1
        round_num = _user_session_counter[user_id]
    else:
        round_num = 1

    # 2. 根据轮次调整进度（看起来在“学习进步”）
    if round_num <= 2:
        level = "入门"
        progress = "基础语法"
    elif round_num <= 5:
        level = "中等"
        progress = "核心概念"
    else:
        level = "进阶"
        progress = "综合应用"

    # 3. 关键词检测（简单粗暴）
    weak = "无"
    weak_map = {
        "多态": "面向对象编程",
        "继承": "面向对象编程",
        "递归": "递归思维",
        "SQL": "SQL联表查询",
        "数据库": "SQL联表查询",
        "设计模式": "设计模式理解",
        "单例": "设计模式理解",
        "API": "接口调用",
        "json": "数据解析"
    }
    for keyword, value in weak_map.items():
        if keyword in user_msg:
            weak = value
            break

    # 4. 返回6维画像
    return {
        "knowledge_base": level,
        "cognitive_style": "视觉型" if random.random() > 0.3 else "逻辑型",
        "weak_points": weak,
        "learning_preference": "案例驱动" if "案例" in user_msg else "概念驱动",
        "goal_level": progress,
        "active_time": "晚间" if "晚上" in user_msg else "灵活"
    }