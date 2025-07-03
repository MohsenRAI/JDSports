import os
import base64
import json
from PIL import Image
from openai import OpenAI
from io import BytesIO
from dotenv import load_dotenv
from flask_cors import CORS
import requests
from flask import send_from_directory
import traceback
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
)

# Set Flask log level to DEBUG
import flask
flask.logging.create_logger = lambda app: logging.getLogger('flask.app')

# Load environment variables
load_dotenv()

# Skin color normalization mapping
NORMALIZE_SKIN = {
    "light": "fair-light",
    "fair": "fair-light",
    "pale": "fair-light",
    "fair-light": "fair-light",
    "medium": "olive",
    "olive": "olive",
    "brown": "brown",
    "medium-brown": "brown",
    "dark": "dark-brown",
    "dark-brown": "dark-brown",
}

# Body type descriptions
BASE_BODY_TYPES = [
    {
        "name": "slim",
        "base_description": "Slim build with lean frame, 5'11\" tall. Naturally thin physique with long limbs and lighter muscle definition. Narrow shoulders and slim waist. Defined facial features with high cheekbones and angular jawline.",
    },
    {
        "name": "average",
        "base_description": "Average build with typical proportions, 5'10\" tall. Balanced frame with moderate shoulder width and natural body composition. Neither particularly muscular nor slim. Friendly, approachable facial features with warm expression.",
    },
    {
        "name": "athletic",
        "base_description": "Athletic build with balanced muscle definition, 5'11\" tall. Well-proportioned with broad shoulders, defined chest, and tapered waist. Natural muscle tone without being overly bulky. Classic handsome features with defined jawline.",
    },
    {
        "name": "muscular",
        "base_description": "Muscular build with strong physique, 6'0\" tall. Broad shoulders, well-developed chest, and visible muscle mass. Powerful frame with defined musculature. Strong facial features with masculine jawline and confident expression.",
    },
    {
        "name": "stocky",
        "base_description": "Stocky build with solid frame, 5'9\" tall. Broader, heavier set physique with strong core and natural strength. Wider shoulders and chest with sturdy limbs. Strong facial features with rounded jawline and confident bearing.",
    },
    {
        "name": "dadbod",
        "base_description": "Comfortable dad bod physique, 5'10\" tall. Natural, relaxed build with softer midsection and broad shoulders. Strong arms with everyday muscle tone. Warm, friendly facial features with kind eyes and welcoming smile.",
    },
    {
        "name": "overweight",
        "base_description": "Overweight build with substantial frame, 5'11\" tall. Full, well-proportioned frame with natural strength. Broad shoulders and chest with substantial build. Strong facial features with confident, approachable expression.",
    },
]

SKIN_TONES = [
    {
        "name": "fair-light",
        "description": "Fair to light skin tone with pale to light complexion. Often has pink, peach, or neutral undertones. May have visible veins and burns easily in sun. Classic European, Northern European, or East Asian light complexion.",
    },
    {
        "name": "olive",
        "description": "Medium olive skin tone with green, yellow, or golden undertones. Often associated with Mediterranean, Middle Eastern, Hispanic, or mixed heritage. Naturally warm complexion that tans easily.",
    },
    {
        "name": "brown",
        "description": "Warm medium brown skin tone with golden, red, or warm undertones. Common in African American, Hispanic, Middle Eastern, South Asian, or mixed heritage individuals. Rich, healthy complexion.",
    },
    {
        "name": "dark-brown",
        "description": "Rich dark brown skin tone with deep warm undertones. Beautiful deep complexion often seen in African, African American, or South Asian heritage. Natural luminous quality with golden or red undertones.",
    },
]

