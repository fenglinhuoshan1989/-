"""Unified configuration for QingJian Translate."""

from typing import List
import os
from pathlib import Path

# Supported OpenAI models
SUPPORTED_MODELS: List[str] = [
    "gpt-4o-mini",      # Default: newest and most cost-effective
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
]

# Default configuration
DEFAULT_MODEL = SUPPORTED_MODELS[0]
DEFAULT_TEMPERATURE = 0.3
DEFAULT_LANGUAGE = os.getenv("LANGUAGE", "zh_CN").split(".")[0]  # Extract lang code

# API and performance settings
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", "5000"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_BACKOFF_FACTOR = 2  # Exponential backoff: 1s, 2s, 4s...

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Directories
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / "locales"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
LOCALES_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Feature flags
ENABLE_BATCH_TRANSLATE = True
ENABLE_HISTORY = True
ENABLE_PERFORMANCE_METRICS = True
