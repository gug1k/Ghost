import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)

BOT_TOKEN = '7668210387:AAF5h_KbdUvTD3VsAfyCVskuyT-hVNqq-O0'  # ← Вставь свой токен
user_templates = {}  # словарь для хранения шаблонов по user_id

def generate_key(template: str):
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{template}-{suffix}"

def generate_keys(amount: int, template: str):
    return '\n'.join(generate_key(template) for _ in range(amount))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_templates:
        user_templates[user_id] = "HIMARS-1D-Gm80A"

    keyboard = [
        [InlineKeyboardButton("100 ключей", callback_data='get100')],
        [InlineKeyboardButton("500 ключей", callback_data='get500')],
        [InlineKeyboardButton("1000 ключей", callback_data='get1000')],
        [InlineKeyboardButton("✏ Изменить шаблон", callback_data='change_template')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Выбери, сколько ключей нужно.\n\nТекущий шаблон: *{user_templates[user_id]}*", parse_mode="Markdown", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if user_id not in user_templates:
        user_templates[user_id] = "HIMARS-1D-Gm80A"

    data = query.data

    if data.startswith('get'):
        amount = int(data.replace('get', ''))
        keys = generate_keys(amount, user_templates[user_id])
        for i in range(0, len(keys), 4000):
            await query.message.reply_text(keys[i:i+4000])
    elif data == 'change_template':
        await query.message.reply_text("Введи новый шаблон (например, `ABC-123-DEF`):")
        context.user_data['awaiting_template'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.user_data.get('awaiting_template'):
        new_template = update.message.text.strip()
        user_templates[user_id] = new_template
        context.user_data['awaiting_template'] = False
        await update.message.reply_text(f"✅ Новый шаблон установлен: *{new_template}*", parse_mode="Markdown")
    else:
        await update.message.reply_text("Нажми /start чтобы начать.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен с возможностью менять шаблон!")
    app.run_polling()
