# Telegram Bot Setup Guide

Complete guide to set up and use the Telegram bot for remote desktop control.

## Overview

The Telegram bot allows you to control your desktop computer remotely through natural language commands sent via Telegram messages (text or voice).

## Features

✅ Text command execution  
✅ Voice message support  
✅ Screenshot capture and sending  
✅ User authentication  
✅ Status monitoring  
✅ LLM-enhanced understanding (optional)  

## Setup Steps

### 1. Create Your Bot

1. Open Telegram on your phone or desktop
2. Search for `@BotFather` (official Telegram bot)
3. Start a chat and send: `/newbot`
4. Follow the prompts:
   - Choose a name for your bot (e.g., "My Desktop Assistant")
   - Choose a username ending in "bot" (e.g., "mydesktop_assistant_bot")
5. You'll receive a token that looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
6. **Save this token securely!**

### 2. Get Your User ID

1. Search for `@userinfobot` on Telegram
2. Start a chat and send: `/start`
3. The bot will reply with your user ID (e.g., `123456789`)
4. **Save this ID** - you'll need it for authorization

### 3. Configure the Agent

#### Option A: Environment Variables (Recommended)

Create a `.env` file in the project directory:

```bash
# Create .env file
cat > .env << EOF
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_AUTHORIZED_USERS=your_user_id_here
EOF
```

Or export in your shell:

```bash
export TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
export TELEGRAM_AUTHORIZED_USERS="123456789"
```

#### Option B: Configuration File

Create `~/.asistent_plant/config.yaml`:

```yaml
telegram:
  token: "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
  authorized_users:
    - 123456789
```

### 4. Start the Bot

```bash
asistent-plant --telegram
```

You should see:
```
Telegram bot initialized successfully
Starting Telegram bot...
```

### 5. Test the Bot

1. Open Telegram and find your bot
2. Send: `/start`
3. You should receive a welcome message
4. Try a command: `take a screenshot`
5. The bot should reply with a screenshot of your desktop

## Usage Examples

### Basic Commands

```
move mouse to center
click on submit button
type hello world
scroll down
open calculator
```

### Screenshot

Send:
```
/screenshot
```

Or:
```
take a screenshot
```

The bot will capture and send you the current screen.

### Voice Commands

1. Record a voice message in Telegram
2. Say your command (e.g., "Open the calculator")
3. Send the voice message to the bot
4. It will convert to text and execute

### Status Check

```
/status
```

Shows if the agent is running and ready.

### Help

```
/help
```

Shows available commands and examples.

## Multi-User Setup

To authorize multiple users:

```bash
export TELEGRAM_AUTHORIZED_USERS="123456789,987654321,555555555"
```

Or in `.env`:
```
TELEGRAM_AUTHORIZED_USERS=123456789,987654321,555555555
```

## LLM Enhancement

### With OpenAI

```bash
export OPENAI_API_KEY="sk-your-key-here"
asistent-plant --telegram --llm openai
```

Benefits:
- Better command understanding
- Context-aware actions
- Complex multi-step workflows

### With Ollama (Local)

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2

# Start bot
asistent-plant --telegram --llm ollama --llm-model llama2
```

## ERP Automation Example

### Scenario

You're away from your desk but need to enter production data in your ERP system.

### Workflow

1. **Send command via Telegram:**
   ```
   Enter today's production: 500 units of Product A in the ERP system
   ```

2. **Agent analyzes (with LLM):**
   - Intent: Data entry
   - Target: ERP system
   - Data: 500 units, Product A

3. **Agent executes:**
   - Captures screen
   - Finds ERP window
   - Navigates to production form
   - Fills in data
   - Saves

4. **Confirmation:**
   ```
   ✅ Successfully entered 500 units of Product A
   📸 [Screenshot of confirmation]
   ```

## Security

### Important Security Considerations

⚠️ **CRITICAL:** Always set `TELEGRAM_AUTHORIZED_USERS`!

Without it, **anyone** can control your desktop through your bot.

### Best Practices

1. **Never share your bot token**
2. **Keep your user ID list updated**
3. **Use strong API keys**
4. **Monitor bot activity**
5. **Run on trusted networks only**
6. **Review commands in logs**

### Recommended Setup

```bash
# .env file (add to .gitignore!)
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_AUTHORIZED_USERS=your_id_only
OPENAI_API_KEY=your_key_here

