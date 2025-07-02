from dotenv import load_dotenv
load_dotenv()
import os
print("OPENAI_API_KEY loaded:", os.getenv("OPENAI_API_KEY"))
from image_gen.image_generator import ImageGenerator
from image_gen.models import MALE_BODY_TYPES

# List of skin colors to generate
SKIN_COLORS = [
    "fair-light",
    "olive",
    "brown",
    "dark-brown",
]

REFERENCE_IMAGE = os.path.abspath("jordan_red_hoodie_reference.png")

# Updated, brighter red hoodie prompt, explicitly referencing the attached image
BRIGHTER_RED_HOODIE_PROMPT = (
    "Create a professional fashion photo of a male model with the specified body type and skin color, using the attached reference image for the exact hoodie style, fit, Jumpman logo placement, and a brighter red color that closely matches RGB: #C70024 (a rich, vibrant scarlet red).\n"
    "\nCRITICAL FRAMING REQUIREMENTS — MUST FOLLOW EXACTLY:\n"
    "\nOUTPUT MUST BE A THREE-QUARTER SHOT: from the top of the head (including ALL hair) to just below the hips\n"
    "\nThe model's entire head, hair, and hoodie (including bottom hem and both sleeves) must be fully visible and uncropped\n"
    "\nDo not crop, blur, or hide any part of the hoodie\n"
    "\nThe white Jumpman logo on the chest must be clearly visible, centered, unobstructed, and accurately shaped and positioned as in the reference\n"
    "\nThe entire front panel of the hoodie must be well lit and clearly visible\n"
    "\nLeave a 5–10% margin around all sides to prevent accidental cropping\n"
    "\nGRID AND LAYOUT REQUIREMENTS:\n"
    "\nDivide the frame into a 3x3 grid\n"
    "\nSubject's head must be centered in the middle square of the top row\n"
    "\nThere must be a full empty grid square (33% of frame height) above the head\n"
    "\nSubject's torso must fully occupy the middle column\n"
    "\nHoodie hem and sleeves must be completely inside the frame, not touching any edges\n"
    "\nCAMERA SETUP AND POSITION:\n"
    "\nCamera at chest height (~4.5 feet / 137 cm from ground)\n"
    "\nUse a slight upward tilt (5–10 degrees) or level angle\n"
    "\nFocal length: 85mm equivalent\n"
    "\nOrientation: Portrait (4:5)\n"
    "\nShow from top of the head to just below the hips\n"
    "\nPOSE AND STYLING:\n"
    "\nModel standing naturally, facing the camera, in a relaxed, confident pose\n"
    "\nArms at sides or lightly adjusting pocket/sleeve\n"
    "\nExpression: neutral or confident\n"
    "\nFace must be clearly visible, not obstructed\n"
    "\nBACKGROUND AND LIGHTING:\n"
    "\nOutdoor urban sidewalk in New York City\n"
    "\nInclude soft-focus elements: red-brick buildings, storefronts, concrete pavement\n"
    "\nUse natural daylight (overcast or golden hour)\n"
    "\nLighting must be bright, evenly diffused, with natural shadows and clear subject-background separation\n"
    "\nCLOTHING SPECIFICATIONS:\n"
    "\nBright red Jordan hoodie matching RGB: #C70024\n"
    "\nWhite Jumpman logo on the chest, sharp and centered\n"
    "\nHoodie must be worn naturally, untucked, no fabric distortion\n"
    "\nNo extra branding or accessories\n"
    "\nTECHNICAL REQUIREMENTS:\n"
    "\n8K resolution, hyperrealistic and photorealistic\n"
    "\nSharp focus on face and hoodie\n"
    "\nNo motion blur\n"
    "\nNatural lighting and accurate color reproduction\n"
    "\nSubject must be separated cleanly from background\n"
)

# Output directory root
OUTPUT_ROOT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "frontend",
    "public",
    "images",
    "bodytypes",
    "headswapper"
)

if __name__ == "__main__":
    image_gen = ImageGenerator(debug=True, use_fabric_details=True)
    image_gen.image_quality = "medium"

    for body_type_obj in MALE_BODY_TYPES:
        body_type = body_type_obj["name"]
        body_type_dir = os.path.join(OUTPUT_ROOT, body_type)
        os.makedirs(body_type_dir, exist_ok=True)

        for skin_color in SKIN_COLORS:
            output_filename = f"jordan_red_hoodie_reference_{skin_color}.png"
            output_path = os.path.join(body_type_dir, output_filename)

            print(f"\n=== Generating: {body_type} / {skin_color} ===")
            print(f"Output: {output_path}")

            # Use the new prompt as the description
            image_gen.transform_reference_image(
                reference_image_path=REFERENCE_IMAGE,
                body_type=body_type,
                skin_color=skin_color,
                description=BRIGHTER_RED_HOODIE_PROMPT,
                output_file=output_path,
                framing="full"
            )
            print(f"✅ Saved: {output_path}") 