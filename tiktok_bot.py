# ملف: tiktok_bot.py
# بوت تيك توك المتقدم - نسخة آمنة

import telebot
import os
import threading
import time
import random
from datetime import datetime
from flask import Flask
from telebot import types

# ========== التوكن من متغيرات البيئة (آمن) ==========
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    # للاختبار المحلي - ضع التوكن هنا مؤقتاً
    # TOKEN = '8574836303:AAGtE8j5u0V1UIl5_StcNCU54ZQD4wfzP90'
    raise Exception("❌ خطأ: لم يتم تعيين التوكن في متغيرات البيئة!")

bot = telebot.TeleBot(TOKEN)

# ========== خادم ويب صغير لـ Koyeb (للفحص الصحي) ==========
app = Flask(__name__)

@app.route('/')
def index():
    return "✅ بوت تيك توك شغال!", 200

@app.route('/health')
def health():
    return "OK", 200

@app.route('/status')
def status():
    return {
        "status": "running",
        "bot": "active",
        "time": datetime.now().isoformat()
    }, 200

def run_web():
    """تشغيل خادم الويب في خلفية"""
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# ========== دوال مساعدة ==========

def format_number(num):
    """تنسيق الأرقام (مثال: 15000 -> 15k)"""
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
        'OM': '🇴🇲', 'YE': '🇾🇪', 'IQ': '🇮🇶',
        'SY': '🇸🇾', 'JO': '🇯🇴', 'LB': '🇱🇧',
        'PS': '🇵🇸', 'US': '🇺🇸', 'GB': '🇬🇧',
        'TR': '🇹🇷', 'FR': '🇫🇷', 'DE': '🇩🇪'
    }
    return flags.get(country_code.upper(), '🌍')

# ========== قائمة الأزرار الرئيسية ==========

def main_menu():
    """القائمة الرئيسية للبوت"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        types.InlineKeyboardButton("📊 معلومات أساسية", callback_data="basic"),
        types.InlineKeyboardButton("📈 إحصائيات متقدمة", callback_data="advanced"),
        types.InlineKeyboardButton("🔥 فيديوهات رائجة", callback_data="viral"),
        types.InlineKeyboardButton("💰 تحليل الأرباح", callback_data="earnings"),
        types.InlineKeyboardButton("👥 تحليل الجمهور", callback_data="audience"),
        types.InlineKeyboardButton("🏆 الإنجازات", callback_data="achievements"),
        types.InlineKeyboardButton("🔄 تحديث", callback_data="refresh"),
        types.InlineKeyboardButton("❓ مساعدة", callback_data="help")
    ]
    
    markup.add(*buttons)
    return markup

def back_button():
    """زر العودة للقائمة الرئيسية"""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back"))
    return markup

# ========== بيانات وهمية للتجربة (مؤقتاً) ==========

def get_sample_user_data(username):
    """بيانات وهمية لحين ربط API حقيقي"""
    
    # بيانات عشوائية متنوعة
    users_db = {
        "ioplau1": {
            "nickname": "شوق 🇸🇦",
            "bio": "✨ حساب رسمي | للتعاون: shawq@email.com",
            "followers": 3012,
            "following": 436,
            "likes": 26656,
            "videos": 167,
            "verified": False,
            "private": False,
            "country": "SA",
            "created": "2023-01-19",
            "engagement": 8.5
        },
        "default": {
            "nickname": f"مستخدم {username}",
            "bio": "✨ هذا حساب على تيك توك",
            "followers": random.randint(1000, 50000),
            "following": random.randint(100, 2000),
            "likes": random.randint(10000, 500000),
            "videos": random.randint(50, 500),
            "verified": random.choice([True, False]),
            "private": random.choice([True, False]),
            "country": random.choice(['SA', 'AE', 'EG', 'US', 'GB', 'TR']),
            "created": f"202{random.randint(1,3)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "engagement": round(random.uniform(3, 15), 1)
        }
    }
    
    return users_db.get(username, users_db["default"])

# ========== دوال عرض المعلومات ==========

def format_basic_info(username, data):
    """تنسيق المعلومات الأساسية"""
    
    flag = get_flag(data['country'])
    verified_icon = "✅" if data['verified'] else "❌"
    private_icon = "🔒" if data['private'] else "🔓"
    
    # حساب عمر الحساب
    created_year = int(data['created'].split('-')[0])
    account_age = datetime.now().year - created_year
    
    info = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     📱 **معلومات الحساب**     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👤 **@{username}**
📝 {data['nickname']}
{flag} {data['country']}

📋 **السيرة الذاتية:**
{data['bio']}

📊 **الإحصائيات الأساسية:**
├─ 👥 المتابعون: `{data['followers']:,}` ({format_number(data['followers'])})
├─ 👣 يتابع: `{data['following']:,}`
├─ ❤️ إجمالي الإعجابات: `{data['likes']:,}`
├─ 🎥 إجمالي المقاطع: `{data['videos']}`
└─ ⭐ نسبة التفاعل: {data['engagement']}%

🔒 **الخصوصية والحالة:**
├─ حساب موثق: {verified_icon}
├─ حساب خاص: {private_icon}
├─ تاريخ الإنشاء: {data['created']}
└─ عمر الحساب: {account_age} سنة

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ بيانات تجريبية لحين ربط API حقيقي
    """
    return info

