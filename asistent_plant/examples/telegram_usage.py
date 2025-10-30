"""
Example: Using Telegram Bot for remote desktop automation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from asistent_plant import DesktopAgent


def setup_telegram_bot():
    """
    Example setup for Telegram bot.
    
    Prerequisites:
    1. Create a bot with @BotFather on Telegram
    2. Get your bot token
    3. Get your Telegram user ID (send a message to @userinfobot)
    4. Set environment variables:
       export TELEGRAM_BOT_TOKEN="your_bot_token_here"
       export TELEGRAM_AUTHORIZED_USERS="123456789,987654321"  # comma-separated user IDs
    """
    
    print("=== Telegram Bot Setup ===\n")
    
    # Check if environment variables are set
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    authorized_users = os.getenv('TELEGRAM_AUTHORIZED_USERS')
    
    if not bot_token:
        print("⚠️  TELEGRAM_BOT_TOKEN not set")
        print("\nTo set up:")
        print("1. Talk to @BotFather on Telegram")
        print("2. Create a new bot with /newbot")
        print("3. Copy the token")
        print("4. Export it: export TELEGRAM_BOT_TOKEN='your_token'")
        print("\nExample:")
        print("  export TELEGRAM_BOT_TOKEN='123456789:ABCdefGHIjklMNOpqrsTUVwxyz'")
        return False
    
    print(f"✓ Bot token configured: {bot_token[:20]}...")
    
    if not authorized_users:
        print("\n⚠️  TELEGRAM_AUTHORIZED_USERS not set")
        print("   This means ANY user can control your desktop!")
        print("\nTo secure your bot:")
        print("1. Send a message to @userinfobot to get your user ID")
        print("2. Export it: export TELEGRAM_AUTHORIZED_USERS='your_user_id'")
        print("\nExample:")
        print("  export TELEGRAM_AUTHORIZED_USERS='123456789'")
        print("\nFor multiple users:")
        print("  export TELEGRAM_AUTHORIZED_USERS='123456789,987654321'")
    else:
        print(f"✓ Authorized users: {authorized_users}")
    
    print("\n" + "="*50)
    return True


def run_telegram_bot_with_llm():
    """
    Example: Run Telegram bot with LLM enhancement.
    """
    print("\n=== Telegram Bot with LLM ===\n")
    
    # Configure with OpenAI
    config = {
        'llm': {
            'provider': 'openai',  # or 'ollama' for local LLM
            'model': 'gpt-3.5-turbo',  # or 'llama2' for Ollama
            'api_key': os.getenv('OPENAI_API_KEY')  # optional, loaded from env
        }
    }
    
    # Initialize agent
    agent = DesktopAgent(config=config)
    
    # Start bot
    print("Starting Telegram bot...")
    print("\nAvailable commands in Telegram:")
    print("  /start - Initialize bot")
    print("  /help - Show help")
    print("  /status - Check agent status")
    print("  /screenshot - Take and send screenshot")
    print("  <any text> - Execute as command")
    print("  <voice message> - Convert to text and execute")
    print("\nPress Ctrl+C to stop")
    
    agent.start_telegram_bot()


def example_command_flow():
    """
    Example: Typical command flow via Telegram.
    """
    print("\n=== Example Command Flow ===\n")
    
    print("1. User sends via Telegram:")
    print("   'Open calculator and type 2+2'")
    print()
    
    print("2. Agent receives command")
    print("   - Authenticates user")
    print("   - Sends 'Processing...' message")
    print()
    
    print("3. LLM analyzes command (if enabled)")
    print("   - Intent: Open calculator application and perform calculation")
    print("   - Actions:")
    print("     a. Open 'calculator' application")
    print("     b. Type '2+2'")
    print("     c. Press 'enter'")
    print()
    
    print("4. Agent executes actions")
    print("   - Vision: Detects calculator window")
    print("   - Control: Opens calculator")
    print("   - Control: Types numbers")
    print("   - Control: Presses enter")
    print()
    
    print("5. Agent sends confirmation to Telegram")
    print("   '✅ Executed: Opened calculator and entered calculation'")
    print()


def example_voice_command():
    """
    Example: Voice command workflow.
    """
    print("\n=== Voice Command Example ===\n")
    
    print("1. User sends voice message to Telegram bot")
    print("   🎤 'Take a screenshot of my desktop'")
    print()
    
    print("2. Bot downloads voice file")
    print("   - Converts OGG to WAV")
    print("   - Uses speech recognition")
    print()
    
    print("3. Bot replies with recognized text")
    print("   '📝 Recognized: Take a screenshot of my desktop'")
    print()
    
    print("4. Agent executes command")
    print("   - Captures screen")
    print("   - Saves to file")
    print()
    
    print("5. Bot sends screenshot to user")
    print("   📸 [Screenshot image]")
    print()


def example_erp_workflow():
    """
    Example: Complete ERP workflow via Telegram.
    """
    print("\n=== ERP Automation via Telegram ===\n")
    
    print("Scenario: Enter production data in ERP system")
    print()
    
    print("1. User sends command:")
    print("   'Enter today's production: 500 units of Product A in the ERP'")
    print()
    
    print("2. LLM analyzes command:")
    print("   - Intent: Data entry in ERP system")
    print("   - Data: 500 units, Product A")
    print("   - Actions needed:")
    print("     a. Activate/open ERP window")
    print("     b. Navigate to production entry form")
    print("     c. Click product field")
    print("     d. Type 'Product A'")
    print("     e. Click quantity field")
    print("     f. Type '500'")
    print("     g. Click save button")
    print()
    
    print("3. Agent captures screen:")
    print("   - Uses OCR to read current screen")
    print("   - Identifies ERP window")
    print("   - Locates input fields")
    print()
    
    print("4. Agent executes automation:")
    print("   ⏳ 'Opening ERP...'")
    print("   ⏳ 'Entering product...'")
    print("   ⏳ 'Entering quantity...'")
    print("   ⏳ 'Saving...'")
    print()
    
    print("5. Agent sends confirmation:")
    print("   '✅ Successfully entered 500 units of Product A'")
    print("   📸 [Screenshot of confirmation]")
    print()


if __name__ == "__main__":
    print("Asistent Plant - Telegram Bot Examples\n")
    print("=" * 60)
    
    # Check setup
    if not setup_telegram_bot():
        print("\n❌ Please configure the bot before continuing")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("\nExample workflows:\n")
    
    # Show examples
    example_command_flow()
    example_voice_command()
    example_erp_workflow()
    
    print("=" * 60)
    print("\nTo start the bot:")
    print("  python -m asistent_plant.main --telegram")
    print("\nWith LLM enhancement:")
    print("  python -m asistent_plant.main --telegram --llm openai")
    print("\nOr run this example:")
    # Uncomment to actually run:
    # run_telegram_bot_with_llm()
