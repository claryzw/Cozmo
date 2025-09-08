# Chatbot with Python by Clarence Itai Msindo
import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramChatbot:
    def __init__(self):
        # Use environment variable for security
        self.bot_token = os.getenv('BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("BOT_TOKEN environment variable not set")
        
        self.updater = Updater(token=self.bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.user_state = {}  # Track conversation state per user
        
        self._register_handlers()
    
    def _register_handlers(self):
        """Register command and message handlers"""
        self.dispatcher.add_handler(CommandHandler('start', self.handle_start))
        self.dispatcher.add_handler(MessageHandler(
            Filters.text & (~Filters.command), 
            self.handle_message
        ))
    
    def handle_start(self, update, context):
        """Handle /start command"""
        user_id = update.effective_user.id
        self.user_state[user_id] = {'stage': 'greeting'}
        
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hey! What's up? Say 'Hi' or 'Hello' to get started!"
        )
    
    def handle_message(self, update, context):
        """Process user messages based on conversation stage"""
        user_id = update.effective_user.id
        user_message = update.message.text.lower().strip()
        
        # Initialize user state if not exists
        if user_id not in self.user_state:
            self.user_state[user_id] = {'stage': 'greeting'}
        
        current_stage = self.user_state[user_id]['stage']
        response = self._generate_response(user_message, current_stage, user_id)
        
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response
        )
    
    def _generate_response(self, message, stage, user_id):
        """Generate appropriate response based on conversation stage"""
        responses = {
            'greeting': self._handle_greeting,
            'wellbeing': self._handle_wellbeing,
            'name_request': self._handle_name_request,
            'farewell': self._handle_farewell
        }
        
        handler = responses.get(stage, self._handle_unknown)
        return handler(message, user_id)
    
    def _handle_greeting(self, message, user_id):
        """Handle initial greeting messages"""
        greeting_keywords = ['hello', 'hi', 'hey', 'howdy']
        
        if any(keyword in message for keyword in greeting_keywords):
            self.user_state[user_id]['stage'] = 'wellbeing'
            return "How are you doing?"
        
        return "Hello there! Say 'hi' to start our conversation."
    
    def _handle_wellbeing(self, message, user_id):
        """Handle wellbeing check responses"""
        positive_responses = [
            "i'm good", "i am good", "good thanks", 
            "fine", "great", "excellent", "doing well"
        ]
        
        if any(response in message for response in positive_responses):
            self.user_state[user_id]['stage'] = 'name_request'
            return "I'm doing well, thanks for asking! What's your name?"
        
        return "That's nice to hear! What's your name?"
    
    def _handle_name_request(self, message, user_id):
        """Extract and respond to user's name"""
        if "my name is" in message:
            # Extract name after "my name is"
            name_parts = message.split("my name is")
            if len(name_parts) > 1:
                extracted_name = name_parts[1].strip().title()
                self.user_state[user_id].update({
                    'stage': 'farewell',
                    'name': extracted_name
                })
                return (f"Nice to meet you, {extracted_name}! "
                       f"Thanks for chatting. Say 'bye' when you're ready to go.")
        
        return "Please tell me your name by saying 'My name is [your name]'"
    
    def _handle_farewell(self, message, user_id):
        """Handle goodbye messages"""
        farewell_keywords = ['bye', 'goodbye', 'see you', 'farewell']
        
        if any(keyword in message for keyword in farewell_keywords):
            # Clean up user state
            user_name = self.user_state[user_id].get('name', 'friend')
            del self.user_state[user_id]
            return f"Goodbye, {user_name}! Have a wonderful day! 👋"
        
        return "Say 'bye' when you're ready to end our chat!"
    
    def _handle_unknown(self, message, user_id):
        """Handle unrecognized messages"""
        return "I didn't quite understand that. Could you try rephrasing?"
    
    def start_bot(self):
        """Start the bot and begin polling"""
        try:
            logger.info("Starting Telegram bot...")
            self.updater.start_polling()
            self.updater.idle()
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise

def main():
    """Main entry point"""
    try:
        chatbot = TelegramChatbot()
        chatbot.start_bot()
    except Exception as e:
        logger.error(f"Failed to start chatbot: {e}")
        return 1
    return 0

if __name__ == '__main__':
    exit(main())


