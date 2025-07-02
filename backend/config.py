# config.py
# Male body types import
from image_gen.models import MALE_BODY_TYPES
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

"""
Configuration settings for the Image Generation system.
"""

# OpenAI API Key
# Load from environment variable for security
DEFAULT_API_KEY = os.getenv("OPENAI_API_KEY", None)

if not DEFAULT_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY environment variable is required. "
        "Please set it in your environment or .env file."
    )

# Models
CHAT_MODEL = "gpt-4.1"
IMAGE_MODEL = "gpt-image-1"

# Image settings
DEFAULT_IMAGE_SIZE = "1024x1536"
DEFAULT_IMAGE_QUALITY = "medium"  # "high" or "medium" or "low"

# Directory settings
INPUT_DIR = "images/Input"
OUTPUT_DIR = "images/Output"
BODY_VARIATIONS_DIR = "body_variations"

# Temporary directories
TEMP_DIR = "temp"

# Reference image suffix
REFERENCE_IMAGE_SUFFIX = "_MODEL_FULL.jpg"
SECONDARY_REFERENCE_IMAGE_SUFFIX = "_MODEL_FRONT.jpg"


# Skin color variations
SKIN_COLORS = [
    "fair-light",
    "olive",
    "brown",
    "dark-brown",
]