BODY_TYPE_DESCRIPTIONS = "\n".join(
    [f"- {bt['name']}: {bt['base_description']}" for bt in BASE_BODY_TYPES]
)
SKIN_TONE_DESCRIPTIONS = "\n".join(
    [f"- {st['name']}: {st['description']}" for st in SKIN_TONES]
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG", quality=95)
    return base64.b64encode(buffered.getvalue()).decode()


def get_system_prompt():
    return (
        "You are an advanced image analysis AI. Your task is to identify the central person "
        "in the provided image and classify them based on the given structured schema. "
        "If no human is present or identifiable, set all attributes to 'N/A' and provide an appropriate message. "
        "If a human is present then always classify all attributes. Never set any attribute to 'N/A'. "
        "If multiple people are in the image, focus on the central character. "
        "The body types with bust size are only for female genders. "
        "The body types without bust size are only for male genders. "
        "The body type will be deduced after the gender, to ensure that the classification is correct. "
        "\nFor males, use these body types with their detailed descriptions:\n"
        f"{BODY_TYPE_DESCRIPTIONS}\n"
        "For females, use these body types: smallbust-slim, mediumbust-slim, largebust-slim, smallbust-athletic, mediumbust-athletic, largebust-athletic, "
        "smallbust-pear, mediumbust-pear, mediumbust-curvy, mediumbust-hourglass, largebust-curvy, largebust-hourglass, "
        "smallbust-topheavy, mediumbust-topheavy, largebust-topheavy, smallbust-apple, mediumbust-apple, largebust-apple, "
        "smallbust-average, mediumbust-average, largebust-average, smallbust-plus, mediumbust-plus, largebust-plus, "
        "smallbust-petite, mediumbust-petite, largebust-petite, smallbust-tall, mediumbust-tall, largebust-tall.\n"
        "\nFor skin color, use these values with their detailed descriptions:\n"
        f"{SKIN_TONE_DESCRIPTIONS}\n"
        "Return the response in this exact JSON format: "
        "{'metadata': {'gender': string, 'body_type': string, 'skin_color': string}, "
        "'success': boolean, 'message': string}"
    )


def analyze_user_image_from_bytes(image_bytes):
    logging.debug(f"DEBUG: Starting image analysis, image size: {len(image_bytes)} bytes")
    try:
        img = Image.open(BytesIO(image_bytes))
        logging.debug(f"DEBUG: Image opened successfully, size: {img.size}, mode: {img.mode}")
        width, height = img.size
        if width > 2000 or height > 2000:
            img.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
            logging.debug(f"DEBUG: Image resized to: {img.size}")
        if img.mode == "RGBA":
            img = img.convert("RGB")
            logging.debug(f"DEBUG: Image converted to RGB")
        img_base64 = image_to_base64(img)
        logging.debug(f"DEBUG: Image converted to base64, length: {len(img_base64)}")
    except Exception as e:
        logging.debug(f"DEBUG: Error in image processing: {e}")
        raise

    system_prompt = get_system_prompt()
    user_prompt = "Please analyze this image and describe the gender, body type, and skin color of the central person."

    params = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                    },
                ],
            },
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.0,
    }

    logging.debug(f"DEBUG: Calling OpenAI API with image base64 length: {len(img_base64)}")
    try:
        response = client.chat.completions.create(**params)
        logging.debug(f"DEBUG: OpenAI API call successful")
        parsed_response = json.loads(response.choices[0].message.content)
        logging.debug(f"DEBUG: Parsed response: {parsed_response}")
        sc = parsed_response["metadata"]["skin_color"].lower()
        parsed_response["metadata"]["skin_color"] = NORMALIZE_SKIN.get(sc, sc)
        logging.debug(f"DEBUG: Final response: {parsed_response}")
        return parsed_response
    except Exception as e:
        logging.debug(f"DEBUG: Error in OpenAI API call: {e}")
        raise


# --- Flask API for frontend integration ---
from flask import Flask, request, jsonify

app = Flask(__name__)

# Secure CORS configuration
CORS(
    app,
    origins=[
        "https://gazmanclone.vercel.app",
        "https://66north-jade.vercel.app",  # Add Vercel frontend domain
        "https://jd-sports.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://10.50.8.142:5173",
        "http://10.50.8.142:5174"
    ],
    supports_credentials=True,
    allow_headers=["Content-Type"],
    methods=["GET", "POST", "OPTIONS"],
)


@app.route("/")
def health_check():
    return jsonify({"status": "ok", "message": "Server is running"}), 200


@app.route("/api/analyze-user-image", methods=["POST"])
def analyze_user_image_api():
    logging.debug("DEBUG: /api/analyze-user-image endpoint called")
    logging.debug(f"DEBUG: Request method: {request.method}")
    logging.debug(f"DEBUG: Request files: {list(request.files.keys())}")
    logging.debug(f"DEBUG: Request form: {list(request.form.keys())}")
    
    if "image" not in request.files:
        logging.debug("DEBUG: No image file in request.files")
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    logging.debug(f"DEBUG: Got file: {file.filename}, content type: {file.content_type}")

    # Validate file type
    if not file.filename or not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")):
        logging.debug(f"DEBUG: Invalid file type: {file.filename}")
        return jsonify({"error": "Invalid file type. Please upload an image."}), 400

    # Read file content once
    file_content = file.read()
    
    # Validate file size (max 10MB)
    if len(file_content) > 10 * 1024 * 1024:
        return jsonify({"error": "File too large. Maximum size is 10MB."}), 400

    try:
        result = analyze_user_image_from_bytes(file_content)
        return jsonify(result)
    except Exception as e:
        # Log the actual error for debugging but don't expose it
        logging.error(f"Error in analyze_user_image_api: {e}")
        logging.error(f"Error type: {type(e).__name__}")
        import traceback
        logging.error(f"Full traceback: {traceback.format_exc()}")
        return jsonify({"error": "Internal server error. Please try again."}), 500


