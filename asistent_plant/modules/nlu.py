"""
Natural Language Understanding Module
Processes text/voice commands and extracts intent and parameters
"""

import re
from typing import Dict, List, Optional, Tuple
from sentence_transformers import SentenceTransformer, util
import torch


class NLUModule:
    """
    Natural Language Understanding module for processing user commands.
    Uses sentence transformers for semantic understanding.
    """

    def __init__(self):
        """Initialize the NLU module with a pre-trained model."""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Define action templates with examples
        self.action_templates = {
            "click": [
                "click on the button",
                "press the submit button",
                "tap on the icon",
                "select the menu item"
            ],
            "type": [
                "type hello world",
                "enter the text",
                "write a message",
                "input the data"
            ],
            "move": [
                "move mouse to coordinates",
                "move cursor to the top",
                "position mouse at center"
            ],
            "scroll": [
                "scroll down the page",
                "scroll up",
                "page down"
            ],
            "open": [
                "open the application",
                "launch the program",
                "start the software"
            ],
            "find": [
                "find the button",
                "locate the text field",
                "search for the icon"
            ],
            "wait": [
                "wait for 5 seconds",
                "pause briefly",
                "hold on"
            ],
            "screenshot": [
                "take a screenshot",
                "capture the screen",
                "save screen image"
            ]
        }
        
        # Pre-compute embeddings for action templates
        self.action_embeddings = {}
        for action, templates in self.action_templates.items():
            self.action_embeddings[action] = self.model.encode(
                templates, convert_to_tensor=True
            )

    def parse_command(self, command: str) -> Dict:
        """
        Parse a natural language command into structured action.
        
        Args:
            command: Natural language command string
            
        Returns:
            Dictionary with action, target, and parameters
        """
        command = command.lower().strip()
        
        # Encode the command
        command_embedding = self.model.encode(command, convert_to_tensor=True)
        
        # Find the best matching action
        best_action = None
        best_score = -1
        
        for action, embeddings in self.action_embeddings.items():
            scores = util.cos_sim(command_embedding, embeddings)
            max_score = torch.max(scores).item()
            
            if max_score > best_score:
                best_score = max_score
                best_action = action
        
        # Extract parameters based on action
        params = self._extract_parameters(command, best_action)
        
        return {
            "action": best_action,
            "confidence": best_score,
            "parameters": params,
            "raw_command": command
        }

    def _extract_parameters(self, command: str, action: str) -> Dict:
        """
        Extract parameters from command based on action type.
        
        Args:
            command: The command string
            action: The identified action
            
        Returns:
            Dictionary of parameters
        """
        params = {}
        
        if action == "click":
            # Extract target element
            target = self._extract_target(command)
            if target:
                params["target"] = target
            
            # Check for double click
            if "double" in command:
                params["double_click"] = True
            
            # Check for right click
            if "right" in command:
                params["button"] = "right"
        
        elif action == "type":
            # Extract text to type
            text = self._extract_text_to_type(command)
            if text:
                params["text"] = text
            
            # Check if should press enter
            if "enter" in command or "submit" in command:
                params["press_enter"] = True
        
        elif action == "move":
            # Extract coordinates or position
            coords = self._extract_coordinates(command)
            if coords:
                params["x"], params["y"] = coords
            else:
                position = self._extract_position(command)
                if position:
                    params["position"] = position
        
        elif action == "scroll":
            # Extract scroll direction and amount
            if "up" in command:
                params["direction"] = "up"
            elif "down" in command:
                params["direction"] = "down"
            
            amount = self._extract_number(command)
            if amount:
                params["amount"] = amount
        
        elif action == "open":
            # Extract application name
            app_name = self._extract_app_name(command)
            if app_name:
                params["application"] = app_name
        
        elif action == "find":
            # Extract element to find
            target = self._extract_target(command)
            if target:
                params["target"] = target
        
        elif action == "wait":
            # Extract wait duration
            duration = self._extract_number(command)
            if duration:
                params["duration"] = duration
            else:
                params["duration"] = 2  # Default wait time
        
        return params

    def _extract_target(self, command: str) -> Optional[str]:
        """Extract target element from command."""
        patterns = [
            r'(?:click|press|tap|select|find)\s+(?:on\s+)?(?:the\s+)?(.+)',
            r'(?:button|icon|field|menu|item|element)\s+(?:called|named|labeled)\s+(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command)
            if match:
                target = match.group(1).strip()
                # Clean up common words
                target = re.sub(r'\s+(button|icon|field|menu|item|element)$', '', target)
                return target
        
        return None

    def _extract_text_to_type(self, command: str) -> Optional[str]:
        """Extract text to be typed from command."""
        patterns = [
            r'(?:type|enter|write|input)\s+["\'](.+?)["\']',
            r'(?:type|enter|write|input)\s+(.+?)(?:\s+and\s+(?:press\s+)?enter)?$',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command)
            if match:
                return match.group(1).strip()
        
        return None

    def _extract_coordinates(self, command: str) -> Optional[Tuple[int, int]]:
        """Extract coordinates from command."""
        pattern = r'(\d+)\s*,?\s*(\d+)'
        match = re.search(pattern, command)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None

    def _extract_position(self, command: str) -> Optional[str]:
        """Extract relative position from command."""
        positions = ["center", "top", "bottom", "left", "right"]
        for pos in positions:
            if pos in command:
                return pos
        return None

    def _extract_number(self, command: str) -> Optional[int]:
        """Extract a number from command."""
        pattern = r'(\d+)'
        match = re.search(pattern, command)
        if match:
            return int(match.group(1))
        return None

    def _extract_app_name(self, command: str) -> Optional[str]:
        """Extract application name from command."""
        pattern = r'(?:open|launch|start)\s+(?:the\s+)?(.+?)(?:\s+application|\s+app|\s+program|$)'
        match = re.search(pattern, command)
        if match:
            return match.group(1).strip()
        return None

    def parse_multi_step_command(self, command: str) -> List[Dict]:
        """
        Parse a command that contains multiple steps.
        
        Args:
            command: Command string potentially containing multiple actions
            
        Returns:
            List of parsed action dictionaries
        """
        # Split by common separators
        separators = [" then ", " and then ", ", then ", " followed by "]
        steps = [command]
        
        for separator in separators:
            new_steps = []
            for step in steps:
                new_steps.extend(step.split(separator))
            steps = new_steps
        
        # Parse each step
        return [self.parse_command(step) for step in steps if step.strip()]
