from flask import Flask, request, render_template_string
from models import db, Product
import threading
import time
import requests
from bs4 import BeautifulSoup
import os

def get_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        selectors = [
            "#priceblock_ourprice",         # 通常価格
            "#priceblock_dealprice",        # セール価格
            "#priceblock_pospromoprice",    # プロモ価格
            ".a-price .a-offscreen",        # 上記がない場合のフォールバック
        ]

        for selector in selectors:
            tag = soup.select_one(selector)
            if tag:
                price_text = tag.get_text(strip=True).replace("￥", "").replace(",", "")
                print(f"[DEBUG] マッチしたセレクタ: {selector}")
                print(f"現在価格: {price_text}円")
                return int(float(price_text))

        print("❌ 価格が見つかりませんでした。")
    except Exception as e:
        print("エラー:", e)
