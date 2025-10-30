"""
Basic usage examples for Asistent Plant
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from asistent_plant import DesktopAgent


def example_text_commands():
    """Example: Execute text commands."""
    print("=== Text Command Examples ===\n")
    
    agent = DesktopAgent()
    
    # Example 1: Move mouse
    print("1. Moving mouse to center...")
    result = agent.execute_command("move mouse to center")
    print(f"   Result: {result['message']}\n")
    
    # Example 2: Take screenshot
    print("2. Taking a screenshot...")
    result = agent.execute_command("take a screenshot")
    print(f"   Result: {result['message']}\n")
    
    # Example 3: Wait
    print("3. Waiting for 2 seconds...")
    result = agent.execute_command("wait for 2 seconds")
    print(f"   Result: {result['message']}\n")


def example_multi_step():
    """Example: Multi-step command."""
    print("=== Multi-Step Command Example ===\n")
    
    agent = DesktopAgent()
    
    command = "move mouse to center then wait 1 second then take a screenshot"
    print(f"Executing: {command}\n")
    
    results = agent.execute_multi_step(command)
    
    for i, result in enumerate(results, 1):
        print(f"Step {i}: {result['message']}")


def example_screen_info():
    """Example: Get screen information."""
    print("=== Screen Information Example ===\n")
    
    agent = DesktopAgent()
    
    info = agent.get_screen_info()
    
    print(f"Screen Size: {info['screen_size']}")
    print(f"Mouse Position: {info['mouse_position']}")
    print(f"Active Window: {info['active_window']}")
    print(f"\nAll Windows ({len(info['all_windows'])}):")
    for window in info['all_windows'][:5]:  # Show first 5
        print(f"  - {window}")


def example_typing():
    """Example: Type text."""
    print("=== Typing Example ===\n")
    print("This will type 'Hello from Asistent Plant!' after 3 seconds")
    print("Make sure a text input is focused!\n")
    
    agent = DesktopAgent()
    
    # Wait to give user time to focus a text input
    agent.execute_command("wait for 3 seconds")
    
    # Type text
    result = agent.execute_command("type 'Hello from Asistent Plant!'")
    print(f"Result: {result['message']}")


def example_window_management():
    """Example: Window management."""
    print("=== Window Management Example ===\n")
    
    agent = DesktopAgent()
    
    # List all windows
    windows = agent.control.list_all_windows()
    print(f"Found {len(windows)} windows:")
    for i, window in enumerate(windows[:10], 1):
        print(f"{i}. {window}")


if __name__ == "__main__":
    print("Asistent Plant - Example Scripts\n")
    print("Available examples:")
    print("1. Text commands")
    print("2. Multi-step commands")
    print("3. Screen information")
    print("4. Typing (requires focused text input)")
    print("5. Window management")
    print("0. Run all examples")
    
    choice = input("\nSelect an example (0-5): ").strip()
    
    examples = {
        '1': example_text_commands,
        '2': example_multi_step,
        '3': example_screen_info,
        '4': example_typing,
        '5': example_window_management,
    }
    
    if choice == '0':
        example_text_commands()
        print("\n" + "="*50 + "\n")
        example_multi_step()
        print("\n" + "="*50 + "\n")
        example_screen_info()
        print("\n" + "="*50 + "\n")
        example_window_management()
    elif choice in examples:
        examples[choice]()
    else:
        print("Invalid choice")
