from locust import HttpUser, task, between
import random
import string

# 生成随机用户名（避免重复，适配SQLite唯一索引）
def generate_random_username():
    return "user_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

class UserBehavior(HttpUser):
    # 模拟用户思考时间：0.5-1秒（贴近真实场景）
    wait_time = between(0.5, 1)

    # 核心任务：并发注册
    @task(1)
    def register(self):
        username = generate_random_username()
        password = "123456abc"  # 固定密码，简化测试
        self.client.post(
            "/register",
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json"}
        )

# 测试配置：
# 200并发用户，每秒生成20个用户（10秒达峰）
# 目标地址：http://127.0.0.1:5000