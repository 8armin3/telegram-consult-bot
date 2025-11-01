import os
from threading import Thread
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ================= CONFIG =================
TOKEN = "8556495652:AAFWKmjfCtZVbXyDCW_5dLJ8nFeXUBDjEZU"
CHANNEL_LINK = "https://t.me/easyknkr"
ADMIN_CHAT_ID = 0  # اگه می‌خوای سوالا برای ادمین برن، آیدیتو اینجا بذار (مثلاً 123456789)

# ================= WEB SERVER برای Render =================
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot is running successfully!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    thread = Thread(target=run_web)
    thread.daemon = True
    thread.start()

# ================= TELEGRAM BOT =================
main_keyboard = ReplyKeyboardMarkup(
    [["❓ سوال دارم", "📢 لینک کانال مشاوره"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋 به بات چت ناشناس مجموعه ایزی کنکور خوش اومدی.\nلطفا یکی از گزینه‌ها رو انتخاب کن:",
        reply_markup=main_keyboard
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "❓ سوال دارم":
        context.user_data["waiting_for_question"] = True
        await update.message.reply_text("لطفاً سوالت رو بنویس ✍️")

    elif text == "📢 لینک کانال مشاوره":
        await update.message.reply_text(f"📎 لینک کانال مشاوره:\n{CHANNEL_LINK}")

    elif context.user_data.get("waiting_for_question"):
        question = text
        context.user_data["waiting_for_question"] = False
        await update.message.reply_text("سؤالت ارسال شد ✅", reply_markup=main_keyboard)

        if ADMIN_CHAT_ID:
            user = update.effective_user
            msg = f"📩 سوال جدید از @{user.username or user.first_name}:\n\n{question}"
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)

    else:
        await update.message.reply_text(
            "از منوی پایین یکی از گزینه‌ها رو انتخاب کن 👇",
            reply_markup=main_keyboard
        )

# ================= MAIN =================
def main():
    keep_alive()  # نگه داشتن سرور برای Render
    app_tg = ApplicationBuilder().token(TOKEN).build()
    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    print("🤖 Bot is running...")
    app_tg.run_polling()

if __name__ == "__main__":
    main()
