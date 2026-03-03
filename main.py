import telebot
import google.generativeai as genai

# သင့်ရဲ့ Key များ
TELEGRAM_TOKEN = '8727032305:AAHhjlbareNK2-v6vt2l_gf-0rKKwupIrvg'
GEMINI_API_KEY = 'AIzaSyAaGm0Fd8KFTUi3gmPDSSXZLgAtqNo8I5U'

# Gemini Setup - နာမည်နဲ့ Personality သတ်မှတ်ခြင်း
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="မင်းရဲ့နာမည်က 'Memories AI' ဖြစ်ပါတယ်။ မင်းက ဖော်ရွေပျူငှာပြီး အမှတ်တရတွေကို တန်ဖိုးထားတဲ့ လူသားဆန်တဲ့ AI တစ်ခုဖြစ်ပါတယ်။ မြန်မာလိုပဲ အဓိက ပြန်ဖြေပေးပါ။"
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "မင်္ဂလာပါ! ကျွန်တော်က **Memories AI** ပါ။ ✨\n"
        "သင်နဲ့အတူ အမှတ်တရကောင်းတွေ ဖန်တီးဖို့ အမြဲအသင့်ရှိနေပါတယ်။\n"
        "ဘာများ ကူညီပေးရမလဲခင်ဗျာ?"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def chat_with_memories_ai(message):
    try:
        # AI ဆီက အဖြေတောင်းခြင်း
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "ခဏလေးနော်... Memories AI မှာ အခက်အခဲလေး ဖြစ်သွားလို့ပါ။")

print("Memories AI is now running...")
bot.infinity_polling()
