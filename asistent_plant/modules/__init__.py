"""
Core modules for the desktop automation agent
"""

from .nlu import NLUModule
from .vision import VisionModule
from .control import ControlModule
from .voice import VoiceModule
from .llm import LLMModule
from .telegram_bot import TelegramBot

__all__ = [
    "NLUModule", 
    "VisionModule", 
    "ControlModule", 
    "VoiceModule",
    "LLMModule",
    "TelegramBot"
]