def format_advanced_stats(username, data):
    """تنسيق الإحصائيات المتقدمة"""
    
    # حسابات إضافية
    avg_likes_per_video = data['likes'] // max(data['videos'], 1)
    views_estimate = data['likes'] * 10  # تقديري
    followers_growth = random.randint(50, 500)  # نمو وهمي
    profile_views = data['followers'] * random.randint(2, 5)
    
    info = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    📈 **إحصائيات متقدمة**    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👤 **@{username}**

📊 **تحليلات المحتوى:**
├─ متوسط الإعجابات/مقطع: `{avg_likes_per_video:,}`
├─ إجمالي المشاهدات: `{views_estimate:,}`
├─ مشاهدات اليوم: `{random.randint(1000, 10000):,}`
├─ مشاهدات الأسبوع: `{random.randint(10000, 100000):,}`
└─ مشاهدات الشهر: `{random.randint(50000, 500000):,}`

📈 **مؤشرات النمو:**
├─ نمو يومي: +{followers_growth} متابع
├─ نمو أسبوعي: +{followers_growth * 7} متابع
├─ نمو شهري: +{followers_growth * 30} متابع
├─ مشاهدات الملف الشخصي: `{profile_views:,}`
└─ نسبة المشاهدة: {random.randint(60, 95)}%

📊 **معدلات التفاعل:**
├─ تفاعل يومي: {random.randint(100, 1000)}
├─ متوسط التعليقات: {random.randint(10, 200)}
├─ متوسط المشاركات: {random.randint(5, 100)}
└─ نقاط الشهرة: {random.randint(50, 100)}/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    """
    return info

def format_viral_videos(username, data):
    """تنسيق الفيديوهات الرائجة"""
    
    videos = []
    for i in range(1, 4):
        video = {
            "title": f"فيديو {i}",
            "views": random.randint(10000, 500000),
            "likes": random.randint(1000, 50000),
            "comments": random.randint(100, 5000),
            "date": f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        }
        videos.append(video)
    
    info = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     🔥 **أفضل الفيديوهات**    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👤 **@{username}**

🎥 **أفضل 3 فيديوهات:**
"""
    
    for i, v in enumerate(videos, 1):
        info += f"""
{i}. **فيديو {i}**
   ├─ 👁 مشاهدات: {v['views']:,}
   ├─ ❤️ إعجابات: {v['likes']:,}
   ├─ 💬 تعليقات: {v['comments']:,}
   └─ 📅 تاريخ: {v['date']}
"""
    
    info += f"""
📊 **إحصائيات الفيديوهات:**
├─ إجمالي الفيديوهات: {data['videos']}
├─ فيديوهات رائجة: {random.randint(5, 20)}
├─ نسبة الفيديوهات الرائجة: {random.randint(5, 30)}%
└─ أفضل مشاهدة: {random.randint(100000, 1000000):,}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 آخر فيديو: منذ {random.randint(1, 24)} ساعة
    """
    return info

