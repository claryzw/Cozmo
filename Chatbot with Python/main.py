# Chatbot with Python by Clarence Itai Msindo
import os
import telebot
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bot import main

BOT_TOKEN = os.environ.get('5940769441:AAEgwz-cZ48FNq_LXU8O0kTXx7Sp5vyS0p8')

bot = telebot.TeleBot(BOT_TOKEN)

# The Chatbot with Python begins here:
# The command handler
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hey! Whats Up? Say 'Hi' or 'Hello'")

# The message handler
def chatbot_functions(update, context):
    message = update.message.text.lower()
    response = ""

    if "hello" in message or "hi" in message:
        response = "How are you doing?"
    elif "i'm good" in message or "i am good" in message or "good thanks and you?" in message or "i'm good thanks and you?" in message:
        response = "I'm doing well, thank's for asking :)! What is your name?"
    elif "my name is" in message:
        name = message.split("my name is")[1].strip()
        response = f"Nice to meet you, {name}! Ok, I'm done talking now. Say 'Bye' to exit this chat. Have a nice day :)!"
    elif "bye" in message:
        response = "Peace out!"
        context.bot.send_message(chat_id=update.message.chat_id, text=response)
        context.bot.leave_chat(chat_id=update.message.chat_id)
    else:
        response = "Nah, I don't understand what you're saying. Try something else."

    context.bot.send_message(chat_id=update.message.chat_id, text=response)


# The updater and dispatcher
updater = Updater(token='5940769441:AAEgwz-cZ48FNq_LXU8O0kTXx7Sp5vyS0p8', use_context=True)
dispatcher = updater.dispatcher

# Add handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), chatbot_functions))


# Starting the bot
updater.start_polling()
updater.idle()