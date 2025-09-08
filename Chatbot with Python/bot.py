# Chatbot with Python by Clarence Itai Msindo
import os
import logging
import re
from datetime import datetime, timedelta
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TelegramError

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramChatbot:
    def __init__(self, cleanup_interval_hours=24):
        # Use environment variable for security
        self.bot_token = os.getenv('BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("BOT_TOKEN environment variable not set")
        
        self.updater = Updater(token=self.bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.user_state = {}  # Track conversation state per user
        self.cleanup_interval = timedelta(hours=cleanup_interval_hours)
        
        # Configuration options
        self.max_name_length = 50
        self.max_message_length = 1000
        
        self._register_handlers()
        logger.info("TelegramChatbot initialized successfully")
    
    def _register_handlers(self):
        """Register command and message handlers with error handling"""
        self.dispatcher.add_handler(CommandHandler('start', self.handle_start))
        self.dispatcher.add_handler(CommandHandler('help', self.handle_help))
        self.dispatcher.add_handler(MessageHandler(
            Filters.text & (~Filters.command), 
            self.handle_message
        ))
        
        # Add error handler for graceful error handling
        self.dispatcher.add_error_handler(self._handle_error)
        logger.info("Handlers registered successfully")
    
    def _handle_error(self, update, context):
        """Handle bot errors gracefully"""
        logger.error(f"Bot error occurred: {context.error}")
        
        if update and update.effective_chat:
            try:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Sorry, something went wrong. Please try again or use /start to restart."
                )
            except TelegramError as e:
                logger.error(f"Failed to send error message: {e}")
    
    def _validate_input(self, update):
        """Validate incoming update for required fields"""
        if not update or not update.message or not update.message.text:
            logger.warning("Invalid update received: missing message or text")
            return False
        
        if len(update.message.text) > self.max_message_length:
            logger.warning(f"Message too long: {len(update.message.text)} chars")
            return False
        
        return True
    
    def _cleanup_old_sessions(self):
        """Remove old user sessions to prevent memory leaks"""
        current_time = datetime.now()
        users_to_remove = []
        
        for user_id, state in self.user_state.items():
            last_activity = state.get('last_activity', current_time)
            if current_time - last_activity > self.cleanup_interval:
                users_to_remove.append(user_id)
        
        for user_id in users_to_remove:
            del self.user_state[user_id]
            logger.info(f"Cleaned up session for user {user_id}")
        
        if users_to_remove:
            logger.info(f"Cleaned up {len(users_to_remove)} old sessions")
    
    def _update_user_activity(self, user_id):
        """Update user's last activity timestamp"""
        if user_id in self.user_state:
            self.user_state[user_id]['last_activity'] = datetime.now()
    
    def handle_start(self, update, context):
        """Handle /start command with validation"""
        try:
            if not self._validate_input(update):
                return
            
            user_id = update.effective_user.id
            user_name = update.effective_user.first_name or "there"
            
            # Initialize user state with timestamp
            self.user_state[user_id] = {
                'stage': 'greeting',
                'last_activity': datetime.now(),
                'start_time': datetime.now()
            }
            
            welcome_message = (
                f"Hey {user_name}! What's up? 👋\n"
                f"Say 'Hi' or 'Hello' to get started!\n"
                f"Type /help for available commands."
            )
            
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=welcome_message
            )
            
            logger.info(f"Started conversation with user {user_id} ({user_name})")
            
        except Exception as e:
            logger.error(f"Error in handle_start: {e}")
            self._handle_error(update, context)
    
    def handle_help(self, update, context):
        """Handle /help command"""
        try:
            help_text = (
                "🤖 Chatbot Commands:\n\n"
                "/start - Start a new conversation\n"
                "/help - Show this help message\n\n"
                "Just say 'hi' to begin chatting!"
            )
            
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=help_text
            )
            
        except Exception as e:
            logger.error(f"Error in handle_help: {e}")
            self._handle_error(update, context)
    
    def handle_message(self, update, context):
        """Process user messages with comprehensive validation"""
        try:
            if not self._validate_input(update):
                return
            
            user_id = update.effective_user.id
            user_message = update.message.text.lower().strip()
            
            # Periodic cleanup of old sessions
            if len(self.user_state) % 100 == 0:  # Every 100 messages
                self._cleanup_old_sessions()
            
            # Initialize user state if not exists
            if user_id not in self.user_state:
                self.user_state[user_id] = {
                    'stage': 'greeting',
                    'last_activity': datetime.now()
                }
            
            # Update activity timestamp
            self._update_user_activity(user_id)
            
            current_stage = self.user_state[user_id]['stage']
            response = self._generate_response(user_message, current_stage, user_id)
            
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=response
            )
            
            logger.debug(f"Processed message from user {user_id} in stage '{current_stage}'")
            
        except Exception as e:
            logger.error(f"Error in handle_message: {e}")
            self._handle_error(update, context)
    
    def _generate_response(self, message, stage, user_id):
        """Generate appropriate response based on conversation stage"""
        response_handlers = {
            'greeting': self._handle_greeting,
            'wellbeing': self._handle_wellbeing,
            'name_request': self._handle_name_request,
            'farewell': self._handle_farewell
        }
        
        handler = response_handlers.get(stage, self._handle_unknown)
        try:
            return handler(message, user_id)
        except Exception as e:
            logger.error(f"Error in response handler for stage '{stage}': {e}")
            return "Sorry, I encountered an error. Please try again or use /start to restart."
    
    def _handle_greeting(self, message, user_id):
        """Handle initial greeting messages with better keyword matching"""
        greeting_patterns = [
            r'\bhi\b', r'\bhello\b', r'\bhey\b', r'\bhowdy\b', 
            r'\bgreetings\b', r'\bhiya\b'
        ]
        
        if any(re.search(pattern, message, re.IGNORECASE) for pattern in greeting_patterns):
            self.user_state[user_id]['stage'] = 'wellbeing'
            return "How are you doing? 😊"
        
        return "Hello there! Say 'hi' to start our conversation."
    
    def _handle_wellbeing(self, message, user_id):
        """Handle wellbeing check responses with emotion detection"""
        positive_patterns = [
            r'\bgood\b', r'\bfine\b', r'\bgreat\b', r'\bexcellent\b',
            r'\bawesome\b', r'\bwonderful\b', r'\bdoing well\b',
            r"i'm good", r"i am good"
        ]
        
        negative_patterns = [
            r'\bbad\b', r'\bterrible\b', r'\bawful\b', r'\bnot good\b',
            r'\bsad\b', r'\bdepressed\b'
        ]
        
        if any(re.search(pattern, message, re.IGNORECASE) for pattern in positive_patterns):
            self.user_state[user_id]['stage'] = 'name_request'
            return "I'm doing well, thanks for asking! 😄 What's your name?"
        elif any(re.search(pattern, message, re.IGNORECASE) for pattern in negative_patterns):
            self.user_state[user_id]['stage'] = 'name_request'
            return "I'm sorry to hear that. I hope things get better! 💙 What's your name?"
        else:
            self.user_state[user_id]['stage'] = 'name_request'
            return "Thanks for sharing! What's your name?"
    
    def _extract_name(self, message):
        """Safely extract name from message with validation"""
        # Pattern to match "my name is [name]"
        name_pattern = r"my name is\s+([a-zA-Z\s]+)"
        match = re.search(name_pattern, message, re.IGNORECASE)
        
        if match:
            extracted_name = match.group(1).strip()
            
            # Validate name length and characters
            if 1 <= len(extracted_name) <= self.max_name_length:
                # Clean and format name
                clean_name = re.sub(r'\s+', ' ', extracted_name)  # Remove extra spaces
                return clean_name.title()
        
        return None
    
    def _handle_name_request(self, message, user_id):
        """Extract and respond to user's name with robust parsing"""
        extracted_name = self._extract_name(message)
        
        if extracted_name:
            self.user_state[user_id].update({
                'stage': 'farewell',
                'name': extracted_name
            })
            return (
                f"Nice to meet you, {extracted_name}! 🎉\n"
                f"Thanks for chatting with me. Say 'bye' when you're ready to go."
            )
        else:
            # Check for simple name patterns (just the name without "my name is")
            simple_name_match = re.match(r'^([a-zA-Z\s]{1,50})$', message.strip())
            if simple_name_match and len(message.strip()) <= 30:
                name = simple_name_match.group(1).strip().title()
                self.user_state[user_id].update({
                    'stage': 'farewell',
                    'name': name
                })
                return (
                    f"Nice to meet you, {name}! 🎉\n"
                    f"Thanks for chatting with me. Say 'bye' when you're ready to go."
                )
        
        return (
            "Please tell me your name by saying 'My name is [your name]'\n"
            "Or just type your name directly. For example: 'Alice' or 'My name is Alice'"
        )
    
    def _handle_farewell(self, message, user_id):
        """Handle goodbye messages with pattern matching"""
        farewell_patterns = [
            r'\bbye\b', r'\bgoodbye\b', r'\bsee you\b', r'\bfarewell\b',
            r'\bciao\b', r'\badios\b', r'\btake care\b'
        ]
        
        if any(re.search(pattern, message, re.IGNORECASE) for pattern in farewell_patterns):
            # Get user's name if available
            user_name = self.user_state[user_id].get('name', 'friend')
            
            # Clean up user state
            del self.user_state[user_id]
            
            return f"Goodbye, {user_name}! Have a wonderful day! 👋✨"
        
        return "Say 'bye' when you're ready to end our chat! 👋"
    
    def _handle_unknown(self, message, user_id):
        """Handle unrecognized messages with helpful suggestions"""
        current_stage = self.user_state[user_id].get('stage', 'greeting')
        
        stage_suggestions = {
            'greeting': "Try saying 'hello' or 'hi' to start!",
            'wellbeing': "Tell me how you're feeling - good, bad, fine, etc.",
            'name_request': "Please share your name with me!",
            'farewell': "Say 'bye' when you want to end our chat."
        }
        
        suggestion = stage_suggestions.get(current_stage, "Try saying 'hi' to restart!")
        
        return f"I didn't quite understand that. 🤔 {suggestion}"
    
    def start_bot(self):
        """Start the bot and begin polling with enhanced error handling"""
        try:
            logger.info("🤖 Starting Telegram bot...")
            self.updater.start_polling()
            logger.info("✅ Bot is running! Press Ctrl+C to stop.")
            self.updater.idle()
        except KeyboardInterrupt:
            logger.info("🛑 Bot stopped by user")
        except Exception as e:
            logger.error(f"❌ Error starting bot: {e}")
            raise
        finally:
            logger.info(f"Bot stopped. Active sessions: {len(self.user_state)}")

def main():
    """Main entry point with better error handling"""
    try:
        chatbot = TelegramChatbot()
        chatbot.start_bot()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print("❌ Please set the BOT_TOKEN environment variable")
        return 1
    except Exception as e:
        logger.error(f"Failed to start chatbot: {e}")
        return 1
    return 0

if __name__ == '__main__':
    exit(main())


