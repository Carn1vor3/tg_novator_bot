import os
from dotenv import load_dotenv
load_dotenv()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")

# Стартове меню з кнопками
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 Прайси", callback_data='show_prices')],
        [InlineKeyboardButton("ℹ️ Про бота", callback_data='about_bot')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привіт! Обери опцію 👇", reply_markup=reply_markup)


# Команда /prices
async def prices_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ЖК Молодість", callback_data='price_molodist')],
        [InlineKeyboardButton("ЖК Ірпінь Сіті", callback_data='price_irpin_city')],
        [InlineKeyboardButton("ЖК Author", callback_data='price_author')],
        [InlineKeyboardButton("ЖК Сяйво 2", callback_data='price_syayvo2')],
        [InlineKeyboardButton("ЖК Light Residence", callback_data='price_light_residence')],
        [InlineKeyboardButton("ЖК Сенсація", callback_data='price_sensation')],
        [InlineKeyboardButton("ЖК Фаворит Преміум", callback_data='price_favorit_premium')],
        [InlineKeyboardButton("ЖК Utlandia", callback_data='price_utlandia')],

        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main')],

    ]
    await update.message.reply_text("Оберіть об'єкт:", reply_markup=InlineKeyboardMarkup(keyboard))


# Команда /about
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Цей бот створено для агенції 'Новатор' в Ірпені.\n"
        "Тут ви можете переглянути прайси та дізнатися більше про об'єкти.\n\n"
        "📬 З усіх питань щодо роботи бота — звертайтесь до @Carn1vor3"
    )


# Обробка натискань кнопок
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'show_prices':
        keyboard = [
            [InlineKeyboardButton("ЖК Молодість", callback_data='price_molodist')],
            [InlineKeyboardButton("ЖК Ірпінь Сіті", callback_data='price_irpin_city')],
            [InlineKeyboardButton("ЖК Author", callback_data='price_author')],
            [InlineKeyboardButton("ЖК Сяйво 2", callback_data='price_syayvo2')],
            [InlineKeyboardButton("ЖК Light Residence", callback_data='price_light_residence')],
            [InlineKeyboardButton("ЖК Сенсація", callback_data='price_sensation')],
            [InlineKeyboardButton("ЖК Фаворит Преміум", callback_data='price_favorit_premium')],
            [InlineKeyboardButton("ЖК Utlandia", callback_data='price_utlandia')],

            [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main')]
        ]
        await query.edit_message_text("Оберіть об'єкт:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'price_molodist':
        await query.message.reply_text(
            "🏘️ Прайс для ЖК Молодість:\n https://docs.google.com/spreadsheets/d/1GmWJAaf6bXApdf4INsz9NOSCIbLnagux/edit?gid=338716738#gid=338716738"
        )

    elif query.data == 'price_irpin_city':
        await query.message.reply_text(
            "🏙️ Прайс для ЖК Ірпінь Сіті:\n https://docs.google.com/spreadsheets/d/1GMPSnL5pYiohMLD3ko9OQoh-maW1zT9X/edit?gid=1193368506#gid=1193368506"
        )

    elif query.data == 'price_author':
        await query.message.reply_text(
            "🏢 Прайс для ЖК Author:\n https://docs.google.com/spreadsheets/d/1M0mt4_CoEcELlXllYDikmmIiGvYPJa18/edit?gid=1220384877#gid=1220384877"
        )

    elif query.data == 'price_syayvo2':
        await query.message.reply_text(
            "🌟 Прайс для ЖК Сяйво 2:\n https://docs.google.com/spreadsheets/d/11LluIUJa1DcAEA69P3Zbkg0f_Bnjr76UR4xKz3XuEzk/edit?gid=0#gid=0"
        )

    elif query.data == 'price_light_residence':
        await query.message.reply_text(
            "🌞 Прайс для ЖК Light Residence:\n https://docs.google.com/spreadsheets/d/1b1sCujZsQVw1Wy4MAo2ZWBh1RXfHQ3IR_4sEmx7DG6Q/edit?gid=1635684235#gid=1635684235"
        )

    elif query.data == 'price_sensation':
        await query.message.reply_text(
            "💡 Прайс для ЖК Сенсація:\n https://drive.google.com/drive/folders/1CHn3YjkNm323AzO-LzklVsWTNTJkhT_2"
        )

    elif query.data == 'price_favorit_premium':
        await query.message.reply_text(
            "🏘️ Прайс для ЖК Фаворит Преміум:\n https://docs.google.com/spreadsheets/d/1GMPSnL5pYiohMLD3ko9OQoh-maW1zT9X/edit?gid=1313105543#gid=1313105543"
        )

    elif query.data == 'price_utlandia':
        await query.message.reply_text(
            "🏙 Прайс для ЖК Utlandia:\n https://flatris.com.ua/public/chess/?ut=web&cid=d5AO30RbA0GRwJE&"
        )


    elif query.data == 'about_bot':
        await query.edit_message_text(
            "🤖 Цей бот створено для агенції 'Новатор' в Ірпені.\n"
            "Тут ви можете переглянути прайси та дізнатися більше про об'єкти.\n\n"
            "📬 З усіх питань щодо роботи бота, а також пропозицій з покращення його функціонала — звертайтесь до @Carn1vor3"
        )

    elif query.data == 'back_to_main':
        keyboard = [
            [InlineKeyboardButton("📋 Прайси", callback_data='show_prices')],
            [InlineKeyboardButton("ℹ️ Про бота", callback_data='about_bot')]
        ]
        await query.edit_message_text("Повертаємось до головного меню:", reply_markup=InlineKeyboardMarkup(keyboard))


# Меню команд
async def set_bot_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "🔄 Запустити бота / Головне меню"),
        BotCommand("prices", "📋 Прайси по об'єктах"),
        BotCommand("about", "ℹ️ Інформація про бота"),
    ])


# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prices", prices_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CallbackQueryHandler(handle_callback))

    app.post_init = set_bot_commands

    print("Бот запущено...")
    app.run_polling()
