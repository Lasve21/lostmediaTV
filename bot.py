import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, threaded=False)  # <-- aggiunto threaded=False
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.stream.read().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def index():
    return "Bot attivo!", 200

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Ciao! 🎬 Sono il tuo bot per le serie TV.")
