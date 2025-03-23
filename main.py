import telebot
import requests
import config
import re
import json

# Initialize bot
bot = telebot.TeleBot(config.BOT_TOKEN)

# FreeGPT35 API URL
FREE_API_URL = "https://freegpt35.missuo.ru/v1/chat/completions"

# Load warnings from file
def load_warnings():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save warnings to file
def save_warnings():
    with open("data.json", "w") as file:
        json.dump(warnings, file)

warnings = load_warnings()

# List of abusive words
abusive_words = ["abuse1", "abuse2", "fight", "insult"]

# Function to detect abusive language
def contains_abuse(text):
    return any(re.search(rf"\b{word}\b", text, re.IGNORECASE) for word in abusive_words)

# Function to check if the bot is an admin
def is_bot_admin(chat_id):
    try:
        bot_info = bot.get_me()
        admins = bot.get_chat_administrators(chat_id)
        return any(admin.user.id == bot_info.id for admin in admins)
    except Exception:
        return False

# Function to handle messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        
        # Check for abuse
        if contains_abuse(text):
            warnings[user_id] = warnings.get(user_id, 0) + 1
            save_warnings()
            
            bot.reply_to(message, f"⚠️ Warning {warnings[user_id]}: Please avoid abusive language.")
            
            # Kick user if they exceed 3 warnings
            if warnings[user_id] >= 3 and is_bot_admin(chat_id):
                bot.kick_chat_member(chat_id, user_id)
                bot.send_message(chat_id, f"🚨 User {message.from_user.first_name} was removed due to repeated violations.")
            return
        
        # Send request to FreeGPT35 API
        response = requests.post(FREE_API_URL, json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": text}]
        })

        # Extract response text
        reply_text = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Sorry, I couldn't process that.")
        
        bot.send_message(chat_id, reply_text)
    
    except Exception as e:
        bot.send_message(chat_id, "Error: " + str(e))

# Start polling
print("Bot is running...")
bot.polling()