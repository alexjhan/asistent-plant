"""
Main entry point for the Asistent Plant desktop automation agent
"""

import argparse
import sys
from .agent import DesktopAgent


def main():
    """Main function to run the desktop agent."""
    parser = argparse.ArgumentParser(
        description="Asistent Plant - AI-powered desktop automation agent"
    )
    
    parser.add_argument(
        '-c', '--command',
        type=str,
        help='Execute a single command and exit'
    )
    
    parser.add_argument(
        '-v', '--voice',
        action='store_true',
        help='Enable voice control mode'
    )
    
    parser.add_argument(
        '-w', '--wake-word',
        type=str,
        default=None,
        help='Wake word for voice control (e.g., "hey jarvis")'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Start interactive command-line mode'
    )
    
    parser.add_argument(
        '--no-vision',
        action='store_true',
        help='Disable computer vision features'
    )
    
    parser.add_argument(
        '--language',
        type=str,
        default='en-US',
        help='Language code for voice recognition (default: en-US)'
    )
    
    args = parser.parse_args()
    
    # Initialize the agent
    config = {
        'language': args.language
    }
    
    try:
        agent = DesktopAgent(config=config)
    except Exception as e:
        print(f"Error initializing agent: {e}")
        sys.exit(1)
    
    use_vision = not args.no_vision
    
    # Execute based on mode
    if args.command:
        # Single command mode
        result = agent.execute_command(args.command, use_vision=use_vision)
        
        if result['success']:
            print(f"✓ {result['message']}")
            sys.exit(0)
        else:
            print(f"✗ {result['message']}")
            sys.exit(1)
    
    elif args.voice:
        # Voice control mode
        try:
            agent.start_voice_control(wake_word=args.wake_word)
        except KeyboardInterrupt:
            print("\nStopping voice control")
            sys.exit(0)
    
    elif args.interactive:
        # Interactive mode
        agent.interactive_mode()
    
    else:
        # Default: show help and start interactive mode
        parser.print_help()
        print("\n" + "="*50)
        print("Starting interactive mode...")
        print("="*50)
        agent.interactive_mode()


if __name__ == "__main__":
    main()
