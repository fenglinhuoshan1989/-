"""Configuration management for 青简译英 (QingJian Translate).

Supports environment variables and .env file for configuration.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    
    env_file = Path.cwd() / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass

# API Configuration
DEFAULT_MODEL = os.getenv("QINGJIAN_MODEL", "gpt-4-mini")
DEFAULT_TEMPERATURE = float(os.getenv("QINGJIAN_TEMPERATURE", "0.3"))
API_TIMEOUT = int(os.getenv("QINGJIAN_API_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("QINGJIAN_MAX_RETRIES", "2"))

# Validation
MAX_INPUT_LENGTH = int(os.getenv("QINGJIAN_MAX_INPUT_LENGTH", "2000"))

# Logging
LOG_LEVEL = os.getenv("QINGJIAN_LOG_LEVEL", "INFO")
