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
url = "https://www.amazon.co.jp/MGSD-%E6%A9%9F%E5%8B%95%E6%88%A6%E5%A3%AB%E3%82%AC%E3%83%B3%E3%83%80%E3%83%A0SEED-%E3%83%95%E3%83%AA%E3%83%BC%E3%83%80%E3%83%A0%E3%82%AC%E3%83%B3%E3%83%80%E3%83%A0-%E8%89%B2%E5%88%86%E3%81%91%E6%B8%88%E3%81%BF%E3%83%97%E3%83%A9%E3%83%A2%E3%83%87%E3%83%AB-2619354/dp/B0BGNC9F44/ref=sr_1_1?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=QJNPHYEE4CB&dib=eyJ2IjoiMSJ9.tCwEfaHJbnWU1USuS6g85nJVIfPMIleZipOVqqkgT6c5pjakCBP1o2bbCiRlcKKBAJW9egXojeZYjaInS-NnxcQ1q75JIplcHc-0XSNrM06hQY_fMYK1KxwgEVAkwH8IJOvJZfduw_bJMeZ6PhqSvozj4b9umhntNNgtwxCRsmLBQt9XXPmc7CGYYHXzMMT1Rqo8v82Pg7cVI-Gi58qm4KBcF80hSROvsOfxU2F453hWyjvdNvglwCiaa0i1VIxa4yjlCvhYa3j0c6DN0U_ESQDMl6BbEICblQQY2J-8jpQ.fSqIWclKdUvwrggjDaiIe6CVQ3TxiIaX6Bop_KmDb2M&dib_tag=se&keywords=mg+sd&qid=1746447719&sprefix=mgsd%2Caps%2C164&sr=8-1"
get_amazon_price(url)
