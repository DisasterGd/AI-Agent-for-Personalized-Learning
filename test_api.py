import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_api(method, url, data=None):
    full_url = f"{BASE_URL}{url}"
    try:
        if method.upper() == "GET":
            resp = requests.get(full_url, params=data, timeout=5)
        else:
            resp = requests.post(full_url, json=data, timeout=10)
        print(f"{method} {url} → 状态码: {resp.status_code}")
        if resp.status_code == 200:
            print(f"  返回: {json.dumps(resp.json(), ensure_ascii=False)[:200]}...")
        else:
            print(f"  ❌ 错误: {resp.text[:200]}")
        return resp
    except Exception as e:
        print(f"{method} {url} → ❌ 连接失败: {e}")
        return None

print("=" * 50)
print("开始测试所有接口...")
print("=" * 50)

# 1. 健康检查
test_api("GET", "/")

# 2. 向量库路径
test_api("GET", "/vector/path")

# 3. 对话接口（SSE 流式，只测试是否能连接）
print("\n[3] POST /api/chat → 测试流式连接...")
try:
    resp = requests.post(
        f"{BASE_URL}/api/chat",
        json={"user_id": "1", "message": "什么是设计模式？"},
        timeout=20
    )
    if resp.status_code == 200:
        print("  ✅ 对话接口连接正常（SSE 流式）")
    else:
        print(f"  ❌ 返回状态码: {resp.status_code}")
except Exception as e:
    print(f"  ❌ 连接失败: {e}")

# 4. 资源生成接口
test_api("POST", "/api/resource/generate", {"user_id": 1, "topic": "设计模式"})

# 5. 路径生成接口
test_api("POST", "/api/path/generate", {"user_id": 1, "topic": "Python数据分析"})

# 6. 路径查询接口
test_api("GET", "/api/path/get", {"user_id": 1})

# 7. 画像更新接口
test_api("POST", "/api/profile/update", {
    "user_id": 1,
    "profile": {
        "knowledge_base": "中等",
        "cognitive_style": "视觉型",
        "weak_points": "面向对象编程",
        "learning_preference": "案例驱动",
        "goal_level": "进阶",
        "active_time": "晚间"
    }
})

print("=" * 50)
print("测试完成！")