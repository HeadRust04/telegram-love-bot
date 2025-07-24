import requests
import time
import datetime
import threading
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = '7766705322:AAH6rVSN0jgE0-7mrnrJCM0Vk9iDBGRRpZs'
CHAT_ID = -4919653671  # ✅ Your group chat ID as an integer (with minus sign)

running = False
emoji = "❤️"

def get_greeting():
    now = datetime.datetime.now().hour
    if 5 <= now < 12:
        return "Good morning lovely pieee ☀️"
    elif 12 <= now < 18:
        return "Good eveningg baby piee 🌇"
    else:
        return "Good night cutieee patootiee 🌙"

def send_message(text):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": text
    })

def love_loop():
    global running
    while running:
        send_message(f"I love you {emoji}")
        time.sleep(10)

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    global running, emoji
    data = request.json

    # 🔍 Save all incoming updates to debug.txt
    try:
        with open("debug.txt", "a") as f:
            f.write(str(data) + "\n\n")
    except Exception as e:
        print("Debug log error:", e)

    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if not text or not chat_id:
        return "Invalid message", 200

    # 🔐 DEBUG command — responds to anyone
    if text == "/debug":
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
            "chat_id": chat_id,
            "text": f"Your chat ID is: {chat_id}"
        })
        return "OK"

    # ✅ Restrict all other commands to your configured group
    if chat_id != CHAT_ID:
        return "Unauthorized", 403

    if text == "/startlove":
        if not running:
            running = True
            threading.Thread(target=love_loop).start()
            send_message("Started infinite love 🥰")
        else:
            send_message("Already running 💞")

    elif text == "/stoplove":
        running = False
        send_message("Stopped love messages 🛑")

    elif text.startswith("/setemoji"):
        parts = text.split(" ", 1)
        if len(parts) == 2:
            emoji = parts[1].strip()
            send_message(f"Emoji updated to {emoji} 🎉")

    elif text == "/greet":
        send_message(get_greeting())

    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
