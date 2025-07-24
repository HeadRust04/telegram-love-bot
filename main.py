import requests
import time

BOT_TOKEN = '7766705322:AAH6rVSN0jgE0-7mrnrJCM0Vk9iDBGRRpZs'
CHAT_ID = -4919653671  # Replace with your group chat ID

MESSAGE = "I love you cutie patootie babyy pieeeeeeeeeeeeeeeeeeee ❤️"

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
