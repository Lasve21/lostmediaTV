import os
import telebot
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# =======================
# Configurazione bot
# =======================
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# =======================
# Serie e episodi
# =======================
SERIE = {
    "Stagione 1": [
        {"titolo": "TUTTI GLI EP.", "link": "https://vidsrc.me/embed/tv?imdb=tt28093628"},
       
    ]
}

# =======================
# Webhook Flask
# =======================
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.stream.read().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def index():
    return "Bot attivo!", 200

# =======================
# Funzione per menu stagioni
# =======================
def menu_stagioni(chat_id):
    markup = InlineKeyboardMarkup()
    for stagione in SERIE.keys():
        markup.add(InlineKeyboardButton(stagione, callback_data=stagione))
    bot.send_message(chat_id, "Scegli la stagione:", reply_markup=markup)

# =======================
# Comando /start
# =======================
@bot.message_handler(commands=["start"])
def start(message):
    menu_stagioni(message.chat.id)

# =======================
# Gestione pulsanti
# =======================
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id

    if call.data == "INDIETRO":  # torna al menu stagioni
        menu_stagioni(chat_id)
        return

    if call.data in SERIE:  # se clicca la stagione
        markup = InlineKeyboardMarkup()
        for ep in SERIE[call.data]:
            markup.add(InlineKeyboardButton(ep["titolo"], url=ep["link"]))
        # aggiungiamo pulsante indietro
        markup.add(InlineKeyboardButton("⬅ Torna indietro", callback_data="INDIETRO"))
        bot.send_message(chat_id, f"Episodi di {call.data}:", reply_markup=markup)

# =======================
# Avvio locale (non usato su Render)
# =======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
