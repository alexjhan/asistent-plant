"""
System Control Module
Handles mouse, keyboard, and window operations
"""

import time
from typing import Optional, Tuple

try:
    import pyautogui
    pyautogui.FAILSAFE = True  # Move mouse to corner to abort
    pyautogui.PAUSE = 0.1  # Small pause between actions
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    from . import control_stub
    pyautogui = control_stub.MockPyAutoGUI()
    PYAUTOGUI_AVAILABLE = False

try:
    from pynput import mouse, keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False

try:
    import pygetwindow as gw
    PYGETWINDOW_AVAILABLE = True
except ImportError:
    from . import control_stub
    
    class gw:
        getActiveWindow = control_stub.get_active_window
        getWindowsWithTitle = control_stub.get_windows_with_title
        getAllWindows = control_stub.get_all_windows
    
    PYGETWINDOW_AVAILABLE = False


class ControlModule:
    """
    System control module for mouse, keyboard, and window operations.
    """

    def __init__(self):
        """Initialize the control module."""
        if not PYAUTOGUI_AVAILABLE:
            # Fallback to default screen size
            self.screen_size = (1920, 1080)
        else:
            self.screen_size = pyautogui.size()
        
        if PYNPUT_AVAILABLE:
            self.mouse_controller = mouse.Controller()
            self.keyboard_controller = keyboard.Controller()
        else:
            self.mouse_controller = None
            self.keyboard_controller = None

    def move_mouse(self, x: int, y: int, duration: float = 0.5):
        """
        Move mouse to specific coordinates.
        
        Args:
            x, y: Screen coordinates
            duration: Time to complete the movement
        """
        if not PYAUTOGUI_AVAILABLE:
            print(f"Mock: Moving mouse to ({x}, {y})")
            return
        pyautogui.moveTo(x, y, duration=duration)

    def move_mouse_relative(self, dx: int, dy: int, duration: float = 0.5):
        """
        Move mouse relative to current position.
        
        Args:
            dx, dy: Relative movement
            duration: Time to complete the movement
        """
        pyautogui.moveRel(dx, dy, duration=duration)

    def click(self, x: Optional[int] = None, y: Optional[int] = None, 
              button: str = "left", clicks: int = 1, interval: float = 0.0):
        """
        Perform a mouse click.
        
        Args:
            x, y: Optional coordinates (uses current position if None)
            button: Mouse button ('left', 'right', 'middle')
            clicks: Number of clicks
            interval: Time between clicks for multiple clicks
        """
        if x is not None and y is not None:
            pyautogui.click(x, y, clicks=clicks, interval=interval, button=button)
        else:
            pyautogui.click(clicks=clicks, interval=interval, button=button)

    def double_click(self, x: Optional[int] = None, y: Optional[int] = None):
        """
        Perform a double click.
        
        Args:
            x, y: Optional coordinates
        """
        self.click(x, y, clicks=2, interval=0.1)

    def right_click(self, x: Optional[int] = None, y: Optional[int] = None):
        """
        Perform a right click.
        
        Args:
            x, y: Optional coordinates
        """
        self.click(x, y, button="right")

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, 
             duration: float = 0.5, button: str = "left"):
        """
        Drag from one position to another.
        
        Args:
            start_x, start_y: Starting coordinates
            end_x, end_y: Ending coordinates
            duration: Time to complete the drag
            button: Mouse button to use
        """
        self.move_mouse(start_x, start_y, duration=0.2)
        pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration, button=button)

    def scroll(self, amount: int, x: Optional[int] = None, y: Optional[int] = None):
        """
        Scroll the mouse wheel.
        
        Args:
            amount: Scroll amount (positive = up, negative = down)
            x, y: Optional position to scroll at
        """
        if x is not None and y is not None:
            self.move_mouse(x, y, duration=0.2)
        
        pyautogui.scroll(amount)

    def type_text(self, text: str, interval: float = 0.0):
        """
        Type text using the keyboard.
        
        Args:
            text: Text to type
            interval: Time between key presses
        """
        pyautogui.write(text, interval=interval)

    def press_key(self, key: str, presses: int = 1, interval: float = 0.0):
        """
        Press a specific key.
        
        Args:
            key: Key name (e.g., 'enter', 'space', 'tab')
            presses: Number of times to press
            interval: Time between presses
        """
        pyautogui.press(key, presses=presses, interval=interval)

    def press_hotkey(self, *keys):
        """
        Press a combination of keys (hotkey).
        
        Args:
            *keys: Keys to press together (e.g., 'ctrl', 'c')
        """
        pyautogui.hotkey(*keys)

    def hold_key(self, key: str):
        """
        Hold down a key (context manager compatible).
        
        Args:
            key: Key to hold
        """
        return pyautogui.hold(key)

    def get_mouse_position(self) -> Tuple[int, int]:
        """
        Get current mouse position.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        return pyautogui.position()

    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get screen dimensions.
        
        Returns:
            Tuple of (width, height)
        """
        return self.screen_size

    def move_to_position(self, position: str, duration: float = 0.5):
        """
        Move mouse to a relative position on screen.
        
        Args:
            position: Position name ('center', 'top', 'bottom', 'left', 'right')
            duration: Time to complete movement
        """
        width, height = self.screen_size
        
        positions = {
            'center': (width // 2, height // 2),
            'top': (width // 2, 50),
            'bottom': (width // 2, height - 50),
            'left': (50, height // 2),
            'right': (width - 50, height // 2),
            'top-left': (50, 50),
            'top-right': (width - 50, 50),
            'bottom-left': (50, height - 50),
            'bottom-right': (width - 50, height - 50)
        }
        
        if position in positions:
            x, y = positions[position]
            self.move_mouse(x, y, duration=duration)

    # Window management functions

    def get_active_window(self):
        """
        Get the currently active window.
        
        Returns:
            Window object or None
        """
        try:
            return gw.getActiveWindow()
        except:
            return None

    def get_window_by_title(self, title: str):
        """
        Find a window by its title.
        
        Args:
            title: Window title (partial match)
            
        Returns:
            Window object or None
        """
        windows = gw.getWindowsWithTitle(title)
        return windows[0] if windows else None

    def activate_window(self, window_title: str):
        """
        Activate (bring to front) a window by title.
        
        Args:
            window_title: Window title to activate
            
        Returns:
            True if successful, False otherwise
        """
        window = self.get_window_by_title(window_title)
        if window:
            try:
                window.activate()
                return True
            except:
                pass
        return False

    def minimize_window(self, window_title: Optional[str] = None):
        """
        Minimize a window.
        
        Args:
            window_title: Window title (uses active window if None)
        """
        if window_title:
            window = self.get_window_by_title(window_title)
        else:
            window = self.get_active_window()
        
        if window:
            window.minimize()

    def maximize_window(self, window_title: Optional[str] = None):
        """
        Maximize a window.
        
        Args:
            window_title: Window title (uses active window if None)
        """
        if window_title:
            window = self.get_window_by_title(window_title)
        else:
            window = self.get_active_window()
        
        if window:
            window.maximize()

    def resize_window(self, width: int, height: int, 
                      window_title: Optional[str] = None):
        """
        Resize a window.
        
        Args:
            width, height: New dimensions
            window_title: Window title (uses active window if None)
        """
        if window_title:
            window = self.get_window_by_title(window_title)
        else:
            window = self.get_active_window()
        
        if window:
            window.resizeTo(width, height)

    def move_window(self, x: int, y: int, window_title: Optional[str] = None):
        """
        Move a window to specific coordinates.
        
        Args:
            x, y: New position
            window_title: Window title (uses active window if None)
        """
        if window_title:
            window = self.get_window_by_title(window_title)
        else:
            window = self.get_active_window()
        
        if window:
            window.moveTo(x, y)

    def list_all_windows(self):
        """
        List all open windows.
        
        Returns:
            List of window titles
        """
        return [w.title for w in gw.getAllWindows() if w.title]

    # Utility functions

    def wait(self, seconds: float):
        """
        Wait for a specified time.
        
        Args:
            seconds: Time to wait
        """
        time.sleep(seconds)

    def alert(self, message: str, title: str = "Alert"):
        """
        Show an alert dialog.
        
        Args:
            message: Alert message
            title: Alert title
        """
        pyautogui.alert(text=message, title=title)

    def confirm(self, message: str, title: str = "Confirm") -> bool:
        """
        Show a confirmation dialog.
        
        Args:
            message: Confirmation message
            title: Dialog title
            
        Returns:
            True if OK clicked, False otherwise
        """
        result = pyautogui.confirm(text=message, title=title, buttons=['OK', 'Cancel'])
        return result == 'OK'

    def prompt(self, message: str, title: str = "Input", default: str = "") -> Optional[str]:
        """
        Show an input prompt dialog.
        
        Args:
            message: Prompt message
            title: Dialog title
            default: Default value
            
        Returns:
            User input or None if cancelled
        """
        return pyautogui.prompt(text=message, title=title, default=default)
