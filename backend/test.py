# 测试千问密钥是否有效
import requests

API_KEY = "sk-sdqwayufizuemhadjtzngpaxcwllxdphazrcjujthvjjaiyc"

url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
data = {
    "model": "qwen-turbo",
    "input": {"messages": [{"role": "user", "content": "你好"}]}
}

response = requests.post(url, headers=headers, json=data)
print("状态码:", response.status_code)
print("返回内容:", response.text)