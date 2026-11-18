import telebot
import time
import threading
import re

# --- APKA TOKEN AUR DETAILS ---
BOT_TOKEN = "9191525116:AAHUOYwxeCnTI5xnYJLbXCSe2sg6JkHte2w"
ADMIN_ID = 6711101951  # Aapki User ID
STORAGE_CHANNEL_ID = -1003984589774  # Anya back-up channel ID
DELETE_AFTER_SECONDS = 300  # 5 minute baad auto-delete
# ------------------------------

bot = telebot.TeleBot(BOT_TOKEN)

def delete_later(chat_id, message_id):
    time.sleep(DELETE_AFTER_SECONDS)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass

@bot.message_handler(commands=['start'])
def handle_start(message):
    text = message.text.split()
    if len(text) > 1 and text[1].startswith("vid_"):
        msg_id = int(text[1].replace("vid_", ""))
        try:
            # Video bhej raha hai bina restriction ke taaki download/forward ho sake
            sent = bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=STORAGE_CHANNEL_ID,
                message_id=msg_id
            )
            
            # Professional Bilingual Warning Message
            warning_text = (
                "⚠️ **Notice:**\n"
                "Because of copyright issues, this video will be deleted in 5 minutes. "
                "Please forward it somewhere safe or download it for future availability.\n\n"
                "⚠️ **सूचना:**\n"
                "कॉपीराइट समस्या के कारण यह वीडियो 5 मिनट में डिलीट हो जाएगी। "
                "कृपया इसे किसी सुरक्षित जगह पर फॉरवर्ड कर लें या भविष्य के लिए डाउनलोड कर लें।"
            )
            
            warn = bot.send_message(
                message.chat.id,
                warning_text,
                parse_mode="Markdown"
            )
            
            threading.Thread(target=delete_later, args=(message.chat.id, sent.message_id)).start()
            threading.Thread(target=delete_later, args=(message.chat.id, warn.message_id)).start()
        except Exception:
            bot.send_message(message.chat.id, "❌ Video nahi mili ya link expire ho gaya hai.")
    else:
        bot.send_message(message.chat.id, "Welcome! Link ke zariye video access karein.")

@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID)
def handle_admin_link(message):
    match = re.search(r"t\.me/c/\d+/(\d+)", message.text)
    if match:
        msg_id = match.group(1)
        bot_username = bot.get_me().username
        secure_link = f"https://t.me/{bot_username}?start=vid_{msg_id}"
        bot.reply_to(message, f"✅ **Secure Link Tayar Hai:**\n\n`{secure_link}`\n\nIse ShrinkMe par short karke post karein!", parse_mode="Markdown")
    else:
        bot.reply_to(message, "Mujhe apne private channel की post ka link bhejein.")

bot.infinity_polling()
