import requests
from bs4 import BeautifulSoup
import time

DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1368891025896112139/1TkU871HZ7s60opRi03QgLsj4Av-axnS8Zs8WYBlX394egEHwwTgvr3Z1kNQzI96HKaf"
AMAZON_URL = "https://www.amazon.co.jp/BANDAI-SPIRITS-%E6%96%B0%E6%A9%9F%E5%8B%95%E6%88%A6%E8%A8%98%E3%82%AC%E3%83%B3%E3%83%80%E3%83%A0W-%E3%82%A6%E3%82%A4%E3%83%B3%E3%82%B0%E3%82%AC%E3%83%B3%E3%83%80%E3%83%A0%E3%82%BC%E3%83%AD-%E8%89%B2%E5%88%86%E3%81%91%E6%B8%88%E3%81%BF%E3%83%97%E3%83%A9%E3%83%A2%E3%83%87%E3%83%AB/dp/B0D5XRM3TV/ref=sr_1_2?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=D81BJEXBFD07&dib=eyJ2IjoiMSJ9.3pfK86iwsPlJkMfl_rmo6yznHgHjMydROTjw1tOBjZNdku51Q2od3E77WEj5ISRJn8NBBw-peKUu_Mrgn8nRpZYbPfirQPOinkOvQhruIP2GqfgzipaxjOlEcucGW5o7weY9jWLtAUM2LIPo7xsdOzQoIsPwwCgfrWX4mu1VNC8fzaZi1c5eXwrvdDHjZur_4bYOmZ5y-UmEQtdBxuWnxn-7u42MDyap6akTDih91uz-KMmLZwL7qEOVMwVpMlmSFkdfZhjDCcld4JGv47glFFhdQqDo-_IjpbRz6zY6YlI.GBmTPKezJvl79TRm_domC3dgIDXzaU9xl2qJ8HLVyxw&dib_tag=se&keywords=SDMG&qid=1746437403&sprefix=sdmg%2Caps%2C178&sr=8-2"

# 通知を送る価格のしきい値（ここを変更）
PRICE_THRESHOLD = 4950

def send_discord_notify(message):
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def get_price_as_number(price_text):
    # ￥3,480 → 3480 のように数値に変換
    return int(price_text.replace("￥", "").replace(",", "").strip())

def check_price():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(AMAZON_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    price_tag = soup.select_one("span.a-price span.a-offscreen")
    if price_tag:
        price_text = price_tag.get_text(strip=True)
        price = get_price_as_number(price_text)
        print(f"現在の価格：{price}円")

        if price <= PRICE_THRESHOLD:
            send_discord_notify(f"💸 安くなったよ！\n現在の価格：{price}円\n{AMAZON_URL}")
        else:
            print("まだ安くなっていません")
    else:
        print("価格情報が見つかりませんでした")

# 定期実行（10分ごと）
while True:
    check_price()
    time.sleep(300)
