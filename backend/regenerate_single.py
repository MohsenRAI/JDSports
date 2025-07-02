#!/usr/bin/env python3
"""
Script to regenerate a single specific image variation.
Modified from main.py to target just one body type and skin color combination.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import from main.py
from image_gen import ImageGenerator
from image_gen.models import MALE_BODY_TYPES

# Configuration
DEFAULT_API_KEY = os.getenv("OPENAI_API_KEY", None)
if not DEFAULT_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required.")

# Target settings
TARGET_BODY_TYPE = "average"
TARGET_SKIN_COLOR = "fair-light"
# Color variations for the new product
COLOR_PREFIXES = ["arcticfox_", "black_", "heather_"]
# Set COLOR_PREFIX to one of the new color prefixes as needed
COLOR_PREFIX = COLOR_PREFIXES[0]

# Paths
OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "public",
    "images",
    "bodytypes",
)

REFERENCE_IMAGE = "jordan_red_hoodie_reference.png"

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def regenerate_single_image():
    """Regenerate just the denim average fair-light image."""

    # Find the target body type from MALE_BODY_TYPES
    target_body_type_obj = None
    for body_type in MALE_BODY_TYPES:
        if body_type["name"] == TARGET_BODY_TYPE:
            target_body_type_obj = body_type
            break

    if not target_body_type_obj:
        raise ValueError(f"Body type '{TARGET_BODY_TYPE}' not found in MALE_BODY_TYPES")

    # Initialize image generator
    logger.info("Initializing ImageGenerator...")
    image_gen = ImageGenerator(
        shop="FT", api_key=DEFAULT_API_KEY, debug=True, use_fabric_details=True
    )
    image_gen.image_quality = "medium"

    # Prepare paths
    main_ref_image = os.path.abspath(REFERENCE_IMAGE)

    # Create output directory
    product_code = "headswapper"
    output_subfolder = os.path.join(OUTPUT_DIR, product_code)
    body_type_dir = os.path.join(output_subfolder, TARGET_BODY_TYPE)
    body_type_dir = body_type_dir.replace(os.path.join("public"), os.path.join("frontend", "public"))
    os.makedirs(body_type_dir, exist_ok=True)

    # Define output filename
    output_filename = f"jordan_red_hoodie_reference_{TARGET_SKIN_COLOR}.png"
    output_path = os.path.join(body_type_dir, output_filename)

    logger.info(f"Target file: {output_path}")
    logger.info(
        f"Body type: {TARGET_BODY_TYPE} - {target_body_type_obj['description']}"
    )
    logger.info(f"Skin color: {TARGET_SKIN_COLOR}")
    logger.info(f"Reference images: {len(REFERENCE_IMAGE_MAP)}")

    # Check if file exists
    if os.path.exists(output_path):
        logger.info(f"File exists. Will overwrite: {output_filename}")
    else:
        logger.info(f"Creating new file: {output_filename}")

    try:
        # Generate the image
        logger.info("Starting image generation...")
        image_gen.transform_reference_image(
            reference_image_path=main_ref_image,
            body_type=target_body_type_obj["name"],
            skin_color=TARGET_SKIN_COLOR,
            description=f"{target_body_type_obj['description']} {TARGET_SKIN_COLOR} skin tone",
            output_file=output_path,
            fabric_detail_image=None,
            framing="full",
        )

        logger.info(f"✅ Successfully generated: {output_filename}")
        logger.info(f"📁 Saved to: {output_path}")

    except Exception as e:
        logger.error(f"❌ Error generating image: {str(e)}")
        raise


if __name__ == "__main__":
    print("🎨 Regenerating single image: denim average fair-light")
    print("=" * 50)
    regenerate_single_image()
    print("✅ Complete!")
