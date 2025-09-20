from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, PollAnswerHandler
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

# user_data хранит для каждого chat_id: current_poll, correct_count, incorrect_count
user_data = {}

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_data[chat_id] = {
        "current_poll": 0,
        "correct_count": 0,
        "incorrect_count": 0
    }
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
        type='quiz',
        correct_option_id=poll["correct_option_id"],
        reply_markup=reply_markup
    )

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id

    if query.data == "next_poll":
        current = user_data.get(chat_id, {}).get("current_poll", 0)
        next_poll = (current + 1) % len(polls)
        user_data[chat_id]["current_poll"] = next_poll

        query.message.delete()

        send_poll(update, context, chat_id, next_poll)
    query.answer()

def receive_poll_answer(update: Update, context: CallbackContext):
    answer = update.poll_answer
    user_id = answer.user.id
    selected_option = answer.option_ids[0]  # так как allows_multiple_answers=False

    # Найдём чат_id, в котором пользователь ответил (в 1-1 чатах user_id == chat_id)
    chat_id = user_id

    # Получаем текущий опрос пользователя
    if chat_id not in user_data:
        return  # Если пользователь не в нашем словаре — игнорируем

    current_poll_index = user_data[chat_id]["current_poll"]
    correct_option = polls[current_poll_index]["correct_option_id"]

    if selected_option == correct_option:
        user_data[chat_id]["correct_count"] += 1
        result_text = "Правильно! ✅"
    else:
        user_data[chat_id]["incorrect_count"] += 1
        result_text = "Неправильно ❌"

    # Отправим сообщение с результатом и статистикой
    context.bot.send_message(
        chat_id=chat_id,
        text=f"{result_text}\n\nСтатистика:\nПравильных ответов: {user_data[chat_id]['correct_count']}\nНеправильных ответов: {user_data[chat_id]['incorrect_count']}"
    )

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(PollAnswerHandler(receive_poll_answer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
