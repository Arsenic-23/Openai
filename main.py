import telebot
import config
from flask import Flask, request

# Initialize bot
bot = telebot.TeleBot(config.BOT_TOKEN)
app = Flask(__name__)

# Webhook route
@app.route('/' + config.BOT_TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Root route to set webhook
@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=config.WEBHOOK_URL + config.BOT_TOKEN)
    return "Bot Webhook Set", 200

# Command: /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am your AI-powered bot. How can I help you?")

# Command: /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "You can ask me anything!")

# Default message handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "I'm here to assist you!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)