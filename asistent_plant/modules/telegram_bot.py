"""
Telegram Bot Module
Handles Telegram bot integration for remote control
"""

import os
import asyncio
import tempfile
from typing import Optional, Callable, List, Dict
from pathlib import Path


class TelegramBot:
    """
    Telegram bot for remote desktop automation control.
    Supports text and voice commands with authentication.
    """
    
    def __init__(self, token: Optional[str] = None, authorized_users: Optional[List[int]] = None):
        """
        Initialize Telegram bot.
        
        Args:
            token: Telegram bot token
            authorized_users: List of authorized user IDs
        """
        self.token = token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.authorized_users = authorized_users or self._load_authorized_users()
        self.command_handler = None
        self.application = None
        self.is_running = False
        
        if not self.token:
            print("Warning: Telegram bot token not provided. Set TELEGRAM_BOT_TOKEN environment variable.")
            return
        
        try:
            from telegram import Update
            from telegram.ext import (
                Application, 
                CommandHandler, 
                MessageHandler, 
                filters,
                ContextTypes
            )
            
            self.Update = Update
            self.ContextTypes = ContextTypes
            self.filters = filters
            
            # Initialize bot application
            self.application = Application.builder().token(self.token).build()
            
            # Add handlers
            self.application.add_handler(CommandHandler("start", self._start_command))
            self.application.add_handler(CommandHandler("help", self._help_command))
            self.application.add_handler(CommandHandler("status", self._status_command))
            self.application.add_handler(CommandHandler("screenshot", self._screenshot_command))
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_text))
            self.application.add_handler(MessageHandler(filters.VOICE, self._handle_voice))
            
            print("Telegram bot initialized successfully")
            
        except ImportError:
            print("Warning: python-telegram-bot not installed. Install with: pip install python-telegram-bot")
            self.application = None
    
    def _load_authorized_users(self) -> List[int]:
        """Load authorized user IDs from environment or config."""
        users_str = os.getenv('TELEGRAM_AUTHORIZED_USERS', '')
        if users_str:
            try:
                return [int(uid.strip()) for uid in users_str.split(',') if uid.strip()]
            except ValueError:
                print("Warning: Invalid TELEGRAM_AUTHORIZED_USERS format")
        return []
    
    def is_available(self) -> bool:
        """Check if bot is properly configured."""
        return self.application is not None and self.token is not None
    
    def set_command_handler(self, handler: Callable):
        """
        Set the command handler function.
        
        Args:
            handler: Function that takes (command: str) and returns result dict
        """
        self.command_handler = handler
    
    def is_authorized(self, user_id: int) -> bool:
        """
        Check if user is authorized.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if authorized
        """
        # If no authorized users specified, allow all (development mode)
        if not self.authorized_users:
            return True
        return user_id in self.authorized_users
    
    async def _start_command(self, update, context):
        """Handle /start command."""
        user_id = update.effective_user.id
        
        if not self.is_authorized(user_id):
            await update.message.reply_text(
                "⛔ Unauthorized. Your user ID: {}".format(user_id)
            )
            return
        
        welcome_message = """🤖 *Asistent Plant - Desktop Automation Agent*

I can help you automate desktop tasks through natural language commands.

*Commands:*
• Send any text command to execute
• Send voice messages for voice commands
• /help - Show available commands
• /status - Check agent status
• /screenshot - Take a screenshot

*Example commands:*
• "Click on the submit button"
• "Type hello world"
• "Move mouse to center"
• "Open calculator"
• "Scroll down"

Your user ID: {}
""".format(user_id)
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def _help_command(self, update, context):
        """Handle /help command."""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("⛔ Unauthorized")
            return
        
        help_text = """*Available Commands:*

*Basic Actions:*
• Click: "click on [button name]"
• Type: "type [text]"
• Move: "move mouse to [position]"
• Scroll: "scroll [up/down]"
• Wait: "wait [seconds]"

*Application Control:*
• "open [app name]"
• "close window"
• "maximize window"

*Information:*
• /status - Agent status
• /screenshot - Take screenshot

*Voice Commands:*
Send a voice message and I'll convert it to text and execute.

*Multi-step:*
Chain commands with "then":
"click on login then type username then press enter"
"""
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def _status_command(self, update, context):
        """Handle /status command."""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("⛔ Unauthorized")
            return
        
        # Get agent status
        status_message = "🟢 Agent is running and ready"
        
        if self.command_handler:
            # Try to get more detailed status
            try:
                status_message += "\n✓ Command handler: Active"
            except:
                pass
        
        await update.message.reply_text(status_message)
    
    async def _screenshot_command(self, update, context):
        """Handle /screenshot command."""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("⛔ Unauthorized")
            return
        
        await update.message.reply_text("📸 Taking screenshot...")
        
        try:
            # Execute screenshot command
            if self.command_handler:
                result = self.command_handler("take a screenshot")
                
                if result.get('success') and 'filename' in result:
                    # Send the screenshot
                    await update.message.reply_photo(
                        photo=open(result['filename'], 'rb'),
                        caption="Screenshot captured"
                    )
                    
                    # Clean up
                    try:
                        os.remove(result['filename'])
                    except:
                        pass
                else:
                    await update.message.reply_text(f"❌ {result.get('message', 'Screenshot failed')}")
            else:
                await update.message.reply_text("❌ Command handler not configured")
        
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def _handle_text(self, update, context):
        """Handle text messages."""
        user_id = update.effective_user.id
        
        if not self.is_authorized(user_id):
            await update.message.reply_text("⛔ Unauthorized. Contact administrator.")
            return
        
        command = update.message.text
        
        # Send "processing" message
        processing_msg = await update.message.reply_text("⏳ Processing command...")
        
        try:
            if self.command_handler:
                # Execute command
                result = self.command_handler(command)
                
                # Format response
                if result.get('success'):
                    response = f"✅ {result.get('message', 'Command executed')}"
                    
                    # Add additional info if available
                    if 'location' in result and result['location']:
                        response += f"\nLocation: {result['location']}"
                else:
                    response = f"❌ {result.get('message', 'Command failed')}"
                
                await processing_msg.edit_text(response)
            else:
                await processing_msg.edit_text("❌ Command handler not configured")
        
        except Exception as e:
            await processing_msg.edit_text(f"❌ Error: {str(e)}")
    
    async def _handle_voice(self, update, context):
        """Handle voice messages."""
        user_id = update.effective_user.id
        
        if not self.is_authorized(user_id):
            await update.message.reply_text("⛔ Unauthorized")
            return
        
        await update.message.reply_text("🎤 Processing voice message...")
        
        try:
            # Download voice file
            voice_file = await update.message.voice.get_file()
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            await voice_file.download_to_drive(tmp_path)
            
            # Convert voice to text
            text = await self._convert_voice_to_text(tmp_path)
            
            # Clean up
            try:
                os.remove(tmp_path)
            except:
                pass
            
            if text:
                await update.message.reply_text(f"📝 Recognized: _{text}_", parse_mode='Markdown')
                
                # Execute command
                if self.command_handler:
                    result = self.command_handler(text)
                    
                    if result.get('success'):
                        await update.message.reply_text(f"✅ {result.get('message', 'Command executed')}")
                    else:
                        await update.message.reply_text(f"❌ {result.get('message', 'Command failed')}")
            else:
                await update.message.reply_text("❌ Could not recognize speech")
        
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing voice: {str(e)}")
    
    async def _convert_voice_to_text(self, audio_path: str) -> Optional[str]:
        """
        Convert voice file to text.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Recognized text or None
        """
        try:
            # Convert OGG to WAV
            from pydub import AudioSegment
            import speech_recognition as sr
            
            # Load and convert audio
            audio = AudioSegment.from_ogg(audio_path)
            
            # Export as WAV
            wav_path = audio_path.replace('.ogg', '.wav')
            audio.export(wav_path, format='wav')
            
            # Recognize speech
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
            
            # Clean up
            try:
                os.remove(wav_path)
            except:
                pass
            
            return text
        
        except ImportError:
            print("Warning: pydub or speech_recognition not installed")
            return None
        except Exception as e:
            print(f"Voice recognition error: {e}")
            return None
    
    async def send_message(self, user_id: int, message: str, parse_mode: Optional[str] = None):
        """
        Send a message to a user.
        
        Args:
            user_id: Telegram user ID
            message: Message text
            parse_mode: Optional parse mode ('Markdown' or 'HTML')
        """
        if not self.is_available():
            return
        
        try:
            await self.application.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode=parse_mode
            )
        except Exception as e:
            print(f"Error sending message: {e}")
    
    async def send_photo(self, user_id: int, photo_path: str, caption: Optional[str] = None):
        """
        Send a photo to a user.
        
        Args:
            user_id: Telegram user ID
            photo_path: Path to photo file
            caption: Optional caption
        """
        if not self.is_available():
            return
        
        try:
            await self.application.bot.send_photo(
                chat_id=user_id,
                photo=open(photo_path, 'rb'),
                caption=caption
            )
        except Exception as e:
            print(f"Error sending photo: {e}")
    
    def run(self):
        """Run the bot (blocking)."""
        if not self.is_available():
            print("Cannot run bot: not properly configured")
            return
        
        print("Starting Telegram bot...")
        self.is_running = True
        
        try:
            self.application.run_polling(allowed_updates=self.Update.ALL_TYPES)
        except KeyboardInterrupt:
            print("\nStopping bot...")
        finally:
            self.is_running = False
    
    async def run_async(self):
        """Run the bot asynchronously."""
        if not self.is_available():
            print("Cannot run bot: not properly configured")
            return
        
        print("Starting Telegram bot...")
        self.is_running = True
        
        try:
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling(allowed_updates=self.Update.ALL_TYPES)
            
            # Keep running
            while self.is_running:
                await asyncio.sleep(1)
        
        finally:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            self.is_running = False
    
    def stop(self):
        """Stop the bot."""
        self.is_running = False
        if self.application:
            print("Stopping Telegram bot...")
