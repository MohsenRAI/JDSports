# image_gen/image_generator.py

import os
import sys
import time
import traceback
import random
import json
import tempfile
import requests
import re
import glob
from tqdm import tqdm
from openai import OpenAI
from openai import BadRequestError, RateLimitError, APIError, APIConnectionError
from image_gen.utils import (
    ensure_directory_exists,
    save_image_data,
    decode_base64_image,
)
from image_gen.models import MALE_BODY_TYPES
from image_gen.prompts import get_body_generation_prompt, get_outfit_application_prompt
from image_gen.poses import get_pose_for_body_and_skin

# Add the project root to the path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# config.py
# Male body types import
from image_gen.models import MALE_BODY_TYPES

"""
Configuration settings for the Image Generation system.
"""

# OpenAI API Key
# In production, this should be loaded from environment variables
DEFAULT_API_KEY = os.getenv("OPENAI_API_KEY", None)

if not DEFAULT_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY environment variable is required. "
        "Please set it in your environment or .env file."
    )

# Models
# CHAT_MODEL = "gpt-4.1"
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

REFERENCE_IMAGE_PREFIXES = ["1_", "2_"]

SHOP = "CT"  # 'CT' or 'FT'


# Skin color variations
SKIN_COLORS = [
    # "porcelain",
    "fair-light",
    # "light-beige",
    "medium",
    "olive",
    # "tan",
    "brown",
    "deep",
]