# File permissions
chmod 600 .env
```

## Running as a Service

### Linux (systemd)

Create `/etc/systemd/system/asistent-plant.service`:

```ini
[Unit]
Description=Asistent Plant Desktop Agent
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/asistent-plant
EnvironmentFile=/path/to/.env
ExecStart=/usr/bin/python -m asistent_plant.main --telegram
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable asistent-plant
sudo systemctl start asistent-plant
```

### macOS (launchd)

Create `~/Library/LaunchAgents/com.asistent-plant.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.asistent-plant</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python</string>
        <string>-m</string>
        <string>asistent_plant.main</string>
        <string>--telegram</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/path/to/asistent-plant</string>
</dict>
</plist>
```

Load:
```bash
launchctl load ~/Library/LaunchAgents/com.asistent-plant.plist
```

## Troubleshooting

### Bot doesn't respond

**Check:**
1. Is the agent running?
2. Is the bot token correct?
3. Is your user ID in the authorized list?
4. Check internet connectivity

**Debug:**
```bash
# Run with verbose output
asistent-plant --telegram
```

### "Unauthorized" message

Your user ID is not in `TELEGRAM_AUTHORIZED_USERS`.

**Fix:**
```bash
# Get your ID from @userinfobot
# Add it to environment
export TELEGRAM_AUTHORIZED_USERS="your_id_here"
# Restart bot
```

### Voice messages not working

**Requirements:**
- `pydub` package
- `ffmpeg` installed
- `speech_recognition` package

**Install:**
```bash
pip install pydub SpeechRecognition
# Ubuntu
sudo apt-get install ffmpeg
# macOS
brew install ffmpeg
```

### Screenshots not sending

**Check:**
1. Screen capture is working
2. Bot has permission to send photos
3. File size is not too large

### Commands fail silently

**Enable debug mode:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Advanced Usage

### Custom Command Handler

```python
from asistent_plant import DesktopAgent
from asistent_plant.modules import TelegramBot

def my_command_handler(command: str) -> dict:
    print(f"Executing: {command}")
    # Custom logic here
    return {"success": True, "message": "Done!"}

# Setup
agent = DesktopAgent()
bot = TelegramBot(token="your_token", authorized_users=[123456789])
bot.set_command_handler(my_command_handler)

# Run
bot.run()
```

### Send Notifications

```python
import asyncio
from asistent_plant.modules import TelegramBot

async def send_alert(user_id: int, message: str):
    bot = TelegramBot(token="your_token")
    await bot.send_message(user_id, message)

# Usage
asyncio.run(send_alert(123456789, "Task completed!"))
```

## FAQ

**Q: Can I use this on multiple computers?**  
A: Yes! Set up the bot on each computer with different bot tokens or use the same token with different authorized users.

**Q: Does the computer need to be unlocked?**  
A: For most operations, yes. Some systems require an active session.

**Q: Can I automate without supervision?**  
A: Yes, but be careful! Test thoroughly and implement error handling.

**Q: What's the latency?**  
A: Typically 1-3 seconds for text commands, 3-5 seconds for voice.

**Q: Can I control multiple desktops?**  
A: Yes! Create a bot for each desktop or use one bot with routing logic.

## Examples

See `asistent_plant/examples/telegram_usage.py` for complete examples.

## Support

- GitHub Issues: https://github.com/alexjhan/asistent-plant/issues
- Documentation: See README.md and USAGE.md

---

Happy automating! 🤖
