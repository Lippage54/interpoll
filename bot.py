from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import random
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN переменная окружения не установлена!")

polls = [
    {
        "question": "Какой язык программирования тебе больше нравится?",
        "options": ["Python", "JavaScript", "C++", "Java"],
        "correct_option_id": 0  # Python
    },
    {
        "question": "Какой у тебя уровень в программировании?",
        "options": ["Начинающий", "Средний", "Продвинутый"],
        "correct_option_id": 2  # Продвинутый
    },
    {
        "question": "Что ты предпочитаешь?",
        "options": ["Frontend", "Backend", "Fullstack"],
        "correct_option_id": 2  # Fullstack
    }
]

# Хранение состояния пользователя — какой опрос сейчас
user_data = {}

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_data[chat_id] = 0  # первый опрос
    send_poll(update, context, chat_id, 0)

def send_poll(update, context, chat_id, poll_index):
    poll = polls[poll_index]

    keyboard = [
        [InlineKeyboardButton("Следующий вопрос", callback_data="next_poll")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_poll(
        chat_id=chat_id,
        question=poll["question"],
        options=poll["options"],
        is_anonymous=False,
        allows_multiple_answers=False,
        type='quiz',  # обязательно quiz для правильного варианта
        correct_option_id=poll["correct_option_id"],
        reply_markup=reply_markup
    )

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id

    # Обработать нажатие "Следующий вопрос"
    if query.data == "next_poll":
        current = user_data.get(chat_id, 0)
        next_poll = (current + 1) % len(polls)  # по кругу
        user_data[chat_id] = next_poll

        # Удаляем старое сообщение с опросом и кнопкой (чтобы не засорять чат)
        query.message.delete()

        send_poll(update, context, chat_id, next_poll)
    query.answer()

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
