# bot.py - semplice bot Telegram via webhook (usare su Render)
import os
from flask import Flask, request
import telebot

TOKEN = os.environ.get("BOT_TOKEN")        # -> preso da Render (mai nel codice)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # -> impostata su Render

if not TOKEN:
    raise RuntimeError("Errore: imposta la variabile d'ambiente BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- comandi del bot ---
@bot.message_handler(commands=['start'])
def on_start(message):
    bot.send_message(message.chat.id, "Ciao! Bot attivo ✅")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"Hai detto: {message.text}")

# --- endpoint webhook per Telegram ---
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "", 200

# --- root semplice per test ---
@app.route("/", methods=['GET'])
def index():
    return "Bot up"

# --- imposta il webhook (verrà eseguito all'import; utile con gunicorn su Render) ---
if WEBHOOK_URL:
    bot.remove_webhook()
    ok = bot.set_webhook(url=WEBHOOK_URL)
    if not ok:
        print("Attenzione: set_webhook ha restituito False")
else:
    print("WEBHOOK_URL non impostata: il bot non riceverà aggiornamenti (solo per sviluppo locale)")
