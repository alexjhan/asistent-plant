# Asistent Plant - Usage Guide

Complete guide for using the AI-powered desktop automation agent.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Telegram Bot Setup](#telegram-bot-setup)
4. [LLM Integration](#llm-integration)
5. [Usage Modes](#usage-modes)
6. [Command Reference](#command-reference)
7. [ERP Automation](#erp-automation)
8. [Advanced Features](#advanced-features)
9. [Troubleshooting](#troubleshooting)

## Installation

### System Requirements

- Python 3.8 or higher
- Operating System: Windows, macOS, or Linux
- Tesseract OCR (for text detection)

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/alexjhan/asistent-plant.git
cd asistent-plant

# Install Python dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Install Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Quick Start

### 1. Interactive Mode

The easiest way to get started:

```bash
asistent-plant --interactive
```

Then type commands like:
```
> move mouse to center
> take a screenshot
> type hello world
> click on button
```

### 2. Single Command Mode

Execute one command and exit:

```bash
asistent-plant --command "move mouse to center"
asistent-plant --command "take a screenshot"
```

### 3. Python API

```python
from asistent_plant import DesktopAgent

# Initialize agent
agent = DesktopAgent()

# Execute commands
agent.execute_command("move mouse to center")
agent.execute_command("click on submit button")
agent.execute_command("type Hello World")
```

## Telegram Bot Setup

### Step 1: Create a Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Get Your User ID

1. Search for `@userinfobot` on Telegram
2. Send `/start` to get your user ID

### Step 3: Configure Environment

Create a `.env` file or export variables:

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_AUTHORIZED_USERS="your_user_id"
```

For multiple authorized users:
```bash
export TELEGRAM_AUTHORIZED_USERS="123456789,987654321,555555555"
```

### Step 4: Start the Bot

```bash
asistent-plant --telegram
```

### Using the Bot

In Telegram, send these commands to your bot:

- `/start` - Initialize the bot
- `/help` - Show available commands
- `/status` - Check agent status
- `/screenshot` - Take and receive a screenshot

Or send any text command:
```
move mouse to center
click on submit button
open calculator
```

Or send a voice message, and it will be converted to text and executed.

## LLM Integration

### OpenAI Setup

1. Get an API key from [OpenAI](https://platform.openai.com/)
2. Set the environment variable:
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   ```
3. Start with LLM:
   ```bash
   asistent-plant --telegram --llm openai
   ```

### Ollama Setup (Local LLM)

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model:
   ```bash
   ollama pull llama2
   ```
3. Start with Ollama:
   ```bash
   asistent-plant --telegram --llm ollama --llm-model llama2
   ```

### Benefits of LLM Integration

- Better command understanding
- Context-aware actions
- Multi-step command planning
- Screen analysis for complex tasks

## Usage Modes

### 1. Interactive Mode

```bash
asistent-plant --interactive
```

Best for: Testing commands, learning the system

### 2. Telegram Bot Mode

```bash
asistent-plant --telegram
```

Best for: Remote control, mobile access

### 3. Voice Control Mode

```bash
asistent-plant --voice
```

Best for: Hands-free operation

With wake word:
```bash
asistent-plant --voice --wake-word "hey jarvis"
```

### 4. Single Command Mode

```bash
asistent-plant --command "your command here"
```

Best for: Scripts, automation

## Command Reference

### Mouse Control

```
move mouse to center
move mouse to 500, 300
move to top
move to bottom left
click
click on button
right click
double click on icon
```

### Keyboard Control

```
type hello world
type "special text" and press enter
press enter
press tab
press ctrl+c
```

### Scrolling

```
scroll down
scroll up
scroll down 5
page down
```

### Window Management

```
open calculator
open chrome
maximize window
minimize window
```

### Screen Capture

```
take a screenshot
capture screen
screenshot
```

### Waiting

```
wait 5 seconds
wait for 2 seconds
pause
```

### Multi-Step Commands

Chain commands with "then":
```
click on username then type admin then press tab then type password123 then press enter
```

## ERP Automation

### Example: Data Entry Workflow

```python
from asistent_plant.examples.erp_automation import ERPAutomation

erp = ERPAutomation()

# Login
erp.login_to_erp("username", "password", "MyERP")

# Navigate to module
erp.navigate_to_module("Sales")

# Create sales order
erp.create_sales_order(
    customer="ACME Corp",
    product="Product A",
    quantity=100
)

# Generate report
erp.generate_report("Sales Report", "This Month")
```

### Via Telegram

Send to your bot:
```
Enter today's production: 500 units of Product A in the ERP
```

With LLM enabled, the agent will:
1. Understand the intent
2. Analyze the screen
3. Navigate to the correct form
4. Fill in the data
5. Save and confirm

## Advanced Features

### Custom Configuration

Create `~/.asistent_plant/config.yaml`:

```yaml
language: en-US

llm:
  provider: openai
  model: gpt-3.5-turbo

telegram:
  enabled: true

voice:
  enabled: true
  wake_word: "hey jarvis"
  timeout: 10

vision:
  enabled: true
  confidence_threshold: 60

control:
  mouse_speed: 0.5
  failsafe: true
```

### Screen Analysis

```python
# Analyze screen for a specific task
analysis = agent.analyze_screen_for_task("fill in the login form")

# Execute suggested actions
for action in analysis['actions']:
    print(f"Step {action['step']}: {action['action']}")
```

### Command History

```python
# Get recent commands
history = agent.get_command_history(limit=10)

for entry in history:
    print(entry['command'])
```

### Screen Information

```python
# Get current screen info
info = agent.get_screen_info()

print(f"Screen size: {info['screen_size']}")
print(f"Mouse position: {info['mouse_position']}")
print(f"Active window: {info['active_window']}")
```

## Troubleshooting

### Issue: "pytesseract not available"

**Solution:** Install Tesseract OCR (see Installation section)

### Issue: "Model download fails"

**Solution:** The agent will use fallback keyword matching. For full NLU features, ensure internet connectivity for first-time model download.

### Issue: "Telegram bot not responding"

**Solutions:**
1. Check bot token is correct
2. Verify user ID is in authorized users list
3. Ensure bot is running: `asistent-plant --telegram`

### Issue: "OpenAI API error"

**Solutions:**
1. Verify API key is correct
2. Check API usage limits
3. Test with: `asistent-plant --llm openai --command "test"`

### Issue: "Screen capture fails"

**Solution:** Install mss package: `pip install mss`

### Issue: "Voice recognition not working"

**Solutions:**
1. Install speech_recognition: `pip install SpeechRecognition`
2. For better quality, install PyAudio: `pip install pyaudio`
3. Check microphone permissions

### Issue: "Click not working on specific element"

**Solutions:**
1. Be more specific in command: "click on submit button" instead of "click on button"
2. Use coordinates: "click at 500, 300"
3. Ensure element is visible on screen

## Security Best Practices

1. **Telegram Bot:**
   - Always set `TELEGRAM_AUTHORIZED_USERS`
   - Never share your bot token
   - Use environment variables, not hardcoded values

2. **API Keys:**
   - Store in `.env` file (add to `.gitignore`)
   - Use environment variables
   - Rotate keys regularly

3. **System Access:**
   - Run with minimal required permissions
   - Review commands before execution in production
   - Test in safe environment first

## Examples

See the `asistent_plant/examples/` directory for:

- `basic_usage.py` - Basic command examples
- `erp_automation.py` - ERP workflow automation
- `telegram_usage.py` - Telegram bot examples
- `quick_demo.py` - Validation and testing

## Getting Help

- GitHub Issues: Report bugs or request features
- Documentation: See README.md for overview
- Examples: Check examples directory for code samples

---

For more information, visit: https://github.com/alexjhan/asistent-plant