def format_earnings(username, data):
    """تنسيق تحليل الأرباح (تقديري)"""
    
    followers = data['followers']
    
    # تقديرات الأرباح (على أساس المتابعين)
    video_earnings = followers * random.uniform(0.1, 0.5)
    live_earnings = followers * random.uniform(0.05, 0.2)
    brand_deals = followers * random.uniform(0.2, 1.0)
    total = video_earnings + live_earnings + brand_deals
    
    info = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     💰 **تحليل الأرباح**      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👤 **@{username}**
⚠️ هذه تقديرات تقريبية

💰 **الأرباح الشهرية:**
├─ 📹 أرباح المقاطع: `${video_earnings:.0f}`
├─ 🔴 أرباح البثوث: `${live_earnings:.0f}`
├─ 🤝 صفقات العلامات: `${brand_deals:.0f}`
├─ 🎁 الهدايا: `${random.randint(0, 500)}`
└─ 💵 **الإجمالي: `${total:.0f}`**

📊 **مؤشرات الربحية:**
├─ الربح لكل متابع: `${(total/followers):.2f}`
├─ الربح لكل فيديو: `${(total/data['videos']):.2f}`
├─ تصنيف الربحية: {random.choice(['ممتاز', 'جيد', 'متوسط'])}
└─ إمكانية النمو: {random.randint(70, 100)}%

💡 **نصائح:**
• {random.choice(['زيد المحتوى', 'فعل البثوث', 'تعاون مع علامات'])}
• {random.choice(['حسن التفاعل', 'انشر يومياً', 'استخدم هاشتاقات'])}
    """
    return info

def format_audience(username, data):
    """تنسيق تحليل الجمهور"""
    
    info = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     👥 **تحليل الجمهور**      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👤 **@{username}**

🌍 **أهم الدول:**
├─ 🇸🇦 السعودية: {random.randint(20, 40)}%
├─ 🇪🇬 مصر: {random.randint(15, 30)}%
├─ 🇦🇪 الإمارات: {random.randint(10, 20)}%
├─ 🇺🇸 أمريكا: {random.randint(5, 15)}%
└─ أخرى: {random.randint(10, 25)}%

📊 **الفئات العمرية:**
├─ 13-17 سنة: {random.randint(10, 25)}%
├─ 18-24 سنة: {random.randint(30, 50)}%
├─ 25-34 سنة: {random.randint(20, 35)}%
├─ 35+ سنة: {random.randint(5, 15)}%
└─ الرجال / النساء: {random.randint(40, 60)}% / {random.randint(40, 60)}%

⏰ **أوقات النشاط:**
├─ الصباح (6-12): {random.randint(15, 25)}%
├─ الظهر (12-6): {random.randint(20, 30)}%
├─ المساء (6-12): {random.randint(35, 50)}%
└─ الليل (12-6): {random.randint(5, 15)}%

📱 **الأجهزة:**
├─ أندرويد: {random.randint(60, 80)}%
├─ آيفون: {random.randint(15, 35)}%
└─ أخرى: {random.randint(1, 5)}%
    """
    return info

def format_achievements(username, data):
    """تنسيق الإنجازات"""
    
    info = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     🏆 **الإنجازات**         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👤 **@{username}**

🥇 **إنجازات الحساب:**
├─ ⭐ نقاط الشهرة: {random.randint(5000, 50000)}
├─ 📊 مستوى الحساب: المستوى {random.randint(10, 50)}
├─ 🎯 أيام النشاط: {random.randint(100, 1000)} يوم
└─ 🔥 أقوى سلسلة: {random.randint(10, 100)} يوم

