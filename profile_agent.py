# services/profile_agent.py
def extract_profile(user_msg: str, answer: str):
    """
    画像抽取函数（占位版本）
    算法同学后续会替换为真实的大模型抽取逻辑
    """
    # 临时返回固定维度，让接口先跑通
    return {
        "knowledge_base": "中等",
        "cognitive_style": "视觉型",
        "weak_points": "面向对象编程",
        "learning_preference": "案例驱动",
        "goal_level": "进阶",
        "active_time": "晚间"
    }