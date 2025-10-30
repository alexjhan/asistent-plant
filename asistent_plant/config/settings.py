"""
Configuration settings for the desktop agent
"""

import os
import yaml
from typing import Dict, Optional


def get_default_config() -> Dict:
    """
    Get default configuration settings.
    
    Returns:
        Default configuration dictionary
    """
    return {
        'language': 'en-US',
        'voice': {
            'enabled': True,
            'wake_word': None,
            'timeout': 10,
            'energy_threshold': 300,
            'dynamic_energy': True
        },
        'vision': {
            'enabled': True,
            'ocr_language': 'eng',
            'confidence_threshold': 60
        },
        'control': {
            'mouse_speed': 0.5,
            'failsafe': True,
            'pause': 0.1
        },
        'nlu': {
            'model': 'all-MiniLM-L6-v2',
            'confidence_threshold': 0.5
        },
        'logging': {
            'enabled': True,
            'level': 'INFO',
            'file': 'asistent_plant.log'
        }
    }


def load_config(config_path: Optional[str] = None) -> Dict:
    """
    Load configuration from file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        config_path = os.path.expanduser('~/.asistent_plant/config.yaml')
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                
            # Merge with defaults
            default_config = get_default_config()
            return {**default_config, **config}
        except Exception as e:
            print(f"Error loading config: {e}")
            return get_default_config()
    
    return get_default_config()


def save_config(config: Dict, config_path: Optional[str] = None):
    """
    Save configuration to file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save configuration
    """
    if config_path is None:
        config_path = os.path.expanduser('~/.asistent_plant/config.yaml')
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        print(f"Configuration saved to {config_path}")
    except Exception as e:
        print(f"Error saving config: {e}")
