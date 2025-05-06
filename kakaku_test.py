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
url = "https://www.amazon.co.jp/BANDAI-SPIRITS-%E6%96%B0%E6%A9%9F%E5%8B%95%E6%88%A6%E8%A8%98%E3%82%AC%E3%83%B3%E3%83%80%E3%83%A0W-%E3%82%A6%E3%82%A4%E3%83%B3%E3%82%B0%E3%82%AC%E3%83%B3%E3%83%80%E3%83%A0%E3%82%BC%E3%83%AD-%E8%89%B2%E5%88%86%E3%81%91%E6%B8%88%E3%81%BF%E3%83%97%E3%83%A9%E3%83%A2%E3%83%87%E3%83%AB/dp/B0D5XRM3TV/ref=sr_1_1?dib=eyJ2IjoiMSJ9.Ji9Duoeuf1JXJQZ9Bn6n8B6yD1HqFowDAweW_-aAn83GkwtJ6s4HFVo1pBqYVogvEkW8cMyQ7YAnH4d65RT5TaHRKHnuHN0yKAk6HqAfnObQJEODE_nushGM84uDJKBR7XxQNUcyHzWAnfS-FHKOZEv-KUGp1XenJnJIM4IfyT5PvzVOY6tgqAjM4LOblLIF3NxURzqO0--b0iZG7CfOuzSJIdORQc2fgTTAbBKxUqYMQRtgKpaFwZez8fIW8n9fqqph2dKbW6pRNwyvIUiRn5htbMX8r1yY8PnDWUuQvnI.FexcrMeGvaJZszw2AYylUp-CMlMcOYnAMta-xx8sm2U&dib_tag=se&keywords=%E3%82%A6%E3%82%A4%E3%83%B3%E3%82%B0%E3%82%AC%E3%83%B3%E3%83%80%E3%83%A0+sdmg&qid=1746447130&sr=8-1"
get_amazon_price(url)
