import requests
from bs4 import BeautifulSoup

def get_price(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # 複数のセレクタで価格を探す
        selectors = [
            ".a-price .a-offscreen",
            "#priceblock_ourprice",
            "#priceblock_dealprice",
            ".a-price-whole"
        ]

        price_text = None
        for sel in selectors:
            tag = soup.select_one(sel)
            if tag:
                price_text = tag.get_text(strip=True)
                break

        if price_text is None:
            print("価格情報が見つかりません")
            return None

        # 数字だけを抽出（カンマや「円」を除去）
        return int("".join(filter(str.isdigit, price_text)))

    except Exception as e:
        print(f"価格取得エラー: {e}")
        return None


# テスト実行部分
if __name__ == "__main__":
    url = "https://www.amazon.co.jp/dp/B0D5XRM3TV"
    price = get_price(url)
    print("取得価格:", price)
