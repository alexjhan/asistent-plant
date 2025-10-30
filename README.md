# Asistent Plant 🤖

An AI-powered desktop automation agent that combines natural language understanding, computer vision, and system control capabilities. Inspired by Tony Stark's Jarvis, this agent can understand your instructions (from text or voice), analyze your desktop screen, and perform corresponding actions such as mouse movements, clicks, and keyboard input.

## Features ✨

- **Natural Language Understanding**: Parse and understand commands in natural language
- **Computer Vision**: Analyze screen content, detect UI elements, and find text using OCR
- **System Control**: Control mouse, keyboard, and window operations
- **Voice Input**: Speech-to-text for hands-free operation
- **Multi-Step Commands**: Execute complex workflows with a single command
- **ERP Automation**: Specialized support for automating ERP system tasks
- **Interactive Mode**: Command-line interface for real-time control
- **Extensible Architecture**: Modular design for easy customization

## Installation 📦

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR (for text detection)

### Install Tesseract

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

### Install Asistent Plant

```bash
# Clone the repository
git clone https://github.com/alexjhan/asistent-plant.git
cd asistent-plant

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start 🚀

### Interactive Mode

Start the interactive command-line interface:

```bash
python -m asistent_plant.main --interactive
```

Or use the installed command:

```bash
asistent-plant --interactive
```

### Single Command

Execute a single command and exit:

```bash
asistent-plant --command "move mouse to center"
asistent-plant --command "take a screenshot"
asistent-plant --command "type hello world"
```

### Voice Control

Start voice control mode:

```bash
asistent-plant --voice
```

With a wake word:

```bash
asistent-plant --voice --wake-word "hey jarvis"
```

## Usage Examples 💡

### Basic Commands

```python
from asistent_plant import DesktopAgent

agent = DesktopAgent()

# Move mouse
agent.execute_command("move mouse to center")

# Click on an element
agent.execute_command("click on the submit button")

# Type text
agent.execute_command("type 'hello world' and press enter")

# Scroll
agent.execute_command("scroll down 5")

# Take screenshot
agent.execute_command("take a screenshot")

# Wait
agent.execute_command("wait for 3 seconds")
```

### Multi-Step Commands

```python
# Execute multiple actions in sequence
agent.execute_multi_step(
    "move mouse to center then wait 1 second then take a screenshot"
)
```

### Vision-Based Automation

```python
# Find and click a button by its text
agent.execute_command("click on the login button")

# Find text on screen
results = agent.vision.find_text_on_screen("Submit")
for result in results:
    print(f"Found at: ({result['x']}, {result['y']})")
```

### ERP System Automation

```python
from asistent_plant.examples.erp_automation import ERPAutomation

erp = ERPAutomation()

# Login to ERP
erp.login_to_erp("username", "password", "MyERP")

# Navigate to module
erp.navigate_to_module("Sales")

# Create sales order
erp.create_sales_order("ACME Corp", "Product A", 100)

# Generate report
erp.generate_report("Sales Report", "This Month")
```

### Voice Control

```python
# Single voice command
result = agent.execute_voice_command(timeout=10)

# Continuous listening
agent.start_voice_control()

# With wake word
agent.start_voice_control(wake_word="hey jarvis")
```

## Command Reference 📖

### Supported Actions

| Action | Examples |
|--------|----------|
| **Click** | "click on button", "press submit", "right click on icon" |
| **Type** | "type hello world", "enter text and press enter" |
| **Move** | "move mouse to center", "move to 100, 200" |
| **Scroll** | "scroll down", "scroll up 5" |
| **Open** | "open notepad", "launch browser" |
| **Find** | "find the login button", "locate text field" |
| **Wait** | "wait 5 seconds", "pause briefly" |
| **Screenshot** | "take a screenshot", "capture screen" |

### Position Keywords

- `center`: Center of the screen
- `top`: Top center
- `bottom`: Bottom center
- `left`: Left center
- `right`: Right center

## Architecture 🏗️

The agent consists of four main modules:

### 1. NLU Module (`nlu.py`)
- Processes natural language commands
- Extracts intent and parameters
- Uses sentence transformers for semantic understanding

### 2. Vision Module (`vision.py`)
- Screen capture and analysis
- OCR text detection
- Template matching
- UI element detection

### 3. Control Module (`control.py`)
- Mouse control (move, click, drag, scroll)
- Keyboard control (type, press keys, hotkeys)
- Window management

### 4. Voice Module (`voice.py`)
- Speech-to-text conversion
- Continuous listening
- Wake word detection

## Configuration ⚙️

Create a configuration file at `~/.asistent_plant/config.yaml`:

```yaml
language: en-US

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

## Testing 🧪

Run the test suite:

```bash
# Run all tests
python -m unittest discover asistent_plant/tests

# Run specific test
python -m unittest asistent_plant.tests.test_nlu
python -m unittest asistent_plant.tests.test_agent
```

## Examples 📝

Run example scripts:

```bash
# Basic usage examples
python asistent_plant/examples/basic_usage.py

# ERP automation demo
python asistent_plant/examples/erp_automation.py
```

## Safety Features 🛡️

- **Failsafe**: Move mouse to corner to abort operations
- **Pause**: Small delay between actions to prevent issues
- **Error Handling**: Graceful handling of failures
- **Command History**: Track all executed commands

## Limitations ⚠️

- OCR accuracy depends on screen quality and text clarity
- Voice recognition requires internet connection (Google Speech Recognition)
- Platform-specific features may vary
- Some applications may have accessibility restrictions

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

MIT License - See LICENSE file for details

## Acknowledgments 🙏

- Sentence Transformers for NLU
- PyAutoGUI for system control
- Tesseract for OCR
- SpeechRecognition for voice input

## Roadmap 🗺️

- [ ] Add support for more languages
- [ ] Implement custom action macros
- [ ] Add web automation capabilities
- [ ] Improve element detection accuracy
- [ ] Add GUI interface
- [ ] Support for recording and replaying actions
- [ ] Integration with more AI models

## Support 💬

For issues, questions, or suggestions, please open an issue on GitHub.

---

Made with ❤️ by Alex Han
