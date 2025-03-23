import telebot
import openai
import config
import re

# Initialize bot
bot = telebot.TeleBot(config.BOT_TOKEN)
openai.api_key = config.OPENAI_API_KEY

# Dictionary to track user warnings
warnings = {}

# List of abusive words (you can expand this)
abusive_words = ["abuse1", "abuse2", "fight", "insult"]  # Add more words

# Function to detect abusive language
def contains_abuse(text):
    return any(re.search(rf"\b{word}\b", text, re.IGNORECASE) for word in abusive_words)

# Function to handle messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        
        # Check for abuse
        if contains_abuse(text):
            if user_id not in warnings:
                warnings[user_id] = 1
            else:
                warnings[user_id] += 1
            
            bot.reply_to(message, f"⚠️ Warning {warnings[user_id]}: Please avoid abusive language.")
            
            # Kick user if they exceed 3 warnings (modify if needed)
            if warnings[user_id] >= 3:
                bot.kick_chat_member(chat_id, user_id)
                bot.send_message(chat_id, f"🚨 User {message.from_user.first_name} was removed due to repeated violations.")
            return
        
        # Process normal messages using OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        reply_text = response["choices"][0]["message"]["content"]
        
        bot.send_message(chat_id, reply_text)
    
    except Exception as e:
        bot.send_message(chat_id, "Error: " + str(e))

# Start polling
print("Bot is running...")
bot.polling()