"""
Quick Demo - Validation of Asistent Plant features
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))


def test_imports():
    """Test that all modules can be imported."""
    print("=" * 60)
    print("Testing Module Imports")
    print("=" * 60)
    
    try:
        from asistent_plant import DesktopAgent
        print("✓ DesktopAgent imported successfully")
        
        from asistent_plant.modules import NLUModule, VisionModule, ControlModule, VoiceModule, LLMModule, TelegramBot
        print("✓ All modules imported successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_agent_initialization():
    """Test agent initialization."""
    print("\n" + "=" * 60)
    print("Testing Agent Initialization")
    print("=" * 60)
    
    try:
        from asistent_plant import DesktopAgent
        
        # Basic initialization
        agent = DesktopAgent()
        print("✓ Agent initialized successfully")
        
        # Check modules
        print(f"  - NLU Module: {'✓' if agent.nlu else '✗'}")
        print(f"  - Vision Module: {'✓' if agent.vision else '✗'}")
        print(f"  - Control Module: {'✓' if agent.control else '✗'}")
        print(f"  - Voice Module: {'✓' if agent.voice else '✗'}")
        print(f"  - LLM Module: {'✓' if agent.llm else '✗'}")
        print(f"  - Telegram Bot: {'✓' if agent.telegram else '✗'}")
        
        return True
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_llm_module():
    """Test LLM module."""
    print("\n" + "=" * 60)
    print("Testing LLM Module")
    print("=" * 60)
    
    try:
        from asistent_plant.modules.llm import LLMModule
        
        # Test with no provider
        llm = LLMModule(provider='none')
        print(f"✓ LLM initialized with provider: {llm.provider.value}")
        print(f"  - Available: {llm.is_available()}")
        
        # Test command enhancement (should fail gracefully)
        result = llm.enhance_command_understanding("click the button")
        print(f"  - Enhancement without LLM: {result['success']} (expected False)")
        
        # Test status message generation
        status = llm.generate_status_message("test", {'success': True})
        print(f"  - Status message: '{status}'")
        
        return True
    except Exception as e:
        print(f"✗ LLM test failed: {e}")
        return False


def test_telegram_bot():
    """Test Telegram bot module."""
    print("\n" + "=" * 60)
    print("Testing Telegram Bot Module")
    print("=" * 60)
    
    try:
        from asistent_plant.modules.telegram_bot import TelegramBot
        
        # Test without token (should handle gracefully)
        bot = TelegramBot()
        print(f"✓ Telegram bot initialized")
        print(f"  - Available: {bot.is_available()}")
        print(f"  - Token configured: {'✓' if bot.token else '✗'}")
        
        if not bot.token:
            print("  - Note: Set TELEGRAM_BOT_TOKEN to enable bot")
        
        return True
    except Exception as e:
        print(f"✗ Telegram test failed: {e}")
        return False


def test_control_module():
    """Test control module."""
    print("\n" + "=" * 60)
    print("Testing Control Module")
    print("=" * 60)
    
    try:
        from asistent_plant.modules.control import ControlModule
        
        control = ControlModule()
        print("✓ Control module initialized")
        
        # Get screen size
        size = control.get_screen_size()
        print(f"  - Screen size: {size}")
        
        # Get mouse position (should work even with stubs)
        pos = control.get_mouse_position()
        print(f"  - Mouse position: {pos}")
        
        return True
    except Exception as e:
        print(f"✗ Control test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_vision_module():
    """Test vision module."""
    print("\n" + "=" * 60)
    print("Testing Vision Module")
    print("=" * 60)
    
    try:
        from asistent_plant.modules.vision import VisionModule
        
        vision = VisionModule()
        print("✓ Vision module initialized")
        
        # Try to capture screen (may use fallback)
        screen = vision.capture_screen()
        print(f"  - Screen capture: {screen.shape}")
        
        return True
    except Exception as e:
        print(f"✗ Vision test failed: {e}")
        return False


def test_configuration():
    """Test configuration."""
    print("\n" + "=" * 60)
    print("Testing Configuration")
    print("=" * 60)
    
    try:
        # Test agent with config
        from asistent_plant import DesktopAgent
        
        config = {
            'language': 'en-US',
            'llm': {
                'provider': 'none'
            },
            'telegram': {
                'token': None
            }
        }
        
        agent = DesktopAgent(config=config)
        print("✓ Agent initialized with config")
        print(f"  - LLM provider: {agent.llm.provider.value}")
        print(f"  - Telegram available: {agent.telegram.is_available()}")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def summary_report(results):
    """Print summary report."""
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The agent is ready to use.")
        print("\nQuick Start:")
        print("  1. Interactive mode: asistent-plant --interactive")
        print("  2. Single command: asistent-plant --command 'take a screenshot'")
        print("  3. Telegram bot: asistent-plant --telegram")
        print("\nFor Telegram, configure:")
        print("  export TELEGRAM_BOT_TOKEN='your_token'")
        print("  export TELEGRAM_AUTHORIZED_USERS='your_user_id'")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("\n" + "=" * 60)


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Asistent Plant - Quick Demo & Validation")
    print("=" * 60)
    print()
    
    results = {}
    
    # Run tests
    results["Module Imports"] = test_imports()
    results["Agent Initialization"] = test_agent_initialization()
    results["LLM Module"] = test_llm_module()
    results["Telegram Bot"] = test_telegram_bot()
    results["Control Module"] = test_control_module()
    results["Vision Module"] = test_vision_module()
    results["Configuration"] = test_configuration()
    
    # Summary
    summary_report(results)


if __name__ == "__main__":
    main()