# Configure image directory from environment variable or use default
IMAGES_DIR = os.getenv("IMAGES_DIR", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "public", "images"))
logging.debug(f"DEBUG: IMAGES_DIR = {IMAGES_DIR}")


def get_reference_image_path(body_type, skin_color, color_prefix=None):
    return f"bodytypes/headswapper/{body_type}/jordan_red_hoodie_reference_{skin_color}.png"


def image_file_to_data_uri(path):
    with open(path, "rb") as img_file:
        b64 = base64.b64encode(img_file.read()).decode()
        ext = path.split(".")[-1]
        return f"data:image/{ext};base64,{b64}"


@app.route("/api/swap-head", methods=["POST"])
def swap_head_api():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]

    # Validate file type
    if not file.filename or not file.filename.lower().endswith(
        (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")
    ):
        return jsonify({"error": "Invalid file type. Please upload an image."}), 400

    # Validate file size (max 10MB)
    file_content = file.read()
    if len(file_content) > 10 * 1024 * 1024:
        return jsonify({"error": "File too large. Maximum size is 10MB."}), 400

    try:
        # Read the original image bytes
        original_image_bytes = file_content
        # 1. Analyze the user image (resized for analysis)
        analysis = analyze_user_image_from_bytes(original_image_bytes)
        body_type = analysis["metadata"]["body_type"]
        skin_color = analysis["metadata"]["skin_color"]
        gender = analysis["metadata"]["gender"]

        # 2. Get the reference image path (allow override from frontend)
        reference_image_rel = request.form.get("reference_image")
        logging.debug(f"DEBUG: Received reference_image parameter: {reference_image_rel}")
        if reference_image_rel:
            # Sanitize the path to prevent directory traversal
            reference_image_rel = (
                reference_image_rel.replace("..", "").replace("//", "/").strip("/")
            )
            # Always resolve relative to IMAGES_DIR
            ref_path = os.path.join(IMAGES_DIR, reference_image_rel)
            logging.debug(f"DEBUG: Resolved reference image path: {ref_path}")
        else:
            relative_ref_path = get_reference_image_path(body_type, skin_color)
            ref_path = os.path.join(IMAGES_DIR, relative_ref_path)
            logging.debug(f"DEBUG: Using default reference image path: {ref_path}")

        # Validate that the reference image path is within allowed directory
        allowed_base = IMAGES_DIR
        if not os.path.commonpath([ref_path, allowed_base]) == allowed_base:
            return jsonify({"error": "Invalid reference image path"}), 400

        logging.debug(f"DEBUG: Looking for reference image at: {os.path.abspath(ref_path)}")
        logging.debug(f"DEBUG: Reference image exists: {os.path.exists(ref_path)}")
        if os.path.exists(ref_path):
            logging.debug(f"DEBUG: Reference image size: {os.path.getsize(ref_path)} bytes")
        else:
            logging.debug("DEBUG: Reference image not found!")
            # List contents of the directory to help debug
            try:
                dir_path = os.path.dirname(ref_path)
                if os.path.exists(dir_path):
                    logging.debug(f"DEBUG: Directory contents: {os.listdir(dir_path)}")
                else:
                    logging.debug(f"DEBUG: Directory does not exist: {dir_path}")
            except Exception as e:
                logging.debug(f"DEBUG: Error listing directory: {e}")
        
        if not os.path.exists(ref_path):
            return jsonify({"error": "Reference image not found"}), 404

        # Construct the public URL for the pregenerated image (extract from ref_path)
        # Get the relative path from the reference image path
        relative_ref_path = os.path.relpath(ref_path, IMAGES_DIR)
        pregenerated_image_url = f"/images/{relative_ref_path}"
        logging.debug(f"DEBUG: Constructed pregenerated_image_url: {pregenerated_image_url}")

        # 3. Read both images as base64 data URIs
        reference_image_data_uri = image_file_to_data_uri(ref_path)
        # Use the original, unresized image for HeadSwapper
        edit_image_data_uri = (
            "data:image/jpeg;base64," + base64.b64encode(original_image_bytes).decode()
        )

        # Test connectivity to HeadSwapper API
        try:
            test = requests.get("http://34.122.243.90:8090/headswap", timeout=5)
            logging.debug(f"Test GET /headswap status: {test.status_code}")
            logging.debug(f"Test GET /headswap response: {test.text}")
        except Exception as e:
            logging.warning(f"Test GET /headswap failed: {e}")
            logging.warning("WARNING: HeadSwapper service is not available. Using fallback mode.")
            # Return a fallback response for testing purposes
            return jsonify({
                "output_image": reference_image_data_uri,  # Return the reference image as fallback
                "analysis": analysis,
                "pregenerated_image_url": pregenerated_image_url,
                "warning": "HeadSwapper API is currently unavailable. Showing reference image as fallback."
            })

        # 4. Call the HeadSwapper API
        url = "http://34.122.243.90:8090/headswap"
        
        # Prepare the payload according to the new API documentation
        # reference_image: the source image whose head you want to transplant (user's image)
        # edit_image: the target image that supplies the new head style (reference model)
        payload = {
            "reference_image": edit_image_data_uri,  # User's image (source head)
            "edit_image": reference_image_data_uri,  # Reference model (target head style)
            "gender": gender.upper() if gender else None,
            "face_description": f"Natural head swap preserving skin tone, hair texture, and lighting for {body_type} body type with {skin_color} skin.",
            "rotation_degrees": 0,  # Default to 0, API will auto-detect if needed
            "owner_id": "gazman_tryon"
        }
        
        logging.debug("DEBUG: Sending request to HeadSwapper API...")
        logging.debug(f"DEBUG: Reference image path: {ref_path}")
        logging.debug(f"DEBUG: Reference image exists: {os.path.exists(ref_path)}")
        logging.debug(f"DEBUG: Reference image size: {os.path.getsize(ref_path) if os.path.exists(ref_path) else 'N/A'}")
        logging.debug(f"DEBUG: API URL: {url}")
        logging.debug(f"DEBUG: Payload keys: {list(payload.keys())}")
        
        try:
            hs_response = requests.post(url, json=payload, timeout=120)
            logging.debug("DEBUG: HeadSwapper request sent successfully")
            logging.debug(f"HeadSwapper response status: {hs_response.status_code}")
            logging.debug(f"HeadSwapper response: {hs_response.text[:500]}")  # Print first 500 chars of response
            hs_response.raise_for_status()
            
            # Parse the new response structure
            response_data = hs_response.json()
            if response_data.get("status") == "success" and "data" in response_data:
                output_image = response_data["data"]["output_image"]
                logging.debug("DEBUG: Successfully extracted output image from response")
            else:
                logging.debug(f"DEBUG: Unexpected response structure: {response_data}")
                return jsonify({"error": "Invalid response from HeadSwapper service"}), 500
                
        except requests.exceptions.RequestException as e:
            logging.error(f"HeadSwapper API error: {str(e)}")
            return jsonify({"error": "Failed to connect to HeadSwapper service"}), 503
        except Exception as e:
            logging.error(f"Error processing HeadSwapper response: {str(e)}")
            return jsonify({"error": "Failed to process HeadSwapper response"}), 500

        return jsonify(
            {
                "output_image": output_image,
                "analysis": analysis,
                "pregenerated_image_url": pregenerated_image_url,
            }
        )
    except Exception as e:
        logging.error("Error in swap-head:", e)
        traceback.print_exc()
        return jsonify({"error": "Internal server error. Please try again."}), 500


@app.route("/images/<path:filename>")
def serve_images(filename):
    try:
        # Construct the full path to the frontend/public/images directory
        images_dir = IMAGES_DIR
        return send_from_directory(images_dir, filename)
    except Exception as e:
        logging.error(f"Error serving image {filename}: {e}")
        return jsonify({"error": "Image not found"}), 404


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        with open(sys.argv[1], "rb") as f:
            result = analyze_user_image_from_bytes(f.read())
            print(json.dumps(result, indent=2))
    else:
        # Use environment variable to determine if we're in production
        is_production = (
            os.getenv("FLASK_ENV") == "production" or os.getenv("VERCEL") == "1"
        )

        if is_production:
            # Production settings - secure
            app.run(debug=False, port=5003, host="127.0.0.1")
        else:
            # Development settings
            app.run(debug=True, port=5003, host="0.0.0.0")
