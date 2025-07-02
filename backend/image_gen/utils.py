"""
Utility functions for image generation and file handling.
"""

import os
import base64
import io
from PIL import Image


def ensure_directory_exists(directory_path):
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        directory_path (str): Path to the directory to ensure exists
    """
    if directory_path and not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)


def save_image_data(image_data, output_file):
    """
    Save image data to a file.

    Args:
        image_data (bytes): Binary image data
        output_file (str): Path where to save the image
    """
    ensure_directory_exists(os.path.dirname(output_file))

    with open(output_file, "wb") as f:
        f.write(image_data)


def decode_base64_image(base64_string):
    """
    Decode a base64 encoded image string to binary data.

    Args:
        base64_string (str): Base64 encoded image string

    Returns:
        bytes: Binary image data
    """
    return base64.b64decode(base64_string)


def encode_image_to_base64(image_path):
    """
    Encode an image file to base64 string.

    Args:
        image_path (str): Path to the image file

    Returns:
        str: Base64 encoded image string
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def resize_image(image_path, max_size=(1024, 1024), quality=85):
    """
    Resize an image while maintaining aspect ratio.

    Args:
        image_path (str): Path to the image file
        max_size (tuple): Maximum width and height
        quality (int): JPEG quality (1-100)

    Returns:
        str: Path to the resized image (overwrites original)
    """
    with Image.open(image_path) as img:
        # Convert to RGB if necessary
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Calculate new size maintaining aspect ratio
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save the resized image
        img.save(image_path, "JPEG", quality=quality, optimize=True)

    return image_path


def get_image_dimensions(image_path):
    """
    Get the dimensions of an image file.

    Args:
        image_path (str): Path to the image file

    Returns:
        tuple: (width, height) of the image
    """
    with Image.open(image_path) as img:
        return img.size
