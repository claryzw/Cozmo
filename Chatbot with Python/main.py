# Chatbot with Python by Clarence Itai Msindo
import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Configure logging for debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SimpleChatbot:
    """A simple conversational Telegram chatbot"""
    
    def __init__(self):
        # Secure token handling with validation
        self.bot_token = os.getenv('BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("BOT_TOKEN environment variable must be set")
        
        # Initialize bot components
        self.updater = Updater(token=self.bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.user_conversations = {}  # Track conversation state per user
        
        # Register handlers
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Register command and message handlers"""
        self.dispatcher.add_handler(CommandHandler('start', self.handle_start))
        self.dispatcher.add_handler(
            MessageHandler(Filters.text & (~Filters.command), self.handle_message)
        )
        
        # Add error handler
        self.dispatcher.add_error_handler(self.handle_error)
    
    def handle_start(self, update, context):
        """Handle the /start command"""
        try:
            user_id = update.effective_user.id
            chat_id = update.effective_chat.id
            
            # Initialize user conversation state
            self.user_conversations[user_id] = {'stage': 'greeting'}
            
            welcome_message = (
                "Hey! What's up? 👋\n"
                "Say 'Hi' or 'Hello' to start chatting!"
            )
            
            context.bot.send_message(chat_id=chat_id, text=welcome_message)
            logger.info(f"Started conversation with user {user_id}")
            
        except Exception as e:
            logger.error(f"Error in start handler: {e}")
    
    def handle_message(self, update, context):
        """Process incoming text messages"""
        try:
            user_id = update.effective_user.id
            chat_id = update.effective_chat.id
            user_message = update.message.text.lower().strip()
            
            # Initialize conversation state if needed
            if user_id not in self.user_conversations:
                self.user_conversations[user_id] = {'stage': 'greeting'}
            
            # Generate appropriate response
            response = self._process_message(user_message, user_id)
            
            # Send response
            context.bot.send_message(chat_id=chat_id, text=response)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, something went wrong. Please try again."
            )
    
    def _process_message(self, message, user_id):
        """Process user message and return appropriate response"""
        current_stage = self.user_conversations[user_id].get('stage', 'greeting')
        
        # Define response handlers for each conversation stage
        response_handlers = {
            'greeting': self._handle_greeting_stage,
            'wellbeing': self._handle_wellbeing_stage,
            'name_collection': self._handle_name_stage,
            'conversation_end': self._handle_end_stage
        }
        
        # Get appropriate handler or default to unknown
        handler = response_handlers.get(current_stage, self._handle_unknown_input)
        return handler(message, user_id)
    
    def _handle_greeting_stage(self, message, user_id):
        """Handle initial greeting messages"""
        greeting_words = ['hello', 'hi', 'hey', 'hiya', 'howdy']
        
        if any(greeting in message for greeting in greeting_words):
            # Move to next conversation stage
            self.user_conversations[user_id]['stage'] = 'wellbeing'
            return "How are you doing? 😊"
        else:
            return "Hello there! Say 'hi' to get our conversation started."
    
    def _handle_wellbeing_stage(self, message, user_id):
        """Handle responses about user's wellbeing"""
        positive_indicators = [
            "i'm good", "i am good", "good thanks", "fine", 
            "great", "excellent", "doing well", "good", "ok"
        ]
        
        if any(indicator in message for indicator in positive_indicators):
            # Move to name collection stage
            self.user_conversations[user_id]['stage'] = 'name_collection'
            return "I'm doing well, thanks for asking! 😄 What's your name?"
        else:
            # Still ask for name regardless of response
            self.user_conversations[user_id]['stage'] = 'name_collection'
            return "Thanks for sharing! What's your name?"
    
    def _handle_name_stage(self, message, user_id):
        """Handle name collection with safe parsing"""
        if "my name is" in message:
            # Safely extract name
            name_parts = message.split("my name is", 1)
            if len(name_parts) > 1 and name_parts[1].strip():
                extracted_name = name_parts[1].strip().title()
                
                # Store name and move to end stage
                self.user_conversations[user_id].update({
                    'stage': 'conversation_end',
                    'name': extracted_name
                })
                
                return (
                    f"Nice to meet you, {extracted_name}! 🎉\n"
                    f"I'm done talking now. Say 'Bye' to exit this chat.\n"
                    f"Have a nice day! 😊"
                )
        
        # If name not provided properly, ask again
        return (
            "Please tell me your name by saying 'My name is [your name]'\n"
            "For example: 'My name is Alex'"
        )
    
    def _handle_end_stage(self, message, user_id):
        """Handle conversation ending"""
        farewell_words = ['bye', 'goodbye', 'see you', 'farewell', 'exit']
        
        if any(farewell in message for farewell in farewell_words):
            # Get user's name if available
            user_name = self.user_conversations[user_id].get('name', 'friend')
            
            # Clean up conversation state
            del self.user_conversations[user_id]
            
            return f"Peace out, {user_name}! 👋 Have an awesome day!"
        else:
            return "Say 'bye' when you're ready to end our chat! 👋"
    
    def _handle_unknown_input(self, message, user_id):
        """Handle unrecognized messages"""
        return (
            "I didn't quite understand that. 🤔\n"
            "Could you try rephrasing or saying 'hi' to restart?"
        )
    
    def handle_error(self, update, context):
        """Handle bot errors gracefully"""
        logger.error(f"Bot error: {context.error}")
        
        if update and update.effective_chat:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Oops! Something went wrong. Please try again."
            )
    
    def start_bot(self):
        """Start the bot and begin polling"""
        try:
            logger.info("🤖 Starting Telegram chatbot...")
            self.updater.start_polling()
            logger.info("✅ Bot is running! Press Ctrl+C to stop.")
            self.updater.idle()
        except KeyboardInterrupt:
            logger.info("🛑 Bot stopped by user")
        except Exception as e:
            logger.error(f"❌ Error starting bot: {e}")
            raise


def main():
    """Main entry point for the chatbot"""
    try:
        # Create and start the chatbot
        chatbot = SimpleChatbot()
        chatbot.start_bot()
        return 0
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print("Please set the BOT_TOKEN environment variable with your bot token")
        return 1
    except Exception as e:
        logger.error(f"Failed to start chatbot: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
