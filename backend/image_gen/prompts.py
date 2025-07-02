# image_gen/prompts.py

"""
Prompt templates for image generation.
"""

# JORDAN HOODIE UPPER BODY PROMPT (for all body types/skin colors)
BODY_GENERATION_TEMPLATE = '''Create a professional fashion photo of the upper body of an overweight olive-skinned male model with the specified body type and description.
CRITICAL FRAMING REQUIREMENTS - MUST FOLLOW EXACTLY:
OUTPUT MUST BE AN UPPER BODY IMAGE ONLY: from top of head (including ALL hair) to just below the waist
The model's head and upper torso must be fully visible and clearly framed
Divide the frame into a 3x3 grid
Subject's head MUST be centered in the middle square of the top row
There MUST be a FULL empty grid square (33% of frame height) above the head
Subject's torso should span the middle column
No cropping of hair, head, shoulders, or upper chest
CAMERA SETUP AND POSITION:
Camera at chest height (about 4.5 feet / 137cm from ground)
Straight-on or slight upward tilt (5–10 degrees)
Framed to include subject from head to just below waist
Focal length: 85mm equivalent for natural proportions
Portrait orientation (4:5 ratio)
POSE SELECTION:
Model is standing naturally and facing the camera on a city sidewalk
Arms relaxed at sides or lightly interacting with the hoodie (e.g., adjusting sleeve or pocket)
Face clearly visible, neutral or confident expression
Posture must appear natural and grounded
BACKGROUND AND LIGHTING:
Outdoor urban sidewalk setting in New York City
Include elements such as concrete pavement, curb, red-brick buildings, or storefronts in soft focus
Use bright diffused daylight (e.g., overcast or golden hour)
Ensure realistic lighting and shadows on model
Urban NYC ambiance must be visible but not distracting
CLOTHING:
Bright red Jordan hoodie with white Jumpman logo on the chest
Hoodie must be worn naturally and untucked
Match the exact red color, tone, and fabric texture of the reference hoodie in the uploaded image (RGB approximation: #C70024)
The red must be rich, vibrant, and consistent — avoid pink, maroon, or muted reds
No visible branding or accessories beyond the hoodie
TECHNICAL SPECIFICATIONS:
8k quality
Hyperrealistic
Photorealistic
Sharp focus on face and garment details
No motion blur
Urban sidewalk textures and lighting must be consistent with real-world photography
Subject must stand out clearly from the background
FINAL CHECKS - MUST VERIFY ALL:
HEAD POSITION:
Head in middle square of top row
Full empty grid square (33%) above head
No part of head/hair touches top third of frame
BODY FRAMING:
Upper body fully visible down to below waist
No cropping of hair, shoulders, or chest
Subject centered in middle column
POSE AND STYLE:
Pose matches the specific instructions
Face clearly visible and expressive
Hoodie clearly visible and well-lit
TECHNICAL:
Sharp focus throughout
Proper natural lighting
Urban NYC sidewalk setting is clear
Exact red hoodie color and fabric match is mandatory'''

# Template for applying outfit
OUTFIT_APPLICATION_TEMPLATE = """Create a photorealistic image of the man wearing the complete outfit from the reference photo.
Maintain the exact same pose and facial features of the base image.
Keep the professional studio lighting and add proper lighting and SHADOWS to the image to make it look realistic"""

