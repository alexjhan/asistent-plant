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
    
    parser.add_argument(
        '--telegram',
        action='store_true',
        help='Start Telegram bot for remote control'
    )
    
    parser.add_argument(
        '--llm',
        type=str,
        choices=['openai', 'ollama', 'none'],
        default='none',
        help='LLM provider for enhanced understanding (default: none)'
    )
    
    parser.add_argument(
        '--llm-model',
        type=str,
        help='LLM model name (e.g., gpt-4, llama2)'
    )
    
    args = parser.parse_args()
    
    # Initialize the agent
    config = {
        'language': args.language,
        'llm': {
            'provider': args.llm,
            'model': args.llm_model
        },
        'telegram': {
            # Token and users loaded from environment variables
        }
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
    
    elif args.telegram:
        # Telegram bot mode
        agent.start_telegram_bot()
    
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
