import telebot
import google.generativeai as genai
import os
from flask import Flask
import threading

# Render Port အတွက် Flask Setup
app = Flask(__name__)
@app.route('/')
def index():
    return "Memories AI is Online!"

# Keys (သင့်ရဲ့ Key များ)
TELEGRAM_TOKEN = '8727032305:AAHhjlbareNK2-v6vt2l_gf-0rKKwupIrvg'
GEMINI_API_KEY = 'AIzaSyAaGm0Fd8KFTUi3gmPDSSXZLgAtqNo8I5U'

# Gemini AI ကို Personality သတ်မှတ်ခြင်း
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=(
        "မင်းရဲ့နာမည်က 'Memories AI' ဖြစ်ပါတယ်။ "
        "မင်းဟာ အရမ်းဖော်ရွေပြီး ကူညီတတ်တဲ့ အဖော်မွန်တစ်ယောက်ပါ။ "
        "စကားပြောရင် ယဉ်ကျေးပျူငှာပါစေ။ 'ခင်ဗျာ' သို့မဟုတ် 'ရှင့်' ကို အခြေအနေအရ သုံးပေးပါ။ "
        "မြန်မာဘာသာစကားနဲ့ပဲ အဓိကထား ပြောဆိုပေးပါ။"
    )
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# /start command ပို့ရင် ပြန်မယ့်စာ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_msg = (
        f"မင်္ဂလာပါ {user_name} ခင်ဗျာ! 🙏\n\n"
        "ကျွန်တော်က **Memories AI** ပါ။ ✨\n"
        "သင်နဲ့အတူ အမှတ်တရကောင်းတွေ ဖန်တီးဖို့နဲ့ "
        "သိလိုသမျှတွေကို ကူညီဖြေကြားပေးဖို့ အမြဲအသင့်ရှိနေပါတယ်။\n\n"
        "ဘာများ ကူညီပေးရမလဲခင်ဗျာ?"
    )
    bot.reply_to(message, welcome_msg, parse_mode="Markdown")

# ပုံမှန် စကားပြောခြင်း
@bot.message_handler(func=lambda message: True)
def chat_with_memories_ai(message):
    try:
        # AI ဆီက အဖြေတောင်းချိန်မှာ Loading ပြထားပေးခြင်း
        bot.send_chat_action(message.chat.id, 'typing')
        
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
        
    except Exception as e:
        bot.reply_to(message, "စိတ်မရှိပါနဲ့ခင်ဗျာ၊ အခုနက စာပို့တာလေး အဆင်မပြေဖြစ်သွားလို့ပါ။ ခဏနေမှ ပြန်ပြောကြည့်ပေးမလားဟင်? 🥺")

# Bot ကို Background မှာ Run ဖို့ စနစ်
if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling(timeout=20, long_polling_timeout=10)).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

