import os
import requests
from bs4 import BeautifulSoup

PRODUCT_URL = "https://shop.amul.com/en/product/amul-high-protein-rose-lassi-200-ml-or-pack-of-30"

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": False,
        },
        timeout=20,
    )

    response.raise_for_status()


def check_stock():
    response = requests.get(
        PRODUCT_URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(" ", strip=True).lower()

    sold_out = (
        "sold out" in page_text
        or "out of stock" in page_text
    )

    add_to_cart = "add to cart" in page_text

    if add_to_cart and not sold_out:
        return True

    return False


if __name__ == "__main__":

    try:
        in_stock = check_stock()

        if in_stock:
            send_telegram(
                "🚨 AMUL ROSE LASSI IS IN STOCK!\n\n"
                "Amul High Protein Rose Lassi\n"
                "200 mL | Pack of 30\n\n"
                "🛒 BUY NOW:\n"
                + PRODUCT_URL
            )

            print("IN STOCK — Telegram alert sent.")

        else:
            print("Still out of stock.")

    except Exception as e:
        print("Error:", e)
        raise
