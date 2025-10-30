"""
Tests for the Desktop Agent
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from asistent_plant.agent import DesktopAgent


class TestDesktopAgent(unittest.TestCase):
    """Test cases for Desktop Agent."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.agent = DesktopAgent()
    
    def test_agent_initialization(self):
        """Test agent initializes correctly."""
        self.assertIsNotNone(self.agent.nlu)
        self.assertIsNotNone(self.agent.vision)
        self.assertIsNotNone(self.agent.control)
        self.assertIsNotNone(self.agent.voice)
    
    def test_command_history(self):
        """Test command history tracking."""
        initial_count = len(self.agent.command_history)
        
        # Execute a command
        self.agent.execute_command("wait for 1 second", use_vision=False)
        
        # Check history increased
        self.assertEqual(len(self.agent.command_history), initial_count + 1)
        
        # Clear history
        self.agent.clear_history()
        self.assertEqual(len(self.agent.command_history), 0)
    
    def test_get_screen_info(self):
        """Test getting screen information."""
        info = self.agent.get_screen_info()
        
        self.assertIn('screen_size', info)
        self.assertIn('mouse_position', info)
        self.assertIn('all_windows', info)
        
        # Screen size should be a tuple of two positive integers
        self.assertEqual(len(info['screen_size']), 2)
        self.assertGreater(info['screen_size'][0], 0)
        self.assertGreater(info['screen_size'][1], 0)
    
    def test_execute_wait_command(self):
        """Test executing wait command."""
        import time
        
        start_time = time.time()
        result = self.agent.execute_command("wait for 1 second", use_vision=False)
        elapsed = time.time() - start_time
        
        self.assertTrue(result['success'])
        self.assertGreaterEqual(elapsed, 1.0)
    
    def test_execute_screenshot_command(self):
        """Test executing screenshot command."""
        result = self.agent.execute_command("take a screenshot", use_vision=False)
        
        self.assertTrue(result['success'])
        self.assertIn('filename', result)
        
        # Check file was created
        if 'filename' in result:
            filename = result['filename']
            if os.path.exists(filename):
                os.remove(filename)  # Clean up
    
    def test_multi_step_execution(self):
        """Test multi-step command execution."""
        command = "wait 1 second then wait 1 second"
        results = self.agent.execute_multi_step(command, use_vision=False)
        
        self.assertGreater(len(results), 1)
        for result in results:
            self.assertTrue(result['success'])
    
    def test_get_command_history_limit(self):
        """Test getting limited command history."""
        # Clear and add some commands
        self.agent.clear_history()
        
        for i in range(5):
            self.agent.execute_command(f"wait 1 second", use_vision=False)
        
        # Get limited history
        history = self.agent.get_command_history(limit=3)
        self.assertEqual(len(history), 3)


class TestAgentWithoutVision(unittest.TestCase):
    """Test agent functionality without vision."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.agent = DesktopAgent()
    
    def test_move_command_with_position(self):
        """Test move command with position."""
        result = self.agent.execute_command("move mouse to center", use_vision=False)
        
        self.assertTrue(result['success'])
    
    def test_failed_command_handling(self):
        """Test handling of commands that should fail gracefully."""
        # Command without proper parameters
        result = self.agent.execute_command("click on", use_vision=False)
        
        # Should not crash, even if it fails
        self.assertIn('success', result)


if __name__ == '__main__':
    unittest.main()
