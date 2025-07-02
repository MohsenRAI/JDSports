#!/usr/bin/env python3
"""
Quick script to generate just one test image.
"""

import os
import sys
from dotenv import load_dotenv
from image_gen import ImageGenerator
from image_gen.models import MALE_BODY_TYPES

# Load environment variables
load_dotenv()

# Target configuration
TARGET_BODY_TYPE = "overweight"
TARGET_SKIN_COLOR = "olive"
TARGET_COLOR = "arcticfox_"
REFERENCE_IMAGE = "jordan_red_hoodie_reference.png"

def generate_single_image():
    """Generate a single test image."""
    print(f"🎯 Targeting: {TARGET_BODY_TYPE} body type with {TARGET_SKIN_COLOR} skin")
    print("=" * 60)
    
    # Initialize image generator
    image_gen = ImageGenerator(
        shop="FT",
        api_key=os.getenv("OPENAI_API_KEY"),
        debug=True,
        use_fabric_details=True
    )
    image_gen.image_quality = "medium"
    
    # Get reference image
    main_ref_image = os.path.abspath(REFERENCE_IMAGE)
    
    # Create output directory
    OUTPUT_DIR = os.path.join(
        os.path.dirname(__file__),
        "..",
        "frontend",
        "public",
        "images",
        "bodytypes",
        "headswapper",
        TARGET_BODY_TYPE
    )
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Define output filename
    output_filename = f"jordan_red_hoodie_reference_{TARGET_SKIN_COLOR}.png"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    # Get body type description
    body_type_info = next((bt for bt in MALE_BODY_TYPES if bt["name"] == TARGET_BODY_TYPE), None)
    if not body_type_info:
        raise ValueError(f"Body type {TARGET_BODY_TYPE} not found")
    
    try:
        # Generate the image
        image_gen.transform_reference_image(
            reference_image_path=main_ref_image,
            body_type=TARGET_BODY_TYPE,
            skin_color=TARGET_SKIN_COLOR,
            description=f"{body_type_info['description']} with {TARGET_SKIN_COLOR} skin tone",
            output_file=output_path,
            fabric_detail_image=None,
            framing="full"
        )
        print(f"\n✅ Image generated successfully: {output_filename}")
        
    except Exception as e:
        print(f"\n❌ Error generating image: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    generate_single_image()