🏅 **الشارات:**
"""
    
    badges = [
        "✨ صانع محتوى نشط",
        "⭐ نجم صاعد",
        "💎 حساب مميز",
        "🎥 منتج محتوى",
        "❤️ محبوب من المتابعين",
        "🔴 بثوث مباشرة"
    ]
    
    selected = random.sample(badges, 3)
    for badge in selected:
        info += f"├─ {badge}\n"
    
    info += f"""
🏆 **أفضل الإنجازات:**
├─ أفضل شهر: {random.choice(['يناير', 'فبراير', 'مارس'])} 2024
├─ أكثر فيديو: {random.randint(100000, 1000000):,} مشاهدة
├─ أفضل تفاعل: {random.randint(10, 30)}%
└─ أعلى مركز: #{random.randint(1, 100)} في {random.choice(['السعودية', 'مصر', 'العالم'])}

📈 **التقدم:**
├─ هذا الشهر: +{random.randint(5, 20)}%
└─ هذا العام: +{random.randint(50, 200)}%
    """
    return info

# ========== معالجات البوت ==========

@bot.message_handler(commands=['start'])
def start_command(message):
    """معالج أمر /start"""
    
    welcome = f"""
🌟 **بوت تيك توك المتقدم** 🌟

مرحباً {message.from_user.first_name}! 👋

📱 **معلومات شاملة عن أي حساب تيك توك:**
• إحصائيات دقيقة ومفصلة
• تحليل متقدم للجمهور
• تقديرات الأرباح
• أفضل الفيديوهات
• والمزيد...

🔍 **للبحث عن مستخدم:**
أرسل معرف المستخدم (مثال: @username أو username)

⚡ **جرب الآن:** أرسل أي اسم مستخدم
    """
    
    bot.send_message(
        message.chat.id, 
        welcome, 
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    """معالج أمر /help"""
    
    help_text = """
❓ **مساعدة البوت**

📝 **الأوامر المتاحة:**
• /start - بدء البوت
• /help - عرض المساعدة
• /about - معلومات عن البوت

🔍 **للبحث عن مستخدم:**
أرسل اسم المستخدم (مثال: ioplau1)

📊 **الأزرار التفاعلية:**
• معلومات أساسية
• إحصائيات متقدمة
• فيديوهات رائجة
• تحليل الأرباح
• تحليل الجمهور
• الإنجازات

⚠️ **ملاحظة:** هذه نسخة تجريبية ببيانات وهمية
    """
    
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['about'])
def about_command(message):
    """معالج أمر /about"""
    
    about_text = """
ℹ️ **عن البوت**

🤖 **الإصدار:** 1.0.0 (تجريبي)
📅 **تاريخ الإصدار:** 2024
👨‍💻 **المطور:** @YourUsername

✨ **المميزات القادمة:**
• ربط API حقيقي
• 75+ معلومة عن كل حساب
• رسوم بيانية تفاعلية
• تصدير البيانات
• تنبيهات النمو

