"""
Desktop Agent - Main orchestrator for the AI desktop automation agent
"""

import time
from typing import Dict, List, Optional, Callable
from .modules import NLUModule, VisionModule, ControlModule, VoiceModule


class DesktopAgent:
    """
    Main orchestrator for the AI-powered desktop automation agent.
    Combines NLU, computer vision, and system control to perform automated tasks.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the desktop agent.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
        # Initialize modules
        print("Initializing AI Desktop Agent...")
        self.nlu = NLUModule()
        self.vision = VisionModule()
        self.control = ControlModule()
        self.voice = VoiceModule(language=self.config.get('language', 'en-US'))
        
        print("Agent initialized successfully!")
        
        # State
        self.running = False
        self.last_command = None
        self.command_history = []

    def execute_command(self, command: str, use_vision: bool = True) -> Dict:
        """
        Execute a natural language command.
        
        Args:
            command: Natural language command
            use_vision: Whether to use computer vision for element detection
            
        Returns:
            Execution result dictionary
        """
        print(f"\nExecuting command: {command}")
        
        # Parse the command
        parsed = self.nlu.parse_command(command)
        print(f"Parsed action: {parsed['action']} (confidence: {parsed['confidence']:.2f})")
        
        # Store in history
        self.command_history.append({
            'command': command,
            'parsed': parsed,
            'timestamp': time.time()
        })
        
        # Execute based on action type
        result = self._execute_action(parsed, use_vision)
        
        self.last_command = parsed
        return result

    def _execute_action(self, parsed: Dict, use_vision: bool) -> Dict:
        """
        Execute a parsed action.
        
        Args:
            parsed: Parsed command dictionary
            use_vision: Whether to use vision for element detection
            
        Returns:
            Execution result
        """
        action = parsed['action']
        params = parsed['parameters']
        
        try:
            if action == "click":
                return self._execute_click(params, use_vision)
            
            elif action == "type":
                return self._execute_type(params)
            
            elif action == "move":
                return self._execute_move(params)
            
            elif action == "scroll":
                return self._execute_scroll(params)
            
            elif action == "open":
                return self._execute_open(params)
            
            elif action == "find":
                return self._execute_find(params)
            
            elif action == "wait":
                return self._execute_wait(params)
            
            elif action == "screenshot":
                return self._execute_screenshot(params)
            
            else:
                return {
                    'success': False,
                    'message': f"Unknown action: {action}"
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f"Error executing action: {str(e)}"
            }

    def _execute_click(self, params: Dict, use_vision: bool) -> Dict:
        """Execute a click action."""
        target = params.get('target')
        
        if target and use_vision:
            # Try to find the target element using vision
            print(f"Searching for: {target}")
            element = self.vision.find_button(target)
            
            if element:
                x, y = element['x'], element['y']
                print(f"Found element at ({x}, {y})")
            else:
                return {
                    'success': False,
                    'message': f"Could not find element: {target}"
                }
        else:
            # Use current mouse position
            x, y = None, None
        
        # Perform the click
        if params.get('double_click'):
            self.control.double_click(x, y)
            action_type = "double click"
        elif params.get('button') == 'right':
            self.control.right_click(x, y)
            action_type = "right click"
        else:
            self.control.click(x, y)
            action_type = "click"
        
        return {
            'success': True,
            'message': f"Performed {action_type}",
            'location': (x, y) if x else None
        }

    def _execute_type(self, params: Dict) -> Dict:
        """Execute a type action."""
        text = params.get('text', '')
        
        if not text:
            return {
                'success': False,
                'message': "No text specified to type"
            }
        
        self.control.type_text(text)
        
        if params.get('press_enter'):
            self.control.press_key('enter')
        
        return {
            'success': True,
            'message': f"Typed: {text}"
        }

    def _execute_move(self, params: Dict) -> Dict:
        """Execute a mouse move action."""
        if 'x' in params and 'y' in params:
            x, y = params['x'], params['y']
            self.control.move_mouse(x, y)
            return {
                'success': True,
                'message': f"Moved mouse to ({x}, {y})"
            }
        elif 'position' in params:
            position = params['position']
            self.control.move_to_position(position)
            return {
                'success': True,
                'message': f"Moved mouse to {position}"
            }
        else:
            return {
                'success': False,
                'message': "No coordinates or position specified"
            }

    def _execute_scroll(self, params: Dict) -> Dict:
        """Execute a scroll action."""
        direction = params.get('direction', 'down')
        amount = params.get('amount', 3)
        
        # Convert direction to scroll amount
        scroll_amount = amount * 100 if direction == 'up' else -amount * 100
        
        self.control.scroll(scroll_amount)
        
        return {
            'success': True,
            'message': f"Scrolled {direction} by {amount} units"
        }

    def _execute_open(self, params: Dict) -> Dict:
        """Execute an open application action."""
        app_name = params.get('application')
        
        if not app_name:
            return {
                'success': False,
                'message': "No application specified"
            }
        
        # Try to activate existing window first
        if self.control.activate_window(app_name):
            return {
                'success': True,
                'message': f"Activated window: {app_name}"
            }
        
        # Otherwise, try to launch (this is platform-specific)
        # For now, we'll just press Win key and type the app name
        self.control.press_key('win')
        time.sleep(0.5)
        self.control.type_text(app_name)
        time.sleep(0.3)
        self.control.press_key('enter')
        
        return {
            'success': True,
            'message': f"Attempted to open: {app_name}"
        }

    def _execute_find(self, params: Dict) -> Dict:
        """Execute a find element action."""
        target = params.get('target')
        
        if not target:
            return {
                'success': False,
                'message': "No target specified"
            }
        
        element = self.vision.find_button(target)
        
        if element:
            return {
                'success': True,
                'message': f"Found element at ({element['x']}, {element['y']})",
                'element': element
            }
        else:
            return {
                'success': False,
                'message': f"Could not find: {target}"
            }

    def _execute_wait(self, params: Dict) -> Dict:
        """Execute a wait action."""
        duration = params.get('duration', 2)
        
        self.control.wait(duration)
        
        return {
            'success': True,
            'message': f"Waited for {duration} seconds"
        }

    def _execute_screenshot(self, params: Dict) -> Dict:
        """Execute a screenshot action."""
        filename = params.get('filename', f'screenshot_{int(time.time())}.png')
        
        self.vision.save_screenshot(filename)
        
        return {
            'success': True,
            'message': f"Screenshot saved: {filename}",
            'filename': filename
        }

    def execute_multi_step(self, command: str, use_vision: bool = True) -> List[Dict]:
        """
        Execute a multi-step command.
        
        Args:
            command: Command potentially containing multiple steps
            use_vision: Whether to use vision
            
        Returns:
            List of execution results
        """
        steps = self.nlu.parse_multi_step_command(command)
        results = []
        
        for i, step in enumerate(steps):
            print(f"\nStep {i+1}/{len(steps)}: {step['raw_command']}")
            result = self._execute_action(step, use_vision)
            results.append(result)
            
            # Small delay between steps
            time.sleep(0.5)
        
        return results

    def start_voice_control(self, wake_word: Optional[str] = None):
        """
        Start voice control mode.
        
        Args:
            wake_word: Optional wake word to activate commands
        """
        print("\n=== Voice Control Mode ===")
        
        if wake_word:
            print(f"Say '{wake_word}' followed by your command")
            self.voice.listen_with_wake_word(
                wake_word=wake_word,
                callback=lambda cmd: self.execute_command(cmd)
            )
        else:
            print("Continuous listening mode")
            print("Say 'stop listening' to exit")
            self.voice.listen_continuous(
                callback=lambda cmd: self.execute_command(cmd)
            )

    def execute_voice_command(self, timeout: int = 10) -> Optional[Dict]:
        """
        Listen for and execute a single voice command.
        
        Args:
            timeout: Maximum time to wait for speech
            
        Returns:
            Execution result or None
        """
        text = self.voice.listen_once(timeout=timeout)
        
        if text:
            return self.execute_command(text)
        
        return None

    def get_command_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get command execution history.
        
        Args:
            limit: Maximum number of commands to return
            
        Returns:
            List of command history entries
        """
        if limit:
            return self.command_history[-limit:]
        return self.command_history

    def clear_history(self):
        """Clear command history."""
        self.command_history = []

    def get_screen_info(self) -> Dict:
        """
        Get information about the current screen.
        
        Returns:
            Dictionary with screen information
        """
        width, height = self.control.get_screen_size()
        mouse_x, mouse_y = self.control.get_mouse_position()
        active_window = self.control.get_active_window()
        
        return {
            'screen_size': (width, height),
            'mouse_position': (mouse_x, mouse_y),
            'active_window': active_window.title if active_window else None,
            'all_windows': self.control.list_all_windows()
        }

    def interactive_mode(self):
        """
        Start interactive command-line mode.
        """
        print("\n=== Interactive Mode ===")
        print("Enter commands in natural language (or 'quit' to exit)")
        print("Examples:")
        print("  - Click on the submit button")
        print("  - Type hello world and press enter")
        print("  - Move mouse to center")
        print("  - Scroll down 5")
        print("  - Take a screenshot")
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['quit', 'exit', 'q']:
                    print("Exiting interactive mode")
                    break
                
                if command.lower() == 'help':
                    self._show_help()
                    continue
                
                if command.lower() == 'history':
                    self._show_history()
                    continue
                
                if command.lower() == 'info':
                    info = self.get_screen_info()
                    print(f"\nScreen: {info['screen_size']}")
                    print(f"Mouse: {info['mouse_position']}")
                    print(f"Active Window: {info['active_window']}")
                    continue
                
                result = self.execute_command(command)
                
                if result['success']:
                    print(f"✓ {result['message']}")
                else:
                    print(f"✗ {result['message']}")
            
            except KeyboardInterrupt:
                print("\nExiting interactive mode")
                break
            except Exception as e:
                print(f"Error: {e}")

    def _show_help(self):
        """Show help information."""
        print("\nAvailable commands:")
        print("  - Natural language commands (e.g., 'click on button', 'type text')")
        print("  - help: Show this help")
        print("  - history: Show command history")
        print("  - info: Show screen information")
        print("  - quit/exit: Exit interactive mode")

    def _show_history(self):
        """Show command history."""
        history = self.get_command_history(limit=10)
        
        if not history:
            print("No command history")
            return
        
        print("\nRecent commands:")
        for i, entry in enumerate(reversed(history), 1):
            print(f"  {i}. {entry['command']}")
