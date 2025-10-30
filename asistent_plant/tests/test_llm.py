"""
Tests for the LLM module
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from asistent_plant.modules.llm import LLMModule, LLMProvider


class TestLLMModule(unittest.TestCase):
    """Test cases for LLM module."""
    
    def test_initialization_none(self):
        """Test initialization with no provider."""
        llm = LLMModule(provider='none')
        
        self.assertEqual(llm.provider, LLMProvider.NONE)
        self.assertFalse(llm.is_available())
    
    def test_initialization_openai_no_key(self):
        """Test OpenAI initialization without API key."""
        # Clear any existing key
        old_key = os.environ.get('OPENAI_API_KEY')
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        llm = LLMModule(provider='openai')
        
        # Restore old key
        if old_key:
            os.environ['OPENAI_API_KEY'] = old_key
        
        # Should not be available without key
        if llm.provider == LLMProvider.OPENAI:
            self.assertIsNone(llm.client)
    
    def test_enhance_command_without_llm(self):
        """Test command enhancement when LLM is not available."""
        llm = LLMModule(provider='none')
        
        result = llm.enhance_command_understanding("click the button")
        
        self.assertFalse(result['success'])
        self.assertFalse(result['enhanced'])
    
    def test_analyze_screen_without_llm(self):
        """Test screen analysis when LLM is not available."""
        llm = LLMModule(provider='none')
        
        result = llm.analyze_screen_context("Some screen text", "Click submit")
        
        self.assertFalse(result['success'])
    
    def test_generate_status_message_fallback(self):
        """Test status message generation without LLM."""
        llm = LLMModule(provider='none')
        
        result = {'success': True, 'message': 'Command executed'}
        message = llm.generate_status_message("test command", result)
        
        self.assertIn('✓', message)
        self.assertIsInstance(message, str)
    
    def test_format_context(self):
        """Test context formatting."""
        llm = LLMModule(provider='none')
        
        context = {
            'screen_size': (1920, 1080),
            'windows': ['Window 1', 'Window 2'],
            'mouse_pos': (100, 100)
        }
        
        formatted = llm._format_context(context)
        
        self.assertIsInstance(formatted, str)
        self.assertIn('screen_size', formatted)


class TestLLMProviderEnum(unittest.TestCase):
    """Test LLM provider enumeration."""
    
    def test_provider_values(self):
        """Test provider enum values."""
        self.assertEqual(LLMProvider.OPENAI.value, 'openai')
        self.assertEqual(LLMProvider.OLLAMA.value, 'ollama')
        self.assertEqual(LLMProvider.NONE.value, 'none')


if __name__ == '__main__':
    unittest.main()
