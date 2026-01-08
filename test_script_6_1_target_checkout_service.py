from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/checkout", methods=["POST"])
def checkout():
    # 获取请求的JSON数据
    data = request.get_json()
    # 提取购物车商品列表，默认空列表
    items = data.get("items", [])
    # 空购物车返回400错误
    if not items:
        return jsonify({"error": "empty cart"}), 400
    # 计算商品总价（单价*数量求和）
    total = sum(i["price"] * i["quantity"] for i in items)
    # 返回成功响应
    return jsonify({"total": total, "status": "ok"}), 200

if __name__ == "__main__":
    # 启动Flask应用，监听本地5000端口，开启调试模式
    app.run(host="127.0.0.1", port=5000, debug=True)