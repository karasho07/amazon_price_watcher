from flask import Flask, render_template_string, request, redirect
from models import db, Product
import os
import threading
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI", "sqlite:///products.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")


# 価格取得処理
def get_price(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        price_text = None

        # パターン1
        whole = soup.select_one(".a-price-whole")
        fraction = soup.select_one(".a-price-fraction")
        if whole and fraction:
            price_text = whole.text.strip() + fraction.text.strip()

        # 数字だけ取り出す
        if price_text:
            return int("".join(filter(str.isdigit, price_text)))
        else:
            print("価格情報が見つかりません")
            return None
    except Exception as e:
        print(f"価格取得エラー: {e}")
        return None


# Discord通知処理
def send_discord_alert(name, price, threshold, url):
    if not DISCORD_WEBHOOK_URL:
        return
    message = f"🔔 **{name}** がしきい値（{threshold}円）を下回りました！\n現在価格: {price}円\n{url}"
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print(f"Discord通知失敗: {e}")


# 価格監視ループ
def watcher_loop():
    import time
    while True:
        print("監視ループ実行中")
        products = Product.query.all()
        for p in products:
            price = get_price(p.url)
            if price is None:
                print(f"{p.name} 価格取得失敗")
                continue
            print(f"{p.name} 現在価格: {price}円")
            if price <= p.threshold:
                send_discord_alert(p.name, price, p.threshold, p.url)
        time.sleep(3600)  # 1時間ごとに監視（テスト時は 60 にしてOK）


# HTMLテンプレート
HTML = """
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>価格ウォッチャー</title></head>
<body>
    <h1>価格ウォッチャー</h1>
    <form method="post" action="/add">
        名前: <input name="name"><br>
        URL: <input name="url"><br>
        閾値（円）: <input name="threshold" type="number"><br>
        <button type="submit">追加</button>
    </form>
    <hr>
    <ul>
        {% for p in products %}
        <li>{{ p.name }} - {{ p.url }} - {{ p.threshold }}円
            <form method="post" action="/delete" style="display:inline">
                <input type="hidden" name="id" value="{{ p.id }}">
                <button type="submit">削除</button>
            </form>
        </li>
        {% endfor %}
    </ul>
    {% if msg %}
    <p>{{ msg }}</p>
    {% endif %}
</body>
</html>
"""


# ルーティング
@app.route("/", methods=["GET"])
def index():
    products = Product.query.all()
    return render_template_string(HTML, products=products, msg=None)


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    url = request.form["url"]
    threshold = int(request.form["threshold"])
    db.session.add(Product(name=name, url=url, threshold=threshold))
    db.session.commit()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    pid = request.form["id"]
    product = Product.query.get(pid)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect("/")


# 起動処理
if __name__ == "__main__":
    with app.app_context():
        print("== DB初期化 ==")
        db.drop_all()
        db.create_all()
    threading.Thread(target=watcher_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
