"""
Manual .env loader for Django
Add this to the top of settings.py if you don't want to use python-decouple
"""

import os
from pathlib import Path

def load_env_file(env_path=None):
    """Load environment variables from .env file"""
    if env_path is None:
        env_path = Path(__file__).resolve().parent / '.env'
    
    if not os.path.exists(env_path):
        print(f"Warning: .env file not found at {env_path}")
        return
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                os.environ.setdefault(key, value)
    
    print(f"Loaded environment variables from {env_path}")

# Usage in settings.py:
# from load_env import load_env_file
# load_env_file()  # Add this line at the top of settings.py