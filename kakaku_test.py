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
url = "https://www.amazon.co.jp/SPIRITS-%E6%A9%9F%E5%8B%95%E6%88%A6%E5%A3%AB%E3%82%AC%E3%83%B3%E3%83%80-FREEDOM-%E3%82%AA%E3%83%97%E3%82%B7%E3%83%A7%E3%83%B3%E3%83%91%E3%83%BC%E3%83%84%E3%82%BB%E3%83%83%E3%83%88-%E3%82%AD%E3%83%A3%E3%83%90%E3%83%AA%E3%82%A2%E3%83%BC%E3%82%A2%E3%82%A4%E3%83%95%E3%83%AA%E3%83%83%E3%83%89/dp/B0DV98PNNV/ref=sr_1_2?crid=35BH3BSR2CAVH&dib=eyJ2IjoiMSJ9.Deo3tSE1SMDf2IFeudpqOF2gdHAKjzdXYLPTSQzLqKRAP4wYcsMMkmI7MI-WK2q9bzpw0zrJ3ak_CVIOxjT3tP2Vym4Xp3lq8IOcrzTSDDxncQdREjR4E9do8Hi_0KNug7ubjO0CcPv972vlB0x-DS9VA7OB3hPBMew4ssqeDiMDqNrCKFZ6CVwtAhMmPnoiLDQMqoxKWH7QQTe5pPae_nZ5yLSmEOC1khuodVDTc3vyB1RRKhmzi7n_QFqtJaQfBJLphpKTVPdzCDIuZz9S-YILxOX5_oYRcO1ugHt-o6U.XIkWAx6AvCJ7HZWaKJgYCcDys9HOfdN8isxcdCcyHQg&dib_tag=se&keywords=%E3%82%AD%E3%83%A3%E3%83%90%E3%83%AA%E3%82%A2%E3%82%A2%E3%82%A4%E3%83%95%E3%83%AA%E3%83%83%E3%83%89&qid=1746513180&sprefix=%E3%81%8D%E3%82%83%E3%81%B0%E3%82%8A%E3%81%82%2Caps%2C169&sr=8-2"
get_amazon_price(url)
