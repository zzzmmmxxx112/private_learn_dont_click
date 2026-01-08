import requests, multiprocessing, time
from test_script_6_1_target_checkout_service import app
def run_server():
    app.run(port=5000)
def test_checkout_total():
    p = multiprocessing.Process(target=run_server)
    p.start(); time.sleep(1)
    data = {"items": [{"price": 20, "quantity": 3}]}
    res = requests.post("http://127.0.0.1:5000/checkout", json=data)
    assert res.status_code == 200
    assert res.json()["total"] == 60
    p.terminate()