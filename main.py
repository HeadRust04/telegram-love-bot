import requests
import time

BOT_TOKEN = 'PASTE_YOUR_TOKEN_HERE'
CHAT_ID = -1001234567890  # Replace with your group chat ID

MESSAGE = "I love you ❤️"

def send_love():
    while True:
        try:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
                "chat_id": CHAT_ID,
                "text": MESSAGE
            })
            time.sleep(10)
        except Exception as e:
            print("Error:", e)
            time.sleep(15)

if __name__ == "__main__":
    send_love()
