# ملف: tiktok_bot.py

import telebot
import os
import threading
from flask import Flask
from telebot import types
import time

# ========== التوكن ==========
# GitHub Secrets: TOKEN
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    TOKEN = '8574836303:AAGtE8j5u0V1UIl5_StcNCU54ZQD4wfzP90'

bot = telebot.TeleBot(TOKEN)

# ========== خادم ويب صغير عشان Koyeb ==========
app = Flask(__name__)

@app.route('/')
def index():
    return "البوت شغال!", 200

@app.route('/health')
def health():
    return "OK", 200

def run_web():
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

# ========== قائمة الأزرار ==========
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📊 معلومات أساسية", callback_data="basic")
    btn2 = types.InlineKeyboardButton("📈 إحصائيات متقدمة", callback_data="advanced")
    btn3 = types.InlineKeyboardButton("🔥 فيديوهات رائجة", callback_data="viral")
    btn4 = types.InlineKeyboardButton("💰 تحليل الأرباح", callback_data="earnings")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

# ========== أمر البدء ==========
@bot.message_handler(commands=['start'])
def start(message):
    welcome = f"""
🌟 **مرحباً بك في بوت تيك توك الشامل** 🌟

مرحباً {message.from_user.first_name}!

🤖 **مميزات البوت:**
• عرض معلومات أي حساب تيك توك
• إحصائيات دقيقة ومفصلة
• معلومات حصرية 75+

📝 **للبحث عن مستخدم:**
أرسل معرف المستخدم (مثال: @username)

🔍 **جرب الآن:** أرسل أي اسم مستخدم
    """
    bot.reply_to(message, welcome, parse_mode="Markdown", reply_markup=main_menu())

# ========== معالجة الرسائل ==========
@bot.message_handler(func=lambda message: True)
def search_user(message):
    username = message.text.strip().replace('@', '')
    
    waiting = bot.reply_to(message, "🔍 **جاري البحث...**", parse_mode="Markdown")
    
    # بيانات وهمية مؤقتاً
    user_info = {
        'username': username,
        'nickname': f'مستخدم {username}',
        'bio': '✨ هذا حساب تجريبي',
        'followers': 15000,
        'following': 850,
        'total_likes': 150000,
        'total_videos': 245,
        'verified': False,
        'private': False,
        'created_date': '2022-06-15',
        'engagement_rate': 7.8,
        'country': '🇸🇦 السعودية'
    }
    
    info = f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃  📱 **معلومات {username}**  ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛

👤 **الاسم:** {user_info['nickname']}
📊 **المتابعين:** {user_info['followers']:,}
❤️ **الإعجابات:** {user_info['total_likes']:,}
🎥 **المقاطع:** {user_info['total_videos']}
⭐ **التفاعل:** {user_info['engagement_rate']}%
🌍 **الدولة:** {user_info['country']}

🔜 قريباً: 75+ معلومة حقيقية
    """
    
    bot.edit_message_text(info, waiting.chat.id, waiting.message_id, 
                         parse_mode="Markdown", reply_markup=main_menu())

# ========== تشغيل البوت ==========
def run_bot():
    print("🤖 البوت يعمل...")
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل الخادم والبوت معاً
    t1 = threading.Thread(target=run_web)
    t2 = threading.Thread(target=run_bot)
    t1.start()
    t2.start()
