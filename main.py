import telebot
import requests
import config

bot = telebot.TeleBot(config.BOT_TOKEN)

FREE_API_URL = "https://freegpt35.missuo.ru/v1/chat/completions"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        chat_id = message.chat.id
        text = message.text
        
        response = requests.post(FREE_API_URL, json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": text}]
        })
        
        reply_text = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Sorry, I couldn't process that.")
        
        bot.send_message(chat_id, reply_text)

    except Exception as e:
        bot.send_message(chat_id, "Error: " + str(e))

bot.polling()