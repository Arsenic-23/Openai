# Telegram AI Chatbot + Auto Moderator  

This bot works like ChatGPT in private and group chats. It also warns users for abusive language and can kick repeat offenders.  

## 🚀 Features  
- AI-powered responses using OpenAI  
- Detects abusive/fight messages and warns users  
- Kicks users after 3 warnings (if the bot is admin)  
- Runs on Termux  

## 📌 Installation (Termux)  
1. Install Termux from [F-Droid](https://f-droid.org/) (Recommended).  
2. Update and install Python:  
   ```bash
   apt update && apt upgrade -y
   pkg install python -y