📢 **للاستفسارات:** @SupportBot
    """
    
    bot.reply_to(message, about_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """معالج الرسائل النصية (للبحث عن مستخدم)"""
    
    username = message.text.strip().replace('@', '')
    
    # منع الأوامر الخاطئة
    if username.startswith('/'):
        return
    
    # إرسال رسالة "جاري البحث"
    waiting_msg = bot.reply_to(
        message, 
        "🔍 **جاري البحث عن المعلومات...**\n⏳ الرجاء الانتظار", 
        parse_mode="Markdown"
    )
    
    # محاكاة وقت البحث
    time.sleep(1.5)
    
    # جلب البيانات
    user_data = get_sample_user_data(username)
    
    # عرض المعلومات الأساسية
    info = format_basic_info(username, user_data)
    
    bot.edit_message_text(
        info,
        waiting_msg.chat.id,
        waiting_msg.message_id,
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

# ========== معالجات الأزرار ==========

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    """معالج الأزرار التفاعلية"""
    
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    # استخراج اسم المستخدم من الرسالة
    lines = call.message.text.split('\n')
    username = None
    for line in lines:
        if '@' in line and not line.startswith('#'):
            parts = line.split('@')
            if len(parts) > 1:
                username = parts[1].strip()
                break
    
    if not username:
        username = "user"
    
    # معالجة الأزرار
    if call.data == "back":
        # العودة للقائمة الرئيسية
        user_data = get_sample_user_data(username)
        info = format_basic_info(username, user_data)
        bot.edit_message_text(
            info,
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        bot.answer_callback_query(call.id, "🔙 العودة للقائمة")
        
    elif call.data == "basic":
        user_data = get_sample_user_data(username)
        info = format_basic_info(username, user_data)
        bot.edit_message_text(
            info,
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        bot.answer_callback_query(call.id, "📊 معلومات أساسية")
        
    elif call.data == "advanced":
        user_data = get_sample_user_data(username)
        info = format_advanced_stats(username, user_data)
        bot.edit_message_text(
            info,
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        bot.answer_callback_query(call.id, "📈 إحصائيات متقدمة")
        
    elif call.data == "viral":
        user_data = get_sample_user_data(username)
        info = format_viral_videos(username, user_data)
        bot.edit_message_text(
            info,
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        bot.answer_callback_query(call.id, "🔥 فيديوهات رائجة")
        
    elif call.data == "earnings":
        user_data = get_sample_user_data(username)
        info = format_earnings(username, user_data)
        bot.edit_message_text(
            info,
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        bot.answer_callback_query(call.id, "💰 تحليل الأرباح")
        
    elif call.data == "audience":
        user_data = get_sample_user_data(username)
        info = format_audience(username, user_data)
        bot.edit_message_text(
            info,
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        bot.answer_callback_query(call.id, "👥 تحليل الجمهور")
        
    elif call.data == "achievements":
        user_data = get_sample_user_data(username)
        info = format_achievements(username, user_data)
        bot.edit_message_text(
            info,
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        bot.answer_callback_query(call.id, "🏆 الإنجازات")
        
    elif call.data == "refresh":
        user_data = get_sample_user_data(username)
        info = format_basic_info(username, user_data)
        bot.edit_message_text(
            info,
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        bot.answer_callback_query(call.id, "🔄 تم التحديث")
        
    elif call.data == "help":
        help_text = """
❓ **المساعدة السريعة**

📊 **الأزرار المتاحة:**
• 📊 معلومات أساسية - عرض البيانات الرئيسية
• 📈 إحصائيات متقدمة - تحليلات أعمق
• 🔥 فيديوهات رائجة - أفضل الفيديوهات
• 💰 تحليل الأرباح - تقديرات الدخل
• 👥 تحليل الجمهور - ديموغرافيا المتابعين
• 🏆 الإنجازات - جوائز وشارات
• 🔄 تحديث - إعادة تحميل البيانات

⚠️ هذه نسخة تجريبية ببيانات وهمية
        """
        bot.send_message(chat_id, help_text, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "❓ المساعدة")

# ========== تشغيل البوت ==========

def run_bot():
    """تشغيل البوت في خلفية"""
    print("🤖 البوت يعمل...")
    print(f"📍 @tiktokallinfo_bot")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("✅ جاهز لاستقبال الأوامر")
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل خادم الويب والبوت معاً في خيطين منفصلين
    web_thread = threading.Thread(target=run_web)
    bot_thread = threading.Thread(target=run_bot)
    
    web_thread.daemon = True
    bot_thread.daemon = True
    
    web_thread.start()
    bot_thread.start()
    
    # البقاء في انتظار
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف البوت")
