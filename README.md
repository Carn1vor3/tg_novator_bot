# 🏘️ Telegram Bot for Residential Complex Listings (Irpin, Ukraine)

This Telegram bot provides quick access to up-to-date apartment prices in various residential complexes (ЖК) located in Irpin, Ukraine. Users can interact with an inline menu to get pricing information with a single tap.

## 🚀 Features

- Interactive inline keyboard
- Instant pricing updates for apartaments and houses in Kyiv region
- Clean and simple UI experience in Telegram

## 🛠️ Technologies Used

- **Python 3.10+**
- **[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v20+**
- **asyncio** for asynchronous execution

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd tg_novator_bot
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

    pip install -r requirements.txt

    BOT_TOKEN=your_telegram_bot_token_here

    python main.py

## 🚀 Deployment
- You can deploy this bot using one of the following platforms:

- **Render**
- **Railway**
- **Fly.io**
- **Heroku (if using webhook mode)**

- Make sure to configure your BOT_TOKEN as an environment variable on the platform of your choice.