# Template for pose category options
POSE_CATEGORY_TEMPLATE = """Professional Standing Poses (select if random number 1-3):
- Standing tall with hands at sides, professional stance, clear face visible
- One hand casually in pocket, other at side, confident pose, direct gaze
- Hands clasped in front, professional stance, engaging camera directly
- One hand in pocket, other hand at collar, strong presence, clear face
- Standing straight, both hands adjusting shirt, face to camera
- One hand adjusting collar, other at side, direct eye contact
- Standing with hands behind back, confident posture, face forward
- Both hands adjusting cuffs, commanding presence, clear facial features

Dynamic Standing Poses (select if random number 4-6):
- Both hands at sides, shoulders back, power stance, direct gaze
- One hand adjusting watch, other at side, looking at camera
- Hands at hips, confident executive pose, face clearly visible
- Standing with subtle contrapposto, one hand at shirt button, face forward
- One hand adjusting collar, other relaxed, direct eye contact
- Both hands subtly adjusting cuffs, face to camera
- Standing with one hand smoothing shirt, clear facial features
- Classic male model pose, hands framing torso, face forward
- Power pose with hands positioned naturally, engaging camera

Editorial Poses (select if random number 7-9):
- Looking directly at camera, one hand at chin, full face visible
- Strong stance with subtle head tilt, engaging eyes to camera
- One hand adjusting collar, direct camera engagement
- Modern power pose, hands framing torso, face forward
- Classic fashion stance, hands at natural position, clear face
- Contemporary pose with hands at sides, strong camera presence
- Bold stance with hands positioned naturally, direct gaze
- Fashion-forward pose, adjusting sleeve, face to camera
- Confident pose with hands subtly positioned, clear facial features
- Strong editorial stance, engaging directly with camera"""

ARCTICFOX_BODY_GENERATION_TEMPLATE = """
Create a full-body professional fashion photo of a male model with the specified body type and description.

CRITICAL FRAMING REQUIREMENTS - MUST FOLLOW EXACTLY:
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
- Poses should be appropriate for a winter outdoor fashion setting (e.g., leaning against a wooden ski resort fence, standing in front of a chalet, walking in snow, etc.)
- Face must be oriented toward the camera with a confident, professional expression

BACKGROUND AND LIGHTING:
- Outdoor winter setting with snow-covered ground and trees, bright diffused daylight
- Background should include a ski chalet, wooden fence, or alpine scenery
- Add proper lighting and SHADOWS to the image to make it look realistic using the background setting from the pose description
- Professional fashion photography lighting

CLOTHING:
- Beige quarter-zip pullover sweater (main garment)
- Garment must be UNTUCKED and hang naturally outside pants
- Exact color and texture of the sweater must be preserved
- No additional clothing items unless specified

TECHNICAL SPECIFICATIONS:
- 8k quality
- Hyperrealistic
- Photorealistic
- Sharp focus throughout
- No motion blur
- Snow textures must be rendered clearly
- Subject must stand out against the winter background

FINAL CHECKS - MUST VERIFY ALL:
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
   - Snow and winter setting are clear
CRITICAL: If ANY of these checks fail, the image must be regenerated.
"""

HEATHER_BODY_GENERATION_TEMPLATE = ARCTICFOX_BODY_GENERATION_TEMPLATE
BLACK_BODY_GENERATION_TEMPLATE = ARCTICFOX_BODY_GENERATION_TEMPLATE

def get_body_generation_prompt(body_type, description):
    """
    Generate a body generation prompt.

    Args:
        body_type (str): Type of body
        description (str): Description of the body type

    Returns:
        str: Formatted prompt
    """
    return BODY_GENERATION_TEMPLATE.format(
        body_type=body_type,
        description=description,
        pose_options=POSE_CATEGORY_TEMPLATE,
    )


def get_outfit_application_prompt():
    """
    Get the outfit application prompt.

    Returns:
        str: Prompt for applying outfit
    """
    return OUTFIT_APPLICATION_TEMPLATE

def get_arcticfox_body_generation_prompt(body_type, description):
    return ARCTICFOX_BODY_GENERATION_TEMPLATE.format(
        body_type=body_type,
        description=description,
    )

def get_heather_body_generation_prompt(body_type, description):
    """Get the prompt for generating a body image with the Heather Grey template."""
    return HEATHER_BODY_GENERATION_TEMPLATE.format(
        body_type=body_type,
        description=description
    )

def get_black_body_generation_prompt(body_type, description):
    """Get the prompt for generating a body image with the Black template."""
    return BLACK_BODY_GENERATION_TEMPLATE.format(
        body_type=body_type,
        description=description
    )
