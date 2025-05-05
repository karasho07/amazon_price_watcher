from flask import Flask, request, render_template_string
import threading
import requests
from bs4 import BeautifulSoup
import time
import json
import os

app = Flask(__name__)

# ✅ ご自身の Discord Webhook URL に変更してください！
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1368929606534697001/-IppnMnlCbbbWV2jwiT2yObA4xX_9OGTAqSswd9C2vzfVArV1Wbe3wMoRSN4q44-f9Gr"

DATA_FILE = "products.json"
PRODUCTS = []
watching = False

# -------------------- データ保存/読み込み --------------------

def load_products():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_products():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(PRODUCTS, f, ensure_ascii=False, indent=2)

# -------------------- 商品価格取得/通知 --------------------

def get_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        price_tag = soup.select_one("span.a-price span.a-offscreen")
        if price_tag:
            return int(price_tag.get_text(strip=True).replace("￥", "").replace(",", ""))
    except:
        pass
    return None

def send_discord_notify(message):
    try:
        data = {"content": message}
        requests.post(DISCORD_WEBHOOK_URL, json=data)
    except:
        pass

# -------------------- 監視ループ（別スレッド） --------------------

def watcher_loop():
    while True:
        print("--- 監視ループ実行中 ---")
        if watching:
            for p in PRODUCTS:
                price = get_price(p["url"])
                if price is None:
                    print(f"[{p['name']}] 価格取得失敗")
                    continue
                print(f"[{p['name']}] 現在の価格: {price}円")
                if price <= p["threshold"]:
                    send_discord_notify(
                        f"💸 {p['name']} が安くなった！\n現在価格: {price}円\nしきい値: {p['threshold']}円\n{p['url']}"
                    )
        time.sleep(30)  # ← テスト用に30秒ごとにチェック



# -------------------- Flaskルート --------------------

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
            delete_index = int(request.form["delete"])
            if 0 <= delete_index < len(PRODUCTS):
                deleted = PRODUCTS.pop(delete_index)
                save_products()
                msg = f"🗑 {deleted['name']} を削除しました"
        elif "name" in request.form and "url" in request.form and "threshold" in request.form:
            try:
                name = request.form["name"]
                url = request.form["url"]
                threshold = int(request.form["threshold"])
                PRODUCTS.append({"name": name, "url": url, "threshold": threshold})
                save_products()
                msg = f"✅ {name}（しきい値: {threshold}円）を追加しました！"
            except:
                msg = "⚠️ 入力が正しくありません"

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
                    <button name="delete" value="{{ loop.index0 }}">🗑 削除</button>
                </form>
            </li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html, products=PRODUCTS, watching=watching, msg=msg)

# -------------------- 起動処理 --------------------

if __name__ == "__main__":
    PRODUCTS = load_products()
    threading.Thread(target=watcher_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
