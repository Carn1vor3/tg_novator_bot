import asyncio
import nest_asyncio
import os
import threading
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from fastapi import FastAPI
import uvicorn
import httpx


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# --- Telegram Bot Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 Прайси", callback_data='show_prices')],
        [InlineKeyboardButton("$ Курс валют", callback_data='show_exchange')],
        [InlineKeyboardButton("ℹ️ Про бота", callback_data='about_bot')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привіт! Обери опцію 👇", reply_markup=reply_markup)

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
        [InlineKeyboardButton("ЖК Millenium park", callback_data='price_millenium_park')],
        [InlineKeyboardButton("ЖК Millenium state", callback_data='price_millenium_state')],

        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main')],
    ]
    await update.message.reply_text("Оберіть об'єкт:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_exchange_rates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json")
            data = response.json()

        # Обираємо потрібні валюти
        target_currencies = ['USD', 'EUR', 'PLN']
        text = "💱 *Курс валют НБУ:*\n\n"
        for currency in data:
            if currency['cc'] in target_currencies:
                text += f"*{currency['cc']}* ➤ {currency['rate']} ₴\n"

        await update.callback_query.edit_message_text(text, parse_mode="Markdown")
    except Exception as e:
        await update.callback_query.edit_message_text("Помилка при отриманні курсу валют 😥")
        print(f"[ERROR] Currency API: {e}")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 Цей бот створено для агенції 'Новатор' в Ірпені.\n"
        "Тут ви можете переглянути прайси та дізнатися більше про об'єкти.\n\n"
        "📬 З усіх питань щодо роботи бота, а також пропозицій з покращення його функціонала — звертайтесь до @Carn1vor3"
    )
    await update.message.reply_text(text)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    prices_links = {
        'price_molodist': "🏘️ Прайс для ЖК Молодість:\n https://docs.google.com/spreadsheets/d/1GmWJAaf6bXApdf4INsz9NOSCIbLnagux/edit?gid=338716738#gid=338716738",
        'price_irpin_city': "🏙️ Прайс для ЖК Ірпінь Сіті:\n https://docs.google.com/spreadsheets/d/1GMPSnL5pYiohMLD3ko9OQoh-maW1zT9X/edit?gid=1193368506#gid=1193368506",
        'price_author': "🏢 Прайс для ЖК Author:\n https://docs.google.com/spreadsheets/d/1M0mt4_CoEcELlXllYDikmmIiGvYPJa18/edit?gid=1220384877#gid=1220384877",
        'price_syayvo2': "🌟 Прайс для ЖК Сяйво 2:\n https://docs.google.com/spreadsheets/d/11LluIUJa1DcAEA69P3Zbkg0f_Bnjr76UR4xKz3XuEzk/edit?gid=0#gid=0",
        'price_light_residence': "🌞 Прайс для ЖК Light Residence:\n https://docs.google.com/spreadsheets/d/1b1sCujZsQVw1Wy4MAo2ZWBh1RXfHQ3IR_4sEmx7DG6Q/edit?gid=1635684235#gid=1635684235",
        'price_sensation': "💡 Прайс для ЖК Сенсація:\n https://drive.google.com/drive/folders/1CHn3YjkNm323AzO-LzklVsWTNTJkhT_2",
        'price_favorit_premium': "🏘️ Прайс для ЖК Фаворит Преміум:\n https://docs.google.com/spreadsheets/d/1GMPSnL5pYiohMLD3ko9OQoh-maW1zT9X/edit?gid=1313105543#gid=1313105543",
        'price_utlandia': "🏙 Прайс для ЖК Utlandia:\n https://flatris.com.ua/public/chess/?ut=web&cid=d5AO30RbA0GRwJE&",
        'price_millenium_park': "🏙 Прайс для ЖК Millenium park:\n https://docs.google.com/spreadsheets/d/1tUw14JU8qS4Zzzl6Z-aLZHv_tgcV_dN_/edit?gid=1913165838#gid=1913165838",
        'price_millenium_state': "🏙 Прайс для ЖК Millenium state:\n https://docs.google.com/spreadsheets/d/1tUw14JU8qS4Zzzl6Z-aLZHv_tgcV_dN_/edit?gid=266656817#gid=266656817",

    }

    if query.data == 'show_prices':
        keyboard = [
            [InlineKeyboardButton(text.replace("price_", "").replace("_", " ").title(), callback_data=key)]
            for key, text in prices_links.items()
        ]
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main')])

        keyboard = [
            [InlineKeyboardButton("ЖК Молодість", callback_data='price_molodist')],
            [InlineKeyboardButton("ЖК Ірпінь Сіті", callback_data='price_irpin_city')],
            [InlineKeyboardButton("ЖК Author", callback_data='price_author')],
            [InlineKeyboardButton("ЖК Сяйво 2", callback_data='price_syayvo2')],
            [InlineKeyboardButton("ЖК Light Residence", callback_data='price_light_residence')],
            [InlineKeyboardButton("ЖК Сенсація", callback_data='price_sensation')],
            [InlineKeyboardButton("ЖК Фаворит Преміум", callback_data='price_favorit_premium')],
            [InlineKeyboardButton("ЖК Utlandia", callback_data='price_utlandia')],
            [InlineKeyboardButton("ЖК Millenium park", callback_data='price_millenium_park')],
            [InlineKeyboardButton("ЖК Millenium state", callback_data='price_millenium_state')],

            [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main')],
        ]
        await query.edit_message_text("Оберіть об'єкт:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data in prices_links:
        await query.message.reply_text(prices_links[query.data])

    elif query.data == 'show_exchange':
        await show_exchange_rates(update, context)


    elif query.data == 'about_bot':
        text = (
            "🤖 Цей бот створено для агенції 'Новатор' в Ірпені.\n"
            "Тут ви можете переглянути прайси та дізнатися більше про об'єкти.\n\n"
            "📬 З усіх питань щодо роботи бота, а також пропозицій з покращення його функціонала — звертайтесь до @Carn1vor3"
        )
        await query.edit_message_text(text)

    elif query.data == 'back_to_main':
        keyboard = [
            [InlineKeyboardButton("📋 Прайси", callback_data='show_prices')],
            [InlineKeyboardButton("$ Курс валют", callback_data='show_exchange')],
            [InlineKeyboardButton("ℹ️ Про бота", callback_data='about_bot')]
        ]
        await query.edit_message_text("Повертаємось до головного меню:", reply_markup=InlineKeyboardMarkup(keyboard))


async def set_bot_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "🔄 Запустити бота / Головне меню"),
        BotCommand("prices", "📋 Прайси по об'єктах"),
        BotCommand("about", "ℹ️ Інформація про бота"),
    ])

# --- FastAPI сервер для підтримки роботи на Fly.io ---
app_api = FastAPI()

@app_api.get("/")
def healthcheck():
    return {"status": "OK"}

def run_api():
    uvicorn.run(app_api, host="0.0.0.0", port=8080)

async def keep_awake():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                await client.get("http://localhost:8080")  # або свій повний Fly.io-URL
                print("[KEEP_ALIVE] Ping sent to self.")
        except Exception as e:
            print(f"[KEEP_ALIVE] Error: {e}")
        await asyncio.sleep(240)


nest_asyncio.apply()

# --- Основна точка запуску ---
if __name__ == '__main__':
    threading.Thread(target=run_api, daemon=True).start()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prices", prices_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("Бот запущено...")

    async def main():
        await set_bot_commands(app)
        asyncio.create_task(keep_awake())
        await app.run_polling()

    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()