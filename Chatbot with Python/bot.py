# Chatbot with Python by Clarence Itai Msindo
import os
import telebot
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

BOT_TOKEN = os.environ.get('your-bot-token-here')

bot = telebot.TeleBot(BOT_TOKEN)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey! Whats Up? Say 'Hi' or 'Hello'")

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = "Sorry, I didn't understand what you said. Can you please try again?"

    if "hello" in text:
        response = "Hello there! How can I assist you today?"
    elif "help" in text:
        response = "Sure, how can I help you today?"
    elif "bye" in text:
        response = "Goodbye! Have a nice day."

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def main():
   def main():
    # create an instance of the Updater class and pass in your bot token
    updater = Updater('your-bot-token-here', use_context=True)

    # get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # register handlers for commands and messages
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
    dispatcher.add_handler(message_handler)

    # start polling for updates from Telegram
    updater.start_polling()

if __name__ == '__main__':
    main()

