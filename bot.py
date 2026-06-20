import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("TOKEN")

user_games = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    number = random.randint(1, 20)
    user_games[user_id] = number
    keyboard = [[InlineKeyboardButton("🔄 بازی جدید", callback_data='new_game')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"🎲 به بازی حدس عدد خوش اومدی!\nعدد بین 1 تا 20 رو حدس بزن.",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    if not text.isdigit():
        await update.message.reply_text("❌ فقط عدد بفرست!")
        return
    guess = int(text)
    if user_id not in user_games:
        await update.message.reply_text("⚠️ /start رو بزن.")
        return
    secret = user_games[user_id]
    if guess < secret:
        await update.message.reply_text("📈 برو بالاتر!")
    elif guess > secret:
        await update.message.reply_text("📉 برو پایین‌تر!")
    else:
        keyboard = [[InlineKeyboardButton("🎮 بازی جدید", callback_data='new_game')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"🎉 آفرین! عدد {secret} بود.", reply_markup=reply_markup)
        del user_games[user_id]

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'new_game':
        user_id = query.from_user.id
        user_games[user_id] = random.randint(1, 20)
        await query.edit_message_text("🔄 بازی جدید شروع شد! عددتو بفرست.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start : شروع بازی\nعدد 1 تا 20 رو بفرست")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