class ImageGenerator:
    def __init__(self, shop=SHOP, api_key=None, debug=True, use_fabric_details=False):
        """
        Initialize the Image Generator.

        Args:
            api_key (str, optional): OpenAI API key
            debug (bool): Whether to print debug information including prompts
            use_fabric_details (bool): Whether to include fabric details in image generation
        """
        if api_key is None:
            api_key = DEFAULT_API_KEY

        self.client = OpenAI(api_key=api_key)
        self.debug = debug
        self.image_quality = DEFAULT_IMAGE_QUALITY
        self.use_fabric_details = use_fabric_details

        # Define the full body prompt
        self.full_body_prompt = """Create a full-body professional fashion photo of a male model.

⚠️ CRITICAL FRAMING REQUIREMENTS - MUST FOLLOW EXACTLY:
- OUTPUT MUST BE A FULL BODY IMAGE showing the COMPLETE model from HEAD (including ALL HAIR) to TOE (including COMPLETE SHOES)
- The model's entire head, hair, and face MUST be completely visible and clear
- Divide the frame into a 3x3 grid
- Subject's head MUST be centered in the middle square of the top row
- There MUST be a FULL empty grid square (33% of frame height) above the head
- Subject's full body should occupy the middle column of squares
- Feet should rest in the bottom third, well above bottom edge

CAMERA SETUP AND POSITION:
- Camera at chest height (about 4.5 feet / 137cm from ground)
- Tilt up 5-10 degrees to create natural headroom
- Distance: far enough to show full body with 33% margin above head
- Focal length: 85mm equivalent (to avoid distortion)
- Portrait orientation (4:5 ratio)

POSE SELECTION:
- IMPORTANT: Use the specific pose instructions provided below in the prompt
- Do not default to generic poses
- Follow the pose description exactly as specified
- Maintain natural and realistic body positioning

BACKGROUND AND LIGHTING:
- Add proper lighting and SHADOWS to the image to make it look realistic using the background setting from the pose description
- Professional studio lighting with dramatic shadows on subject
- Rim light to highlight figure
- Even lighting across the frame

CLOTHING:
- Crisp white dress shirt
- Light gray dress pants
- Black leather belt
- Clean, pressed appearance

TECHNICAL SPECIFICATIONS:
- 8k quality
- Hyperrealistic
- Photorealistic
- Sharp focus throughout
- No motion blur

⚠️ FINAL CHECKS - MUST VERIFY ALL: 
1. HEAD POSITION:
   - Head MUST be in middle square of top row
   - Full empty grid square (33%) above head
   - No part of head/hair touches top third of frame

2. BODY FRAMING:
   - Full body visible with consistent margins
   - Subject centered in middle column
   - No cropping of any body parts

3. POSE AND STYLE:
   - Pose matches the specific instructions provided
   - Face clearly visible to camera
   - Proper professional clothing

4. TECHNICAL:
   - Sharp focus throughout
   - Professional lighting
   - Add proper lighting and SHADOWS to the image to make it look realistic using the background setting from the pose description
⚠️ CRITICAL: If ANY of these checks fail, the image must be regenerated."""

        # Define the knee-length (2/3 body) prompt
        self.knee_length_prompt = """Create a knee-length (2/3 body) professional fashion photo of a male model.

⚠️ CRITICAL FRAMING REQUIREMENTS - MUST FOLLOW EXACTLY:
- OUTPUT MUST BE A 2/3 BODY IMAGE showing the model from HEAD (including ALL HAIR) to KNEES
- The model's entire head, hair, and face MUST be completely visible and clear
- Divide the frame into a 3x3 grid
- Subject's head MUST be centered in the middle square of the top row
- There MUST be adequate headroom (space above head)
- Subject's body should occupy the middle column of squares
- Knees should rest at the bottom edge of the frame
- DO NOT show anything below the knees

CAMERA SETUP AND POSITION:
- Camera at chest height (about 4.5 feet / 137cm from ground)
- Distance: close enough to show body down to knees with proper margins
- Focal length: 85mm equivalent (to avoid distortion)
- Portrait orientation (4:5 ratio)

POSE SELECTION:
- IMPORTANT: Use the specific pose instructions provided below in the prompt
- Adapt the pose to work with knee-length framing
- Ensure hands and arms are visible within the frame
- Maintain natural and realistic body positioning

BACKGROUND AND LIGHTING:
- Add proper lighting and SHADOWS to the image to make it look realistic using the background setting from the pose description
- Professional studio lighting with dramatic shadows on subject
- Rim light to highlight figure
- Even lighting across the frame

CLOTHING:
- Crisp white dress shirt
- Light gray dress pants
- Black leather belt
- Clean, pressed appearance

TECHNICAL SPECIFICATIONS:
- 8k quality
- Hyperrealistic
- Photorealistic
- Sharp focus throughout
- No motion blur

⚠️ FINAL CHECKS - MUST VERIFY ALL: 
1. HEAD POSITION:
   - Head positioned properly with adequate headroom
   - Full head and hair visible and clear
   - Good face visibility

2. BODY FRAMING:
   - Body visible down to knees with consistent margins
   - Subject centered in frame
   - Nothing below knees is visible

3. POSE AND STYLE:
   - Pose adapted appropriately for knee-length framing
   - Face clearly visible to camera
   - Proper professional clothing

4. TECHNICAL:
   - Sharp focus throughout
   - Professional lighting
   - Add proper lighting and SHADOWS to the image to make it look realistic using the background setting from the pose description
⚠️ CRITICAL: If ANY of these checks fail, the image must be regenerated."""

        # Define the transform prompt for full body
        self.full_body_transform_prompt = """Create a professional fashion photo by transforming this base body image to wear the tux and tie (if present), bow tie (if present), and the matching shoes, trousers, and socks from the reference fashion image.

THE COLOR AND TEXTURE OF THE TUX AND VEST, POCKET AND LAPEL DETAILS, ETC. MUST BE EXACTLY THE SAME AS THE FIRST REFERENCE IMAGE.

- ⚠️ CAREFULLY EXAMINE the fabric detail image provided as the  reference image
- PRECISELY replicate all fabric textures, patterns, weaves, and material properties shown in the detail image
- MATCH the exact fabric appearance including color variations, sheen, and surface characteristics
- ENSURE all seams, stitching, buttons, and hardware elements are accurately recreated
- REPRODUCE any fabric-specific qualities like wrinkle patterns, drape, or stretch characteristics
- MAINTAIN the exact same fabric thickness and weight appearance as shown in the detail image
- APPLY these fabric details consistently across the entire garment
- The fabric detail image shows the TRUE, HIGH-FIDELITY representation of how the fabric should appear

CRITICAL REQUIREMENTS (MUST FOLLOW EXACTLY):
- ⚠️ DON'T ADD ANY CLOSING ITEMS other than the ones in the reference image. 
- ⚠️ Follow the exact patterns of the source garment regarding color, Texture, Lapel, vest, tie, bow tie, buttons, pocket, etc. 
- ⚠️ OUTPUT MUST BE A FULL BODY IMAGE showing the COMPLETE model from HEAD (including ALL HAIR) to TOE (including COMPLETE SHOES)
- ⚠️ Add proper lighting and SHADOWS to the image to make it look realistic using the background setting from the pose description
- ⚠️ The model's entire head, hair, and face MUST be completely visible and clear
- COPY EXACT GARMENT ITEMS from the reference image
- PRESERVE the base body's body type, proportions, and skin color
- Add proper lighting and SHADOWS to the image to make it look realistic using the background setting from the pose description

- FOLLOW THE POSE INSTRUCTIONS provided in this prompt

CLOTHING APPLICATION:
- Apply ALL clothing items from the reference exactly as shown
- Maintain the same fit, patterns, textures and color of clothing
- Ensure clothing fits the body type appropriately
- Preserve all product details, tags, buttons, etc.

COMPOSITION REQUIREMENTS:
- ⚠️ HEAD & HAIR POSITION: Complete head WITH FULL HAIR must be in the top third of the frame
- ⚠️ FEET & SHOES: Complete shoes must be fully visible at the bottom of the frame
- FRAMING: Ensure proper headroom (space above head)
- ENSURE THE ENTIRE BODY is shown from head to toe with proper margins
- DO NOT crop any part of the body - EVERY part must be fully visible
- ZOOM OUT enough to ensure nothing is cropped - if in doubt, zoom out more

IMPORTANT TECHNICAL DETAILS:
- The clothing must look realistic on the body
- Maintain professional fashion photography standards
- Preserve the model's original face, hair, body type and skin tone
- Keep the model centered with the same amount of space above head
- Ensure sharp focus throughout the entire image
- The final image should be studio-quality for commercial fashion use

CRITICAL INSTRUCTIONS For Tux and Vest , Pocket and Lapel Details, etc. APPLY THESE EXACTLY and CAREFULLY and CONSISTENTLY.
Add proper lighting and SHADOWS to the image to make it look realistic using the background setting from the pose description
- ⚠️ CAREFULLY EXAMINE the fabric detail image provided as the  reference image
- PRECISELY replicate all fabric textures, patterns, weaves, and material properties shown in the detail image
- MATCH the exact fabric appearance including color variations, sheen, and surface characteristics
- ENSURE all seams, stitching, buttons, and hardware elements are accurately recreated
- REPRODUCE any fabric-specific qualities like wrinkle patterns, drape, or stretch characteristics
- MAINTAIN the exact same fabric thickness and weight appearance as shown in the detail image
- APPLY these fabric details consistently across the entire garment
- The fabric detail image shows the TRUE, HIGH-FIDELITY representation of how the fabric should appear
"""

        # Define the transform prompt for knee-length (2/3 body)
        self.knee_length_transform_prompt = """Create a knee-length (2/3 body) professional fashion photo by transforming this base body image to wear the outfit from the reference fashion image.

CRITICAL REQUIREMENTS (MUST FOLLOW EXACTLY):
- ⚠️ DON'T ADD ANY CLOSING ITEMS other than the ones in the reference image. DON'T ADD JACKET if the reference image doesn't have one
- ⚠️ OUTPUT MUST BE A 2/3 BODY IMAGE showing the model from HEAD (including ALL HAIR) to KNEES
- ⚠️ The model's entire head, hair, and face MUST be completely visible and clear
- COPY EXACT CLOTHING ITEMS from the reference image
- PRESERVE the base body's body type, proportions, and skin color
- Add proper lighting and SHADOWS to the image to make it look realistic using the background setting from the pose description
- FOLLOW THE POSE INSTRUCTIONS provided in this prompt

CLOTHING APPLICATION:
- Apply ALL clothing items from the reference exactly as shown
- Maintain the same fit, patterns, textures and color of clothing
- Ensure clothing fits the body type appropriately
- Preserve all product details, tags, buttons, etc.

COMPOSITION REQUIREMENTS:
- ⚠️ HEAD & HAIR POSITION: Complete head WITH FULL HAIR must be in the top third of the frame
- ⚠️ KNEES: The frame should end at the knees - DO NOT SHOW BELOW THE KNEES
- FRAMING: Ensure proper headroom (space above head)
- ENSURE THE BODY is shown down to the knees with proper margins
- Zoom appropriately to focus on upper body and torso down to knees
- Center the subject in the frame

IMPORTANT TECHNICAL DETAILS:
- The clothing must look realistic on the body
- Maintain professional fashion photography standards
- Preserve the model's original face, hair, body type and skin tone
- Keep the model centered with appropriate spacing
- Ensure sharp focus throughout the entire image
- The final image should be studio-quality for commercial fashion use

CRITICAL INSTRUCTIONS For Tux and Vest , Pocket and Lapel Details, etc. APPLY THESE EXACTLY and CAREFULLY and CONSISTENTLY and don't add any additional items like sunglasses, hats, etc.
Add proper lighting and SHADOWS to the image to make it look realistic using the background setting from the pose description
"""

        # Set the default prompts
        self.body_prompt = self.full_body_prompt
        self.transform_prompt = self.full_body_transform_prompt
        self.shop = "CT"  # 'CT' or 'FT'

    def _log_prompt(self, title, prompt):
        """
        Log a prompt to the console if debug is enabled.

        Args:
            title (str): Title/description of the prompt
            prompt (str): The actual prompt text
        """
        if self.debug:
            print("\n" + "=" * 80)
            print(f"DEBUG - {title}")
            print("=" * 80)
            print(prompt)
            print("=" * 80 + "\n")

    def _handle_api_error(
        self, error, operation_type="API call", retry_count=0, max_retries=3
    ):
        """
        Handle API errors with proper wait times and retry logic.

        Args:
            error: The exception that was raised
            operation_type (str): Description of the operation being performed
            retry_count (int): Current retry attempt number
            max_retries (int): Maximum number of retry attempts

        Returns:
            bool: True if the operation should be retried, False otherwise
            int: Number of seconds to wait before retrying
        """
        # Base wait time (seconds)
        base_wait = 10

        # Default wait time
        wait_time = base_wait * (2**retry_count) + random.uniform(0, 1)

        if isinstance(error, RateLimitError):
            print(
                f"⚠️ Rate limit exceeded during {operation_type}. Waiting and retrying..."
            )

            # Check if the error response contains a specific retry-after time
            if hasattr(error, "headers") and "retry-after" in error.headers:
                retry_after = int(error.headers["retry-after"])
                wait_time = max(wait_time, retry_after + 1)  # Add 1 second buffer
            else:
                # Apply exponential backoff for rate limit errors
                wait_time = base_wait * (2**retry_count) + random.uniform(1, 5)

            if retry_count < max_retries:
                print(
                    f"Waiting {wait_time:.1f} seconds before retry {retry_count + 1}/{max_retries}..."
                )
                return True, wait_time
            else:
                print(
                    f"Maximum retries ({max_retries}) reached. Giving up on this operation."
                )
                return False, 0

        elif isinstance(error, APIConnectionError):
            if retry_count < max_retries:
                print(
                    f"⚠️ API connection error during {operation_type}. Waiting {wait_time:.1f} seconds before retry {retry_count + 1}/{max_retries}..."
                )
                return True, wait_time
            else:
                print(
                    f"Maximum retries ({max_retries}) reached. Giving up on this operation."
                )
                return False, 0

        elif isinstance(error, APIError):
            if error.status_code and error.status_code >= 500:
                # Server errors might resolve with a retry
                if retry_count < max_retries:
                    print(
                        f"⚠️ Server error ({error.status_code}) during {operation_type}. Waiting {wait_time:.1f} seconds before retry {retry_count + 1}/{max_retries}..."
                    )
                    return True, wait_time
                else:
                    print(
                        f"Maximum retries ({max_retries}) reached. Giving up on this operation."
                    )
                    return False, 0
            else:
                # Client errors (4xx) are unlikely to be resolved with retries
                print(
                    f"❌ API error ({error.status_code if error.status_code else 'unknown'}) during {operation_type}. Error details: {str(error)}"
                )
                return False, 0
        else:
            # Other errors are unlikely to be resolved with retries
            print(f"❌ Error during {operation_type}: {str(error)}")
            return False, 0

    def generate_image(
        self, prompt, output_file=None, size=DEFAULT_IMAGE_SIZE, quality=None
    ):
        """
        Generate an image using GPT Image model.

        Args:
            prompt (str): Text prompt for image generation
            output_file (str, optional): Path to save the generated image
            size (str, optional): Image size, default from config
            quality (str, optional): Image quality, defaults to self.image_quality

        Returns:
            bytes: Image data in binary format
        """
        if quality is None:
            quality = self.image_quality

        max_retries = 3
        retry_count = 0

        while retry_count <= max_retries:
            try:
                # Log the prompt for debugging
                self._log_prompt("IMAGE GENERATION PROMPT", prompt)

                response = self.client.images.generate(
                    model=IMAGE_MODEL,
                    prompt=prompt,
                    size=size,
                    quality=quality,
                    n=1,
                )

                # Get the first image from the response
                image = response.data[0]

                # GPT Image model always returns base64 data
                image_data = decode_base64_image(image.b64_json)

                # Save the image if output file is specified
                if output_file:
                    # Ensure output directory exists
                    output_dir = os.path.dirname(output_file)
                    ensure_directory_exists(output_dir)
                    save_image_data(image_data, output_file)

                return image_data

            except (RateLimitError, APIError, APIConnectionError) as e:
                should_retry, wait_time = self._handle_api_error(
                    e, "image generation", retry_count, max_retries
                )
                if should_retry:
                    time.sleep(wait_time)
                    retry_count += 1
                else:
                    break
            except Exception as e:
                print(f"Error generating image: {e}")
                traceback.print_exc()
                break

        return None

    def transform_reference_image(
        self,
        reference_image_path,
        body_type,
        skin_color,
        description=None,
        output_file=None,
        fabric_detail_image=None,
        framing="full",
        tux_instructions=None,
    ):
        """
        Transform a reference image directly to change body type and skin color while keeping
        everything else the same (clothing, pose, lighting, background, etc.).

        Args:
            reference_image_path (str): Path to the reference image
            body_type (str): The target body type name
            skin_color (str): The target skin color
            description (str, optional): Additional description for the body type
            output_file (str, optional): Path to save the generated image
            fabric_detail_image (str, optional): Path to fabric detail image to include
            framing (str): The framing option ('full' for full body or 'knee' for knee-length)

        Returns:
            bytes: Image data in binary format
        """
        max_retries = 3
        retry_count = 0

        try:
            print(
                f"Transforming reference image to {body_type} body type with {skin_color} skin..."
            )
            print(
                f"Framing: {'Full body' if framing == 'full' else 'Knee-length (2/3 body)'}"
            )

            # If fabric_detail_image is None but class is set to use fabric details, don't use it
            # If fabric_detail_image is provided, use it regardless of class setting
            if fabric_detail_image:
                print(
                    f"Including fabric detail image: {os.path.basename(fabric_detail_image)}"
                )
            elif not self.use_fabric_details:
                fabric_detail_image = (
                    None  # Ensure it's None if we're not using fabric details
                )

            # Find the body type dictionary from MALE_BODY_TYPES
            body_type_info = next(
                (bt for bt in MALE_BODY_TYPES if bt["name"] == body_type), None
            )
            body_description = (
                body_type_info["description"]
                if body_type_info
                else f"{body_type} body type"
            )

            # Get detailed skin color description
            skin_color_details = self._get_detailed_skin_description(skin_color)

            # Create a detailed combined description if one isn't provided
            if not description:
                if body_type_info:
                    description = f"{body_type_info['description']} with {skin_color} skin tone: {skin_color_details}"
                else:
                    description = f"{body_type} body type with {skin_color} skin tone: {skin_color_details}"

            # Get an appropriate pose for this body type and skin color
            pose_description = get_pose_for_body_and_skin(body_type, skin_color)

            # Create a highly specific transformation prompt based on framing
            base_transform_prompt = (
                self.full_body_transform_prompt
                if framing == "full"
                else self.knee_length_transform_prompt
            )

            transform_prompt = f"""{base_transform_prompt}

CHANGE TO THIS SPECIFIC POSE:
{pose_description}

CHANGE TO THIS SPECIFIC BODY TYPE AND SKIN COLOR:
- Body type: {body_type}
- Body details: {body_description}
- Skin color: {skin_color}
- Skin color details: {skin_color_details}

FACIAL EXPRESSION:
- The model MUST have a WARM, GENUINE SMILE
- Eyes should be slightly crinkled at corners to show authenticity
- Natural, approachable expression
- Teeth showing slightly in a friendly manner
- Relaxed, confident demeanor

CRITICAL INSTRUCTIONS For Tux and Vest , Pocket and Lapel Details, etc. APPLY THESE EXACTLY and CAREFULLY and CONSISTENTLY:
{tux_instructions}"""

            # Add fabric detail instructions if fabric detail image is provided
            if fabric_detail_image:
                fabric_detail_prompt = """
FABRIC DETAILS (CRITICAL - REFER TO REFERENCE IMAGE):
- ⚠️ CAREFULLY EXAMINE the fabric detail image provided as the  reference image
- PRECISELY replicate all fabric textures, patterns, weaves, and material properties shown in the detail image
- MATCH the exact fabric appearance including color variations, sheen, and surface characteristics
- ENSURE all seams, stitching, buttons, and hardware elements are accurately recreated
- REPRODUCE any fabric-specific qualities like wrinkle patterns, drape, or stretch characteristics
- MAINTAIN the exact same fabric thickness and weight appearance as shown in the detail image
- APPLY these fabric details consistently across the entire garment
- The fabric detail image shows the TRUE, HIGH-FIDELITY representation of how the fabric should appear
"""
                transform_prompt += fabric_detail_prompt

            transform_prompt += f"""
This is for fashion e-commerce website, so the product appearance must be perfectly preserved with the only change being the model's body type, skin color, pose, and smiling expression.

Add proper lighting and SHADOWS to the image to make it look realistic using the background setting from the pose description

NOTE: Main the exact COLORS and TEXTURE of the tux and vest, pocket and lapel details, etc. apply the critical instructions for tux and vest, pocket and lapel details, etc. exactly and carefully and consistently as stated above shown in the detail image
and don't add any additional items like sunglasses, hats, etc."""

            # Log the transformation prompt for debugging
            self._log_prompt(
                f"DIRECT TRANSFORM PROMPT ({body_type}, {skin_color})", transform_prompt
            )

            # Process with retry logic for API errors
            while retry_count <= max_retries:
                try:
                    if fabric_detail_image:
                        # Open both reference images and apply the transformation
                        images = []
                        with open(reference_image_path, "rb") as ref_file:
                            images.append(ref_file)
                            with open(fabric_detail_image, "rb") as fabric_file:
                                images.append(fabric_file)

                                transform_response = self.client.images.edit(
                                    model=IMAGE_MODEL,
                                    image=images,  # Pass both images as a list
                                    prompt=transform_prompt,
                                    size=DEFAULT_IMAGE_SIZE,
                                    quality=self.image_quality,
                                )
                    else:
                        # Open reference image only and apply the transformation
                        with open(reference_image_path, "rb") as ref_file:
                            transform_response = self.client.images.edit(
                                model=IMAGE_MODEL,
                                image=ref_file,  # Single image doesn't need to be in a list
                                prompt=transform_prompt,
                                size=DEFAULT_IMAGE_SIZE,
                                quality=self.image_quality,
                            )

                    # Process and save the result
                    transform_image_data = decode_base64_image(
                        transform_response.data[0].b64_json
                    )

                    if output_file:
                        # Ensure output directory exists
                        output_dir = os.path.dirname(output_file)
                        ensure_directory_exists(output_dir)

                        save_image_data(transform_image_data, output_file)
                        print(f"Transformed image saved to {output_file}")

                    # Add a 5-second wait time after each direct transformation
                    print(f"Waiting 5 seconds before proceeding to next generation...")
                    time.sleep(30)

                    return transform_image_data

                except (RateLimitError, APIError, APIConnectionError) as e:
                    should_retry, wait_time = self._handle_api_error(
                        e, "direct transformation", retry_count, max_retries
                    )
                    if should_retry:
                        time.sleep(wait_time)
                        retry_count += 1
                    else:
                        raise e

        except Exception as e:
            print(f"Error in transform_reference_image: {e}")
            traceback.print_exc()
            return None

    def generate_body_variation(
        self,
        body_type,
        skin_color,
        output_file=None,
        framing="full",
        tux_instructions=None,
    ):
        """
        Generate a base body image with a specific body type and skin color.

        Args:
            body_type (str): Body type to generate (e.g., 'slim', 'athletic', etc.)
            skin_color (str): Skin color to generate (e.g., 'light', 'medium', 'dark', etc.)
            output_file (str, optional): Path to save the generated image
            framing (str): The framing option ('full' for full body or 'knee' for knee-length)

        Returns:
            str: Path to the generated image or None if generation failed
        """
        try:
            # Get body type description
            body_type_info = next(
                (bt for bt in MALE_BODY_TYPES if bt["name"] == body_type), None
            )
            body_description = (
                body_type_info["description"]
                if body_type_info
                else f"{body_type} body type"
            )

            # Get detailed skin color description
            skin_color_details = self._get_detailed_skin_description(skin_color)

            # Get an appropriate pose for this body type and skin color
            pose_description = get_pose_for_body_and_skin(body_type, skin_color)

            # Select the appropriate body prompt based on framing
            base_body_prompt = (
                self.full_body_prompt if framing == "full" else self.knee_length_prompt
            )

            # Create the base body prompt with detailed descriptions
            prompt = f"""{base_body_prompt}

BODY TYPE: {body_type}
BODY TYPE DETAILS: {body_description}

SKIN COLOR: {skin_color}
SKIN COLOR DETAILS: {skin_color_details}

FACIAL EXPRESSION:
- The model MUST have a WARM, GENUINE SMILE
- Eyes should be slightly crinkled at corners to show authenticity
- Natural, approachable expression
- Teeth showing slightly in a friendly manner
- Relaxed, confident demeanor

POSE INSTRUCTIONS:
{pose_description}

SPECIFIC INSTRUCTIONS For Tux:
{tux_instructions}"""

            # Log the body prompt for debugging
            self._log_prompt(f"BODY GENERATION ({body_type}, {skin_color})", prompt)

            # Generate the image with the specified body type and skin color
            if output_file:
                self._generate_image_with_prompt(prompt, output_file)
                return output_file
            else:
                # Generate a temp file if no output path provided
                temp_output = os.path.join(
                    TEMP_DIR, f"temp_body_{body_type}_{skin_color}.jpg"
                )
                ensure_directory_exists(os.path.dirname(temp_output))
                self._generate_image_with_prompt(prompt, temp_output)
                return temp_output

        except Exception as e:
            print(f"Error generating body variation: {e}")
            traceback.print_exc()
            return None

    def generate_variation_with_reference(
        self,
        reference_image_path,
        body_type,
        description,
        output_file=None,
        use_base_library=False,
        base_bodies_dir=None,
        fabric_detail_image=None,
        framing="full",
        tux_instructions=None,
    ):
        """
        Generate a variation of a reference image with a specified body type and description.
        This uses a two-step process:
        1. Generate a base body image with the specified body type
        2. Apply the outfit from the reference image to the base body

        Args:
            reference_image_path (str): Path to the reference image
            body_type (str): The body type to use for generation
            description (str): Description of the body type and skin color
            output_file (str, optional): Path to save the generated image
            use_base_library (bool): Whether to use pre-generated base body images
            base_bodies_dir (str, optional): Directory containing pre-generated base bodies
            fabric_detail_image (str, optional): Path to a fabric detail image to include
            framing (str): The framing option ('full' for full body or 'knee' for knee-length)

        Returns:
            str: Path to the generated image
        """
        try:
            print(
                f"Generating variation with reference {os.path.basename(reference_image_path)}..."
            )
            print(
                f"Framing: {'Full body' if framing == 'full' else 'Knee-length (2/3 body)'}"
            )

            # Check if fabric detail image should be used
            use_fabric = False
            if fabric_detail_image and (
                self.use_fabric_details or fabric_detail_image is not None
            ):
                use_fabric = True
                print(
                    f"Including fabric detail image: {os.path.basename(fabric_detail_image)}"
                )

            # Extract skin color from description using regex
            skin_color_match = re.search(
                r"(\w+)\s+skin\s+tone", description, re.IGNORECASE
            )
            skin_color = (
                skin_color_match.group(1).lower() if skin_color_match else "light"
            )

            # Get detailed skin color description
            skin_color_details = self._get_detailed_skin_description(skin_color)

            # Get body type information
            body_type_info = next(
                (bt for bt in MALE_BODY_TYPES if bt["name"] == body_type), None
            )
            body_description = (
                body_type_info["description"]
                if body_type_info
                else f"{body_type} body type"
            )

            # Get a pose description for this body type and skin color
            pose_description = get_pose_for_body_and_skin(body_type, skin_color)

            # Use pre-generated base body if available and requested
            base_body_path = None
            if use_base_library and base_bodies_dir:
                # Check if there's a pre-generated base body image for this combination
                base_body_pattern = f"*{body_type}*{skin_color}*.jpg"
                base_body_search_path = os.path.join(base_bodies_dir, base_body_pattern)
                matching_files = glob.glob(base_body_search_path)

                if matching_files:
                    base_body_path = matching_files[0]  # Use the first matching file
                    print(
                        f"Using pre-generated base body: {os.path.basename(base_body_path)}"
                    )
                else:
                    print(
                        f"No pre-generated base body found for {body_type} with {skin_color} skin tone"
                    )

            # Generate a base body if needed
            if not base_body_path:
                print(
                    f"Generating base body with {body_type} body type and {skin_color} skin tone..."
                )
                # Create a temporary file for the base body
                temp_dir = (
                    os.path.join(os.path.dirname(output_file), "temp")
                    if output_file
                    else TEMP_DIR
                )
                ensure_directory_exists(temp_dir)

                base_body_path = os.path.join(
                    temp_dir, f"base_body_{body_type}_{skin_color}.jpg"
                )

                # Generate the base body image
                self.generate_body_variation(
                    body_type,
                    skin_color,
                    base_body_path,
                    framing=framing,
                    tux_instructions=tux_instructions,
                )

            # Step 2: Apply the outfit from the reference image to the base body
            print(f"Applying outfit from reference image to the base body...")

            # Create transform prompt with pose and detailed skin color
            base_transform_prompt = (
                self.full_body_transform_prompt
                if framing == "full"
                else self.knee_length_transform_prompt
            )

            transform_prompt = f"""{base_transform_prompt}

BODY TYPE: {body_type}
BODY TYPE DETAILS: {body_description}

SKIN COLOR: {skin_color}
SKIN COLOR DETAILS: {skin_color_details}

FACIAL EXPRESSION:
- The model MUST have a WARM, GENUINE SMILE
- Eyes should be slightly crinkled at corners to show authenticity
- Natural, approachable expression
- Teeth showing slightly in a friendly manner
- Relaxed, confident demeanor

POSE INSTRUCTIONS:
{pose_description}"""

            # Log the transform prompt for debugging
            self._log_prompt(
                f"TWO-STEP TRANSFORM ({body_type}, {skin_color})", transform_prompt
            )

            # Transform the base body with the reference image
            self._transform_image_with_reference(
                base_image_path=base_body_path,
                reference_image_path=reference_image_path,
                prompt=transform_prompt,
                output_file=output_file,
                fabric_detail_image=fabric_detail_image if use_fabric else None,
            )

            return output_file

        except Exception as e:
            print(f"Error in generate_variation_with_reference: {e}")
            traceback.print_exc()
            return None

    def _generate_image_with_prompt(
        self, prompt, output_file, size=DEFAULT_IMAGE_SIZE, quality=None
    ):
        """
        Helper method to generate an image using a prompt and save it to a file.

        Args:
            prompt (str): The generation prompt
            output_file (str): Path to save the generated image
            size (str): Image size
            quality (str): Image quality, defaults to self.image_quality

        Returns:
            bytes: Image data or None if generation failed
        """
        if quality is None:
            quality = self.image_quality

        try:
            # Log the prompt for debugging
            self._log_prompt("GENERATE IMAGE PROMPT", prompt)

            # Generate the image
            response = self.client.images.generate(
                model=IMAGE_MODEL,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
            )

            # Get the first image from the response
            image = response.data[0]

            # GPT Image model always returns base64 data
            image_data = decode_base64_image(image.b64_json)

            # Save the image
            save_image_data(image_data, output_file)

            return image_data

        except Exception as e:
            print(f"Error in _generate_image_with_prompt: {e}")
            traceback.print_exc()
            raise

    def _transform_image_with_reference(
        self,
        base_image_path,
        reference_image_path,
        prompt,
        output_file,
        fabric_detail_image=None,
    ):
        """
        Helper method to transform an image using a base image and a reference image.

        Args:
            base_image_path (str): Path to the base image
            reference_image_path (str): Path to the reference image
            prompt (str): The transformation prompt
            output_file (str): Path to save the transformed image
            fabric_detail_image (str, optional): Path to fabric detail image to include

        Returns:
            bytes: Image data or None if transformation failed
        """
        try:
            # Log the prompt for debugging
            self._log_prompt("TRANSFORM IMAGE PROMPT", prompt)

            # Add fabric detail instructions if fabric detail image is provided
            if fabric_detail_image:
                fabric_detail_prompt = """
FABRIC DETAILS (CRITICAL - REFER TO THIRD REFERENCE IMAGE):
- ⚠️ CAREFULLY EXAMINE the fabric detail image provided as the third reference
- PRECISELY replicate all fabric textures, patterns, weaves, and material properties shown
- MATCH the exact fabric appearance including color variations, sheen, and surface characteristics
- ENSURE all seams, stitching, buttons, and hardware elements are accurately recreated
- REPRODUCE any fabric-specific qualities like wrinkle patterns, drape, or stretch characteristics
- MAINTAIN the exact same fabric thickness and weight appearance as shown in the detail image
- APPLY these fabric details consistently across the entire garment
"""
                prompt += fabric_detail_prompt
                self._log_prompt("FABRIC DETAIL ADDITION", fabric_detail_prompt)

            # Open images for the transformation
            if fabric_detail_image:
                # Open all three images
                with open(base_image_path, "rb") as base_file, open(
                    reference_image_path, "rb"
                ) as ref_file, open(fabric_detail_image, "rb") as fabric_file:
                    # Apply the transformation with all three images
                    response = self.client.images.edit(
                        model=IMAGE_MODEL,
                        image=[
                            base_file,
                            ref_file,
                            fabric_file,
                        ],  # Pass all three images as a list
                        prompt=prompt,
                        quality=self.image_quality,
                    )
            else:
                # Open both images for the transformation
                with open(base_image_path, "rb") as base_file, open(
                    reference_image_path, "rb"
                ) as ref_file:
                    # Apply the transformation
                    response = self.client.images.edit(
                        model=IMAGE_MODEL,
                        image=[base_file, ref_file],  # Pass both images as a list
                        prompt=prompt,
                        quality=self.image_quality,
                    )

            # Get the first image from the response
            image = response.data[0]

            # GPT Image model always returns base64 data
            image_data = decode_base64_image(image.b64_json)

            # Ensure output directory exists
            output_dir = os.path.dirname(output_file)
            ensure_directory_exists(output_dir)

            # Save the image
            save_image_data(image_data, output_file)

            return image_data

        except Exception as e:
            print(f"Error in _transform_image_with_reference: {e}")
            traceback.print_exc()
            raise

    def generate_base_body_library(
        self,
        output_dir,
        body_types=None,
        skin_colors=None,
        poses_per_combination=1,
        image_quality=None,
    ):
        """
        Generate a library of base body images with different combinations of body types,
        skin colors, and poses. These can be used later as base images for outfit application.

        Args:
            output_dir (str): Directory to save the generated base body images
            body_types (list, optional): List of body types to generate. If None, uses all from MALE_BODY_TYPES
            skin_colors (list, optional): List of skin colors to generate. If None, uses a default set
            poses_per_combination (int): Number of different poses to generate for each body type + skin color combination
            image_quality (str, optional): Quality of generated images (high, medium, or low)

        Returns:
            dict: Dictionary mapping body type and skin color combinations to generated image paths
        """
        # Use the provided image quality or the default from the instance
        if image_quality is not None:
            # Temporarily save the current quality
            original_quality = self.image_quality
            self.image_quality = image_quality

        try:
            # Create output directory if it doesn't exist
            ensure_directory_exists(output_dir)

            # Define default skin colors if not provided
            if skin_colors is None:
                skin_colors = [
                    "fair",
                    "light",
                    "medium",
                    "olive",
                    "tan",
                    "brown",
                    "dark",
                ]

            # Define body types if not provided (use names from MALE_BODY_TYPES)
            if body_types is None:
                body_types = [bt["name"] for bt in MALE_BODY_TYPES]

            # Dictionary to track generated images
            generated_images = {}

            # Generate each combination
            total_combinations = (
                len(body_types) * len(skin_colors) * poses_per_combination
            )
            count = 0

            print(f"Generating {total_combinations} base body images...")
            print(f"- Body types: {len(body_types)}")
            print(f"- Skin colors: {len(skin_colors)}")
            print(f"- Poses per combination: {poses_per_combination}")

            # Create progress bar
            progress_bar = tqdm(
                total=total_combinations, desc="Generating base bodies", unit="image"
            )

            for body_type in body_types:
                # Find the body type dictionary from MALE_BODY_TYPES
                body_type_info = next(
                    (bt for bt in MALE_BODY_TYPES if bt["name"] == body_type), None
                )

                if not body_type_info:
                    print(
                        f"Warning: No information found for body type {body_type}, skipping..."
                    )
                    continue

                for skin_color in skin_colors:
                    # Create a subdirectory for this body type and skin color
                    combination_dir = os.path.join(
                        output_dir, f"{body_type}_{skin_color}"
                    )
                    ensure_directory_exists(combination_dir)

                    # Track generated images for this combination
                    combination_images = []

                    for pose_index in range(poses_per_combination):
                        count += 1
                        print(
                            f"\nGenerating image {count}/{total_combinations}: {body_type} with {skin_color} skin (pose {pose_index+1})..."
                        )

                        # Create filename
                        filename = (
                            f"base_body_{body_type}_{skin_color}_pose{pose_index+1}.jpg"
                        )
                        output_file = os.path.join(combination_dir, filename)

                        # Skip if file already exists
                        if os.path.exists(output_file):
                            print(f"Image already exists: {output_file}")
                            combination_images.append(output_file)
                            continue

                        # Create description and generate the image
                        description = f"{body_type_info['description']} with {skin_color} skin tone"

                        try:
                            # Generate the base body image
                            print("Generating base body image...")
                            body_response = self.client.images.generate(
                                model=IMAGE_MODEL,
                                prompt=body_prompt,
                                size=DEFAULT_IMAGE_SIZE,
                                quality=self.image_quality,
                                n=1,
                            )
                            combination_images.append(output_file)

                            # Update progress bar
                            progress_bar.update(1)

                        except Exception as e:
                            print(
                                f"Error generating {body_type} with {skin_color} skin: {e}"
                            )
                            traceback.print_exc()
                            # Still update progress bar on error
                            progress_bar.update(1)

                    # Add the images to the dictionary
                    key = f"{body_type}_{skin_color}"
                    generated_images[key] = combination_images

            # Close progress bar
            progress_bar.close()

            print(f"\nGenerated {count} base body images.")
            return generated_images

        except Exception as e:
            print(f"Error in generate_base_body_library: {e}")
            traceback.print_exc()
            return {}
        finally:
            # Restore the original quality if it was changed
            if image_quality is not None:
                self.image_quality = original_quality

    def _get_detailed_skin_description(self, skin_color):
        """
        Get a detailed description for a skin color.

        Args:
            skin_color (str): The skin color name (e.g., 'light', 'medium', 'dark')

        Returns:
            str: Detailed description of the skin color
        """
        # Dictionary of detailed skin color descriptions
        skin_descriptions = {
            "porcelain": "Nearly translucent, very-fair skin with cool pink-or-peach hue; freckles possible",
            "fair-light": "Light but less translucent skin with neutral to soft peach warmth",
            "light-beige": "Light-medium beige skin with subtle golden warmth; tans slowly",
            "medium": "True medium depth skin with balanced golden glow and even tone",
            "olive": "Medium skin with green-yellow cast; rarely burns",
            "tan": "Warm tan to light-brown skin with golden or reddish warmth; tans easily",
            "brown": "Medium-deep brown skin with rich red-brown warmth and smooth tone",
            "deep": "Very deep brown to ebony skin with cool blue-red lowlights and high melanin. Fitzpatrick VI.",
        }

        # Return the detailed description or a generic one if not found
        return skin_descriptions.get(
            skin_color.lower(), f"{skin_color} skin tone with natural undertones"
        )

    def find_fabric_detail_image(self, product_code, fabric_details_dir):
        """
        Find a fabric detail image for a given product code.

        Args:
            product_code (str): The product code to find fabric details for
            fabric_details_dir (str): Directory containing fabric detail images

        Returns:
            str: Path to the fabric detail image or None if not found
        """
        if not self.use_fabric_details or not fabric_details_dir:
            return None

        # Check if directory exists
        if not os.path.exists(fabric_details_dir):
            print(f"Fabric details directory not found: {fabric_details_dir}")
            return None

        # Look for fabric detail image with pattern: PRODUCT_CODE*_FABRIC*.jpg
        pattern = os.path.join(fabric_details_dir, f"{product_code}*_FABRIC*.jpg")
        fabric_images = glob.glob(pattern)

        # Also try with just the product code in any format
        if not fabric_images:
            pattern = os.path.join(fabric_details_dir, f"{product_code}*.jpg")
            fabric_images = glob.glob(pattern)

        if fabric_images:
            print(f"Found fabric detail image: {os.path.basename(fabric_images[0])}")
            return fabric_images[0]
        else:
            print(f"No fabric detail image found for product {product_code}")
            return None
