"""
Tests for the NLU module
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from asistent_plant.modules.nlu import NLUModule


class TestNLUModule(unittest.TestCase):
    """Test cases for NLU module."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.nlu = NLUModule()
    
    def test_parse_click_command(self):
        """Test parsing click commands."""
        result = self.nlu.parse_command("click on the submit button")
        
        self.assertEqual(result['action'], 'click')
        self.assertIn('target', result['parameters'])
        self.assertIn('submit', result['parameters']['target'].lower())
    
    def test_parse_type_command(self):
        """Test parsing type commands."""
        result = self.nlu.parse_command("type hello world")
        
        self.assertEqual(result['action'], 'type')
        self.assertIn('text', result['parameters'])
    
    def test_parse_move_command(self):
        """Test parsing move commands."""
        result = self.nlu.parse_command("move mouse to center")
        
        self.assertEqual(result['action'], 'move')
        self.assertIn('position', result['parameters'])
    
    def test_parse_scroll_command(self):
        """Test parsing scroll commands."""
        result = self.nlu.parse_command("scroll down the page")
        
        self.assertEqual(result['action'], 'scroll')
        self.assertEqual(result['parameters']['direction'], 'down')
    
    def test_parse_wait_command(self):
        """Test parsing wait commands."""
        result = self.nlu.parse_command("wait for 5 seconds")
        
        self.assertEqual(result['action'], 'wait')
        self.assertIn('duration', result['parameters'])
    
    def test_parse_multi_step_command(self):
        """Test parsing multi-step commands."""
        command = "click on button then type hello then press enter"
        results = self.nlu.parse_multi_step_command(command)
        
        self.assertGreater(len(results), 1)
        self.assertEqual(results[0]['action'], 'click')
    
    def test_confidence_score(self):
        """Test confidence scores."""
        result = self.nlu.parse_command("click the button")
        
        self.assertIn('confidence', result)
        self.assertIsInstance(result['confidence'], float)
        self.assertGreater(result['confidence'], 0)
    
    def test_extract_coordinates(self):
        """Test coordinate extraction."""
        coords = self.nlu._extract_coordinates("move to 100, 200")
        
        self.assertIsNotNone(coords)
        self.assertEqual(coords, (100, 200))
    
    def test_extract_number(self):
        """Test number extraction."""
        num = self.nlu._extract_number("wait for 10 seconds")
        
        self.assertIsNotNone(num)
        self.assertEqual(num, 10)
    
    def test_extract_target(self):
        """Test target extraction."""
        target = self.nlu._extract_target("click on the save button")
        
        self.assertIsNotNone(target)
        self.assertIn('save', target.lower())


class TestNLUParameterExtraction(unittest.TestCase):
    """Test cases for parameter extraction."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.nlu = NLUModule()
    
    def test_extract_button_names(self):
        """Test extracting button names."""
        commands = [
            "click on submit",
            "press the cancel button",
            "tap on ok"
        ]
        
        for cmd in commands:
            result = self.nlu.parse_command(cmd)
            self.assertIn('target', result['parameters'])
    
    def test_extract_text_with_quotes(self):
        """Test extracting text with quotes."""
        result = self.nlu.parse_command('type "hello world"')
        
        self.assertEqual(result['parameters']['text'], 'hello world')
    
    def test_extract_positions(self):
        """Test extracting position keywords."""
        positions = ['center', 'top', 'bottom', 'left', 'right']
        
        for pos in positions:
            result = self.nlu.parse_command(f"move mouse to {pos}")
            self.assertEqual(result['parameters']['position'], pos)


if __name__ == '__main__':
    unittest.main()
