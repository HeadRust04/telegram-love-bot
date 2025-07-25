import requests
import time
import datetime
import threading
import random
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = '7766705322:AAH6rVSN0jgE0-7mrnrJCM0Vk9iDBGRRpZs'
CHAT_ID = -1002868780439  # ✅ Updated to correct group ID

running = False
emoji = "❤️"
love_interval = 10  # seconds
nickname = "pieee"
memory = []
mood = "romantic"
theme = "default"
scheduled_messages = {}  # {"08:00": "Good morning, baby!"}

# ✅ Send message with full debug
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    r = requests.post(url, data=payload)
    print("SendMessage Response:", r.status_code, r.text, flush=True)

def get_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return f"Good morning lovely {nickname} ☀️"
    elif 12 <= hour < 18:
        return f"Good eveningg {nickname} 🌇"
    else:
        return f"Good night cutieee {nickname} 🌙"

# ✅ Love loop
def love_loop():
    global running
    while running:
        if theme == "cute":
            text = f"Hey {nickname}, I love you {emoji}"
        elif theme == "gentle":
            text = f"Just a soft reminder, you're my everything {emoji}"
        elif theme == "flirty":
            text = f"Damn {nickname}, falling for you again {emoji}"
        else:
            text = f"I love you {emoji}"
        send_message(text)
        time.sleep(love_interval)

# ✅ Scheduler thread
def scheduler_loop():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now in scheduled_messages:
            send_message(scheduled_messages[now])
        time.sleep(60)

threading.Thread(target=scheduler_loop, daemon=True).start()

# ✅ Webhook handler
@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    global running, emoji, love_interval, nickname, memory, mood, theme, scheduled_messages
    data = request.json
    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    print("Incoming Update:", data, flush=True)
    send_message(f"Debug: Received '{text}'")  # ✅ always reply for now

    if chat_id != CHAT_ID:
        return "OK"

    if text.startswith("/startlove"):
        if not running:
            running = True
            threading.Thread(target=love_loop).start()
            send_message("Started infinite love 🥰")
        else:
            send_message("Already running 💕")

    elif text.startswith("/stoplove"):
        running = False
        send_message("Stopped love messages 🛑")

    elif text.startswith("/setemoji"):
        parts = text.split(" ", 1)
        if len(parts) == 2:
            emoji = parts[1].strip()
            send_message(f"Emoji updated to {emoji} 🎉")

    elif text.startswith("/greet"):
        send_message(get_greeting())

    elif text.startswith("/burst"):
        for _ in range(5):
            send_message(f"I love you {emoji}")

    elif text.startswith("/lovemeter"):
        percent = random.randint(75, 100)
        send_message(f"Your love today is: {percent}% {emoji}")

    elif text.startswith("/surprise"):
        options = [
            f"Just thinking of you {emoji}",
            f"Hey {nickname}, you're my whole world 🌍",
            f"You're my favorite notification 😍",
            f"You + Me = ❤️"
        ]
        send_message(random.choice(options))

    elif text.startswith("/every"):
        parts = text.split(" ", 1)
        if len(parts) == 2 and parts[1].isdigit():
            love_interval = int(parts[1])
            send_message(f"Love interval set to {love_interval} seconds ⏱")

    elif text.startswith("/nickname set"):
        parts = text.split(" ", 2)
        if len(parts) == 3:
            nickname = parts[2]
            send_message(f"Nickname updated to {nickname} 💍")

    elif text.startswith("/nickname"):
        send_message(f"Your current nickname is: {nickname}")

    elif text.startswith("/settheme"):
        parts = text.split(" ", 1)
        if len(parts) == 2:
            theme = parts[1].strip().lower()
            send_message(f"Theme set to: {theme} 🎨")

    elif text.startswith("/randomlove"):
        lines = [
            f"Falling for you more every day, {nickname} 😍",
            f"You light up my heart ✨",
            f"Tera naam lete hi smile aa jaati hai 😘",
            f"Tum ho, to sab kuch hai. ❤️",
            f"Your smile is my favorite thing ever 🤩",
            f"I'd pause my game for you. And that's saying a lot. 😂"
        ]
        send_message(random.choice(lines))

    elif text.startswith("/memory add"):
        parts = text.split(" ", 2)
        if len(parts) == 3:
            memory.append(parts[2])
            send_message("Memory saved 📓")

    elif text.startswith("/memory recall"):
        if memory:
            send_message(f"Remember this? {random.choice(memory)}")
        else:
            send_message("No memories saved yet 😢")

    elif text.startswith("/mood"):
        parts = text.split(" ", 1)
        if len(parts) == 2:
            mood = parts[1]
            send_message(f"Mood set to {mood} 🤍")

    elif text.startswith("/schedule"):
        parts = text.split(" ", 2)
        if len(parts) == 3:
            time_str = parts[1].strip()
            msg = parts[2].strip()
            scheduled_messages[time_str] = msg
            send_message(f"Scheduled daily message at {time_str} ⏰")

    elif text.startswith("/unschedule"):
        parts = text.split(" ", 1)
        if len(parts) == 2:
            time_str = parts[1].strip()
            if time_str in scheduled_messages:
                del scheduled_messages[time_str]
                send_message(f"Removed scheduled message at {time_str} ❌")
            else:
                send_message(f"No message scheduled at {time_str} ❓")

    elif text.startswith("/debug"):
        send_message(f"Your chat ID is: {chat_id}")

    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
