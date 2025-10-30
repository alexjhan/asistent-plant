"""
LLM Module for enhanced natural language reasoning
Supports OpenAI API and local Ollama models
"""

import os
from typing import Dict, List, Optional, Union
from enum import Enum


class LLMProvider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    OLLAMA = "ollama"
    NONE = "none"


class LLMModule:
    """
    LLM module for enhanced natural language understanding and reasoning.
    Supports OpenAI and Ollama backends.
    """
    
    def __init__(self, provider: str = "none", model: Optional[str] = None, 
                 api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the LLM module.
        
        Args:
            provider: LLM provider ('openai', 'ollama', or 'none')
            model: Model name (e.g., 'gpt-4', 'llama2')
            api_key: API key for OpenAI
            base_url: Base URL for Ollama (default: http://localhost:11434)
        """
        self.provider = LLMProvider(provider.lower())
        self.model = model
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = base_url or os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.client = None
        
        if self.provider == LLMProvider.OPENAI:
            self._init_openai()
        elif self.provider == LLMProvider.OLLAMA:
            self._init_ollama()
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            import openai
            if not self.api_key:
                print("Warning: OpenAI API key not provided")
                return
            
            self.client = openai.OpenAI(api_key=self.api_key)
            self.model = self.model or 'gpt-3.5-turbo'
            print(f"Initialized OpenAI with model: {self.model}")
        except ImportError:
            print("Warning: openai package not installed. Install with: pip install openai")
            self.provider = LLMProvider.NONE
    
    def _init_ollama(self):
        """Initialize Ollama client."""
        try:
            import ollama
            self.client = ollama
            self.model = self.model or 'llama2'
            print(f"Initialized Ollama with model: {self.model}")
        except ImportError:
            print("Warning: ollama package not installed. Install with: pip install ollama")
            self.provider = LLMProvider.NONE
    
    def is_available(self) -> bool:
        """Check if LLM is available."""
        return self.provider != LLMProvider.NONE and self.client is not None
    
    def enhance_command_understanding(self, command: str, context: Optional[Dict] = None) -> Dict:
        """
        Use LLM to enhance understanding of the command.
        
        Args:
            command: User command
            context: Optional context (screen info, previous commands, etc.)
            
        Returns:
            Enhanced command interpretation
        """
        if not self.is_available():
            return {
                'success': False,
                'message': 'LLM not available',
                'enhanced': False
            }
        
        system_prompt = """You are an AI assistant helping to interpret desktop automation commands.
Your task is to:
1. Understand the user's intent
2. Extract specific actions needed (click, type, move, etc.)
3. Identify target elements or coordinates
4. Break down complex commands into steps
5. Provide structured output for automation

Respond in JSON format with:
{
    "intent": "brief description of what user wants",
    "actions": [
        {
            "action": "click|type|move|scroll|wait|etc",
            "target": "element name or description",
            "parameters": {"key": "value"}
        }
    ],
    "confidence": 0.0-1.0,
    "notes": "any clarifications or assumptions"
}"""
        
        context_str = ""
        if context:
            context_str = f"\n\nContext:\n{self._format_context(context)}"
        
        user_message = f"Command: {command}{context_str}"
        
        try:
            response = self._call_llm(system_prompt, user_message)
            
            # Try to parse JSON response
            import json
            try:
                parsed = json.loads(response)
                parsed['success'] = True
                parsed['enhanced'] = True
                return parsed
            except json.JSONDecodeError:
                # If not JSON, return as text
                return {
                    'success': True,
                    'enhanced': True,
                    'raw_response': response,
                    'intent': response
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f"LLM error: {str(e)}",
                'enhanced': False
            }
    
    def analyze_screen_context(self, screen_description: str, task: str) -> Dict:
        """
        Analyze screen content to determine actions.
        
        Args:
            screen_description: Description of current screen (OCR text, elements, etc.)
            task: Task to perform
            
        Returns:
            Analysis with suggested actions
        """
        if not self.is_available():
            return {'success': False, 'message': 'LLM not available'}
        
        system_prompt = """You are analyzing a desktop screen to help automate tasks.
Given a description of the current screen and a task, determine the specific actions needed.

Provide a structured plan in JSON format:
{
    "analysis": "what you see on the screen",
    "actions": [
        {
            "step": 1,
            "action": "action type",
            "target": "element to interact with",
            "input": "text to type if applicable"
        }
    ],
    "confidence": 0.0-1.0,
    "warnings": ["any potential issues"]
}"""
        
        user_message = f"Screen content:\n{screen_description}\n\nTask: {task}"
        
        try:
            response = self._call_llm(system_prompt, user_message)
            
            import json
            try:
                parsed = json.loads(response)
                parsed['success'] = True
                return parsed
            except json.JSONDecodeError:
                return {
                    'success': True,
                    'raw_response': response
                }
        
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def generate_status_message(self, command: str, result: Dict) -> str:
        """
        Generate a human-friendly status message.
        
        Args:
            command: Original command
            result: Execution result
            
        Returns:
            Formatted status message
        """
        if not self.is_available():
            # Fallback to simple message
            if result.get('success'):
                return f"✓ Completed: {command}"
            else:
                return f"✗ Failed: {command}\nError: {result.get('message', 'Unknown error')}"
        
        system_prompt = """Generate a concise, friendly status message for the user.
Keep it brief (1-2 sentences) and informative."""
        
        user_message = f"Command: {command}\nResult: {result}\n\nGenerate a status message."
        
        try:
            response = self._call_llm(system_prompt, user_message)
            return response.strip()
        except:
            # Fallback
            if result.get('success'):
                return f"✓ {result.get('message', 'Command completed')}"
            else:
                return f"✗ {result.get('message', 'Command failed')}"
    
    def _call_llm(self, system_prompt: str, user_message: str) -> str:
        """
        Call the LLM with messages.
        
        Args:
            system_prompt: System prompt
            user_message: User message
            
        Returns:
            LLM response text
        """
        if self.provider == LLMProvider.OPENAI:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            return response.choices[0].message.content
        
        elif self.provider == LLMProvider.OLLAMA:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            return response['message']['content']
        
        return ""
    
    def _format_context(self, context: Dict) -> str:
        """Format context dictionary as string."""
        lines = []
        for key, value in context.items():
            if isinstance(value, (list, dict)):
                lines.append(f"{key}: {len(value)} items")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)
    
    def test_connection(self) -> bool:
        """
        Test LLM connection.
        
        Returns:
            True if connection successful
        """
        if not self.is_available():
            return False
        
        try:
            response = self._call_llm("You are a helpful assistant.", "Say 'OK'")
            return len(response) > 0
        except Exception as e:
            print(f"LLM connection test failed: {e}")
            return False
