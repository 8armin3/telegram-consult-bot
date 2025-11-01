from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8556495652:AAFWKmjfCtZVbXyDCW_5dLJ8nFeXUBDjEZU"
CHANNEL_LINK = "https://t.me/easyknkr"
ADMIN_CHAT_ID = 0  # اگه می‌خوای سوالا برای ادمین برن، آیدیتو بزار

# --- دکمه‌های اصلی ---
main_keyboard = ReplyKeyboardMarkup(
    [["❓ سوال دارم", "📢 لینک کانال مشاوره"]],
    resize_keyboard=True
)

# --- دستور /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋 به بات چت ناشناس مجموعه ایزی کنکور خوش اومدی.\nلطفا یکی از گزینه‌ها رو انتخاب کن:",
        reply_markup=main_keyboard
    )

# --- هندلر پیام‌ها ---
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
        await
 update.message.reply_text("سوالتون با موفقیت ارسال شد✨", reply_markup=main_keyboard)

        if ADMIN_CHAT_ID:
            user = update.effective_user
            msg = f"📩 سوال جدید از @{user.username or user.first_name}:\n\n{question}"
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)

    else:
        await update.message.reply_text("از منوی پایین یکی از گزینه‌ها رو انتخاب کن 👇", reply_markup=main_keyboard)


# --- تابع اصلی ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    print("🤖 Bot is running...")
    app.run_polling()


# --- اجرای برنامه ---
if name == "main":
    main()
