import requests
from bs4 import BeautifulSoup

def get_price(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        price_whole = soup.select_one(".a-price-whole")
        price_frac = soup.select_one(".a-price-fraction")

        if price_whole:
            price_text = f"{price_whole.text}{price_frac.text if price_frac else ''}"
            return int("".join(filter(str.isdigit, price_text)))
        else:
            print(f"[価格未取得] URL: {url}")
            return None

    except Exception as e:
        print(f"[例外発生] URL: {url}, Error: {e}")
        return None
