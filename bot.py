from telegram import Update, Poll
from telegram.ext import Updater, CommandHandler, CallbackContext
import random
import os

# 🔧 Вставь сюда свой токен
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN переменная окружения не установлена!")

# Или для отладки:
print(f"Токен (обрезан): {TELEGRAM_BOT_TOKEN[:5]}...")  # не печатай весь токен в лог!

# 📋 Готовые опросы
polls = [
    {
        "question": "Какой язык программирования тебе больше нравится?",
        "options": ["Python", "JavaScript", "C++", "Java"]
    },
    {
        "question": "Какой у тебя уровень в программировании?",
        "options": ["Начинающий", "Средний", "Продвинутый"]
    },
    {
        "question": "Что ты предпочитаешь?",
        "options": ["Frontend", "Backend", "Fullstack"]
    }
]

# 📥 Обработчик команды /start
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    poll = random.choice(polls)
    
    context.bot.send_poll(
        chat_id=chat_id,
        question=poll["question"],
        options=poll["options"],
        is_anonymous=False,
        allows_multiple_answers=False
    )

# 🚀 Основной запуск
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':

    main()

