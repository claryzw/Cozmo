# Chatbot with Python by Clarence Itai Msindo
import os
import logging
import re
from datetime import datetime, timedelta
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TelegramError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramChatbot:
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("BOT_TOKEN environment variable not set")
        
        self.updater = Updater(token=self.bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.user_state = {}
        
        self._register_handlers()
        logger.info("Bot initialized successfully")

    def _register_handlers(self):
        """Register command and message handlers"""
        handlers = [
            CommandHandler('start', self.handle_start),
            CommandHandler('help', self.handle_help),
            MessageHandler(Filters.text & ~Filters.command, self.handle_message)
        ]
        
        for handler in handlers:
            self.dispatcher.add_handler(handler)
        
        self.dispatcher.add_error_handler(self._handle_error)

    # [Keep the rest of your bot.py code as is]
    # ... include all your existing methods

def main():
    """Main entry point"""
    try:
        chatbot = TelegramChatbot()
        chatbot.start_bot()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        return 1
    return 0

if __name__ == '__main__':
    main()


