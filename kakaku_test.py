import requests
from bs4 import BeautifulSoup

def get_amazon_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        selectors = [
            ".a-price .a-offscreen",  # 通常価格・セール価格
            "#priceblock_ourprice",
            "#priceblock_dealprice",
            "#priceblock_pospromoprice",
        ]

        for selector in selectors:
            tag = soup.select_one(selector)
            if tag:
                price_text = tag.text.strip().replace(",", "").replace("￥", "")
                print(f"[DEBUG] マッチしたセレクタ: {selector}")
                print(f"現在価格: {price_text}円")
                return int("".join(filter(str.isdigit, price_text)))
        
        print("❌ 価格が見つかりませんでした。")
    except Exception as e:
        print("エラー:", e)

# ここに取得したい商品のURLを入れる
url = "https://www.amazon.co.jp/BANDAI-SPIRITS-%E3%82%A2%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3%E3%83%99%E3%83%BC%E3%82%B97-%E3%83%97%E3%83%A9%E3%82%B9%E3%83%81%E3%83%83%E3%82%AF%E8%A3%BD-%E3%83%87%E3%82%A3%E3%82%B9%E3%83%97%E3%83%AC%E3%82%A4%E3%82%B9%E3%82%BF%E3%83%B3%E3%83%89/dp/B0CJLGVDLJ/ref=sr_1_2?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=39K6CFR116VMM&dib=eyJ2IjoiMSJ9.9sVmoHmQkaQ77Kk84QIkfQMQoX_dY8mgq_-VCv8VWPxUNnEp2UsEdB91cwUEvwoX59BDlUY-zmpckHaN1_vsnxaZHITOOuOmjCzs120srBAq69O9VI4KTEsxQjPPbhqb6M2nfvexk3iOVA6tg7Pl-Ld8r-g0g19aVTAJdxk0yeP_AFRCKO-CzsjadRo6s0WiuVR2CzKvubNQd2Lg3v9Ks7MQ_OFCXNefOQkYcPdU2MIwqIu-jyazBYQVgHwHkfnB8sLccP0TqKc--dsdZhL1cr2rJzJT1iltU6pZacf8-0c.ZHvW6ueRZb6KObO3OtBSVlaPc0aD4A6MK7mgl79BRF8&dib_tag=se&keywords=%E3%82%A2%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3%E3%83%99%E3%83%BC%E3%82%B97&qid=1746531160&sprefix=%E3%82%A2%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3%E3%83%99%E3%83%BC%E3%82%B97%2Caps%2C183&sr=8-2&th=1"
get_amazon_price(url)
