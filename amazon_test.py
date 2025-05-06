import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.co.jp/dp/B0D5XRM3TV"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

res = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(res.text, "html.parser")

# 価格表示部分を探す
whole = soup.select_one(".a-price-whole")
fraction = soup.select_one(".a-price-fraction")

print("whole:", whole)
print("fraction:", fraction)

# ページの最初の一部も表示（確認用）
print("HTML冒頭:", res.text[:500])
