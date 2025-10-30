"""
Stub implementations for control module when dependencies are missing
"""

import time
from typing import Optional, Tuple


class MockPyAutoGUI:
    """Mock implementation of pyautogui for testing."""
    
    @staticmethod
    def size():
        return (1920, 1080)
    
    @staticmethod
    def moveTo(x, y, duration=0):
        pass
    
    @staticmethod
    def moveRel(dx, dy, duration=0):
        pass
    
    @staticmethod
    def click(x=None, y=None, clicks=1, interval=0, button='left'):
        pass
    
    @staticmethod
    def drag(x, y, duration=0, button='left'):
        pass
    
    @staticmethod
    def scroll(amount, x=None, y=None):
        pass
    
    @staticmethod
    def write(text, interval=0):
        pass
    
    @staticmethod
    def press(key, presses=1, interval=0):
        pass
    
    @staticmethod
    def hotkey(*keys):
        pass
    
    @staticmethod
    def hold(key):
        class HoldContext:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        return HoldContext()
    
    @staticmethod
    def position():
        return (100, 100)
    
    @staticmethod
    def alert(text='', title=''):
        print(f"Alert: {text}")
    
    @staticmethod
    def confirm(text='', title='', buttons=None):
        return 'OK'
    
    @staticmethod
    def prompt(text='', title='', default=''):
        return default
    
    FAILSAFE = True
    PAUSE = 0.1


class MockWindow:
    """Mock window object."""
    
    def __init__(self, title='Mock Window'):
        self.title = title
    
    def activate(self):
        pass
    
    def minimize(self):
        pass
    
    def maximize(self):
        pass
    
    def resizeTo(self, width, height):
        pass
    
    def moveTo(self, x, y):
        pass


def get_active_window():
    """Mock get active window."""
    return MockWindow()


def get_windows_with_title(title):
    """Mock get windows with title."""
    return [MockWindow(title)]


def get_all_windows():
    """Mock get all windows."""
    return [MockWindow("Window 1"), MockWindow("Window 2")]
