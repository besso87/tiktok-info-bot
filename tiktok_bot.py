# ملف: tiktok_bot.py
# بوت تيك توك - نسخة متكاملة مع خادم الويب

import telebot
import os
import threading
import time
import random
from datetime import datetime
from flask import Flask
from telebot import types

# ========== التوكن من متغيرات البيئة ==========
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    raise Exception("❌ خطأ: لم يتم تعيين التوكن في متغيرات البيئة!")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ========== متغير للتحكم بتشغيل البوت ==========
bot_thread = None
bot_running = False

# ========== دوال مساعدة ==========

def format_number(num):
    """تنسيق الأرقام"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(num)

def get_flag(country_code):
    """تحويل رمز الدولة إلى علم"""
    flags = {
        'SA': '🇸🇦', 'AE': '🇦🇪', 'EG': '🇪🇬', 
        'KW': '🇰🇼', 'QA': '🇶🇦', 'BH': '🇧🇭',
        'US': '🇺🇸', 'GB': '🇬🇧', 'TR': '🇹🇷'
    }
    return flags.get(country_code.upper(), '🌍')

# ========== قائمة الأزرار ==========

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("📊 معلومات أساسية", callback_data="basic"),
        types.InlineKeyboardButton("📈 إحصائيات متقدمة", callback_data="advanced"),
        types.InlineKeyboardButton("🔥 فيديوهات رائجة", callback_data="viral"),
        types.InlineKeyboardButton("💰 تحليل الأرباح", callback_data="earnings"),
        types.InlineKeyboardButton("👥 تحليل الجمهور", callback_data="audience"),
        types.InlineKeyboardButton("🏆 الإنجازات", callback_data="achievements"),
    ]
    markup.add(*buttons)
    return markup

# ========== بيانات وهمية ==========

def get_sample_user_data(username):
    """بيانات وهمية للتجربة"""
    
    # بيانات افتراضية
    return {
        'nickname': f'مستخدم {username}',
        'bio': '✨ هذا حساب على تيك توك',
        'followers': random.randint(1000, 50000),
        'following': random.randint(100, 2000),
        'likes': random.randint(10000, 500000),
        'videos': random.randint(50, 500),
        'verified': random.choice([True, False]),
        'private': random.choice([True, False]),
        'country': random.choice(['SA', 'AE', 'EG', 'US']),
        'created': f"202{random.randint(1,3)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
        'engagement': round(random.uniform(3, 15), 1)
    }

# ========== دوال عرض المعلومات ==========

def format_basic_info(username, data):
    flag = get_flag(data['country'])
    verified_icon = "✅" if data['verified'] else "❌"
    private_icon = "🔒" if data['private'] else "🔓"
    
    info = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     📱 **معلومات الحساب**     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👤 **@{username}**
📝 {data['nickname']}
{flag} {data['country']}

📋 **السيرة:**
{data['bio']}

📊 **الإحصائيات:**
├─ 👥 المتابعون: `{data['followers']:,}`
├─ 👣 يتابع: `{data['following']:,}`
├─ ❤️ الإعجابات: `{data['likes']:,}`
├─ 🎥 المقاطع: `{data['videos']}`
└─ ⭐ التفاعل: {data['engagement']}%

🔒 **الخصوصية:**
├─ موثق: {verified_icon}
├─ خاص: {private_icon}
└─ تاريخ الإنشاء: {data['created']}
    """
    return info

# ========== معالجات البوت ==========

@bot.message_handler(commands=['start'])
def start_command(message):
    welcome = f"""
🌟 **بوت تيك توك المتقدم** 🌟

مرحباً {message.from_user.first_name}! 👋

📱 **أرسل اسم المستخدم:** @username
    """
    bot.send_message(message.chat.id, welcome, parse_mode="Markdown", reply_markup=main_menu())

@bot.message_handler(commands=['test'])
def test_command(message):
    """أمر اختبار للتأكد من أن البوت يرسل رسائل"""
    bot.reply_to(message, "✅ البوت يعمل بشكل طبيعي!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """معالج جميع الرسائل"""
    
    username = message.text.strip().replace('@', '')
    
    # تجاهل الأوامر
    if username.startswith('/'):
        return
    
    try:
        # رسالة انتظار
        waiting = bot.reply_to(message, "🔍 جاري البحث...")
        
        # بيانات وهمية
        user_data = get_sample_user_data(username)
        
        # عرض المعلومات
        info = format_basic_info(username, user_data)
        
        # تعديل رسالة الانتظار
        bot.edit_message_text(
            info,
            waiting.chat.id,
            waiting.message_id,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        
        # تسجيل النجاح
        print(f"✅ تم عرض معلومات {username}")
        
    except Exception as e:
        error_msg = f"❌ خطأ: {str(e)}"
        bot.reply_to(message, error_msg)
        print(f"❌ خطأ مع {username}: {str(e)}")

# ========== مسار اختبار Flask ==========

@app.route('/')
def home():
    return "🤖 بوت تيك توك شغال!", 200

@app.route('/health')
def health():
    return "OK", 200

@app.route('/status')
def status():
    return {
        "status": "running",
        "bot": "active",
        "bot_thread": bot_thread.is_alive() if bot_thread else False,
        "time": datetime.now().isoformat()
    }, 200

# ========== دالة تشغيل البوت في خلفية ==========

def run_bot():
    """تشغيل البوت مع معالجة الأخطاء"""
    global bot_running
    bot_running = True
    
    print("🚀 بدء تشغيل البوت...")
    print(f"📍 @tiktokallinfo_bot")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    while bot_running:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"⚠️ خطأ في البوت: {str(e)}")
            print("♻️ إعادة التشغيل بعد 5 ثواني...")
            time.sleep(5)

# ========== بدء التشغيل ==========

if __name__ == "__main__":
    # تشغيل البوت في خيط منفصل
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # تشغيل خادم Flask (هذا ما يستخدمه Gunicorn)
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
