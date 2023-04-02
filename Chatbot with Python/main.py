# Chatbot with Python by Clarence Itai Msindo
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

# Define a command handler
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hey Whats Up?, I'm Cozmo! How Can I Help?")

# Define a message handler
def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

# Set up the updater and dispatcher
updater = Updater('5940769441:AAEgwz-cZ48FNq_LXU8O0kTXx7Sp5vyS0p8', use_context=True)
dispatcher = updater.dispatcher

# Add handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, echo))

# Start the bot
updater.start_polling()
updater.idle()