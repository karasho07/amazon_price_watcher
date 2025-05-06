from flask import Flask, request, render_template_string
from models import db, Product
import threading
import time
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

watching = False

# 商品価格を取得する関数
def get_price(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # まず従来のセレクタ
        price_tag = soup.select_one(
            "#twister-plus-price-data-price, #priceblock_ourprice, #priceblock_dealprice, #price_inside_buybox"
        )

        if not price_tag:
            # 新しい価格形式に対応
            whole = soup.select_one(".a-price-whole")
            fraction = soup.select_one(".a-price-fraction")
            if whole:
                price_text = whole.text.replace(",", "")
                if fraction:
                    price_text += "." + fraction.text
                return int(float(price_text))  # 小数も対応

        else:
            price_text = price_tag.text.replace("￥", "").replace(",", "").strip()
            return int(float(price_text))

    except Exception as e:
        print("価格取得エラー：", e, flush=True)


# Discord通知（必要なら）
def send_discord_notify(msg):
    webhook = os.environ.get("https://discordapp.com/api/webhooks/1368929606534697001/-IppnMnlCbbbWV2jwiT2yObA4xX_9OGTAqSswd9C2vzfVArV1Wbe3wMoRSN4q44-f9Gr")
    if webhook:
        try:
            requests.post(webhook, json={"content": msg})
        except:
            pass

# 監視ループ
def watcher_loop():
    print("★ 監視ループが開始されました", flush=True)
    while True:
        if watching:
            with app.app_context():
                for product in Product.query.all():
                    price = get_price(product.url)
                    if price is None:
                        print(f"{product.name} → 価格取得失敗", flush=True)
                        continue
                    print(f"[{product.name}] 現在価格: {price}円", flush=True)
                    if price <= product.threshold:
                        send_discord_notify(
                            f"🔔 {product.name} が安くなった！\n現在価格: {price}円\nしきい値: {product.threshold}円\n{product.url}"
                        )
        time.sleep(300)  # 5分おき

# Webルート
@app.route("/", methods=["GET", "POST"])
def index():
    global watching
    msg = ""

    if request.method == "POST":
        if "start" in request.form:
            watching = True
            msg = "✅ 監視を開始しました！"
        elif "stop" in request.form:
            watching = False
            msg = "🛑 監視を停止しました。"
        elif "delete" in request.form:
            delete_id = int(request.form["delete"])
            product = Product.query.get(delete_id)
            if product:
                db.session.delete(product)
                db.session.commit()
                msg = f"🗑 {product.name} を削除しました"
        elif "name" in request.form and "url" in request.form and "threshold" in request.form:
            try:
                name = request.form["name"]
                url = request.form["url"]
                threshold = int(request.form["threshold"])
                new_product = Product(name=name, url=url, threshold=threshold)
                db.session.add(new_product)
                db.session.commit()
                msg = f"✅ {name}（しきい値: {threshold}円）を追加しました！"
            except:
                msg = "⚠️ 入力が正しくありません"

    products = Product.query.all()
    html = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>Amazon価格監視アプリ</title>
        <style>
            body { font-family: sans-serif; margin: 20px; }
            input { margin-bottom: 5px; }
            li { margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <h2>Amazon価格監視アプリ</h2>

        <form method="post">
            商品名：<input name="name" placeholder="例：ガンダム" required><br>
            商品URL：<input name="url" placeholder="https://www.amazon.co.jp/..." required><br>
            しきい値（円）：<input name="threshold" type="number" placeholder="例：4900" required><br>
            <button type="submit">商品を追加</button>
        </form>

        <form method="post" style="margin-top: 10px;">
            <button name="start">▶ 監視開始</button>
            <button name="stop">■ 監視停止</button>
        </form>

        <p>{{ msg }}</p>
        <hr>

        <h3>登録商品（{{ "監視中" if watching else "停止中" }}）</h3>
        <ul>
        {% for p in products %}
            <li>
                <a href="{{ p.url }}" target="_blank"><strong>{{ p.name }}</strong></a>
                （しきい値：{{ p.threshold }}円）
                <form method="post" style="display:inline">
                    <button name="delete" value="{{ p.id }}">🗑 削除</button>
                </form>
            </li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html, products=products, watching=watching, msg=msg)

# 起動処理
if __name__ == "__main__":
    with app.app_context():
        print("== DBリセット ==")
        db.drop_all()
        db.create_all()

    threading.Thread(target=watcher_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



