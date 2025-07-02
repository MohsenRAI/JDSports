# image_gen/poses.py

"""
Pose definitions for different body types and skin colors.
"""
import random
import time
import hashlib

# Dictionary of poses for different body type and skin color combinations
# POSES = {
#     "athletic_light": """POSE TYPE: POWER STANCE WITH CROSSED ARMS
#         - Standing directly facing camera
#         - Arms crossed firmly at chest level
#         - Elbows pointing outward at 45-degree angles
#         - Feet planted shoulder-width apart
#         - Face and eyes directly to camera""",
#     "athletic_medium": """POSE TYPE: ONE HAND IN POCKET
#         - Standing directly facing camera
#         - Right hand in pants pocket, thumb out
#         - Left arm relaxed at side
#         - Feet hip-width apart
#         - Face and eyes directly to camera""",
#     "athletic_tan": """POSE TYPE: HANDS BEHIND BACK
#         - Standing directly facing camera
#         - Both hands clasped behind lower back
#         - Chest naturally forward
#         - Feet shoulder-width apart
#         - Face and eyes directly to camera""",
#     "average_light": """POSE TYPE: BOTH HANDS IN POCKETS
#         - Standing directly facing camera
#         - Both hands in front pockets, thumbs out
#         - Relaxed, natural stance
#         - Feet hip-width apart
#         - Face and eyes directly to camera""",
#     "average_medium": """POSE TYPE: ONE HAND ADJUSTING CUFF
#         - Standing directly facing camera
#         - Right hand adjusting left cuff at waist level
#         - Left arm slightly raised for cuff adjustment
#         - Feet naturally positioned
#         - Face and eyes directly to camera""",
#     "average_tan": """POSE TYPE: HANDS CLASPED LOW
#         - Standing directly facing camera
#         - Hands clasped loosely at waist level
#         - Relaxed, approachable posture
#         - Feet slightly apart
#         - Face and eyes directly to camera""",
#     "average_dark": """POSE TYPE: CASUAL STANCE
#         - Standing directly facing camera
#         - One hand lightly touching belt buckle
#         - Other arm relaxed at side
#         - Feet casually positioned
#         - Face and eyes directly to camera""",
#     "slim_medium": """POSE TYPE: SUBTLE MOTION
#         - Standing directly facing camera
#         - Right hand adjusting shirt collar
#         - Left hand in pocket
#         - Feet in narrow stance
#         - Face and eyes directly to camera""",
#     "slim_tan": """POSE TYPE: MODERN POSE
#         - Standing directly facing camera
#         - Both hands adjusting shirt cuffs
#         - Elbows slightly out
#         - Feet hip-width apart
#         - Face and eyes directly to camera""",
#     "slim_dark": """POSE TYPE: REFINED STANCE
#         - Standing directly facing camera
#         - Hands clasped at chest level
#         - Fingers interlocked elegantly
#         - Feet slightly apart
#         - Face and eyes directly to camera""",
#     "muscular_light": """POSE TYPE: STRONG CROSSED ARMS
#         - Standing directly facing camera
#         - Arms crossed high on chest
#         - Biceps naturally flexed
#         - Feet in strong stance
#         - Face and eyes directly to camera""",
#     "muscular_medium": """POSE TYPE: POWER GESTURE
#         - Standing directly facing camera
#         - One hand adjusting watch
#         - Other arm showing natural muscle
#         - Feet shoulder-width apart
#         - Face and eyes directly to camera""",
#     "muscular_dark": """POSE TYPE: COMMANDING POSE
#         - Standing directly facing camera
#         - Hands clasped behind back
#         - Chest and shoulders broad
#         - Feet planted firmly
#         - Face and eyes directly to camera""",
#     "stocky_medium": """POSE TYPE: STABLE POSE
#         - Standing directly facing camera
#         - One hand in pocket
#         - Other hand holding belt
#         - Feet in stable position
#         - Face and eyes directly to camera""",
#     "large_medium": """POSE TYPE: EXECUTIVE STANCE
#         - Standing directly facing camera
#         - Hands clasped at front
#         - Dignified, upright posture
#         - Feet in power stance
#         - Face and eyes directly to camera""",
# }

# # Default poses for each body type (used when specific combination is not found)
# DEFAULT_POSES = {
#     "athletic": """POSE TYPE: ATHLETIC STANCE
#         - Standing directly facing camera
#         - Arms slightly away from body
#         - Shoulders back, chest up
#         - Feet shoulder-width apart
#         - Face and eyes directly to camera""",
#     "slim": """POSE TYPE: ELEGANT STANCE
#         - Standing directly facing camera
#         - One hand lightly at side
#         - Other hand in pocket
#         - Feet close together
#         - Face and eyes directly to camera""",
#     "average": """POSE TYPE: NEUTRAL STANCE
#         - Standing directly facing camera
#         - Both arms relaxed at sides
#         - Natural, relaxed posture
#         - Feet hip-width apart
#         - Face and eyes directly to camera""",
#     "muscular": """POSE TYPE: STRONG STANCE
#         - Standing directly facing camera
#         - Arms slightly away from torso
#         - Chest elevated, shoulders back
#         - Feet in power position
#         - Face and eyes directly to camera""",
#     "stocky": """POSE TYPE: SOLID STANCE
#         - Standing directly facing camera
#         - Hands clasped in front
#         - Balanced, stable posture
#         - Feet shoulder-width apart
#         - Face and eyes directly to camera""",
# }

# List of fallback poses that can be used for any body type
FALLBACK_POSES = [
    # COOL ADVERTISING POSES - Leaning, sitting, standing
    "Full body shot of a man leaning confidently against a modern glass building on Collins Street in Melbourne CBD with skyscrapers behind. Left shoulder against wall, right hand in pocket, legs crossed at ankles. Head turned directly toward camera with a charismatic, confident smile. Urban Australian cityscape backdrop.",
    "Full body shot of a man standing with arms crossed in a power stance on George Street in Sydney with Harbour Bridge visible in distance. Feet shoulder-width apart, confident posture, one eyebrow slightly raised. Head facing camera directly with an intense, professional gaze. Iconic Sydney architecture background.",
    "Full body shot of a man casually leaning against a palm tree in Queen Street Mall Brisbane with one hand adjusting his collar. Relaxed lean with crossed ankles, other hand in pocket. Head turned to face camera with a warm, approachable smile. Subtropical Queensland urban setting.",
    "Full body shot of a man sitting on a modern concrete ledge along St Kilda Road Melbourne with Royal Botanic Gardens behind. One foot on ground, other leg extended, hands resting on thigh. Head facing camera directly with a genuine, relaxed expression. Tree-lined Melbourne boulevard atmosphere.",
    "Full body shot of a man leaning against a heritage pillar in Rundle Mall Adelaide with one arm draped casually. Side lean with weight on left leg, right hand adjusting watch. Head facing camera directly with a sophisticated, charming expression. South Australian city center heritage atmosphere.",
    "Full body shot of a man sitting on steps of Flinders Street Station Melbourne with one elbow on knee. Casual seated pose with one foot flat, other leg angled. Head turned directly toward camera with an engaging, friendly smile. Classic Melbourne streetscape with iconic architecture.",
    "Full body shot of a man leaning casually against a brick wall in James Street Fortitude Valley Brisbane. One shoulder against wall, arms crossed loosely, ankles crossed. Head turned to camera with a hip, creative smile. Brisbane's trendy converted warehouse district.",
    "Full body shot of a man sitting on a modern bench in King William Street Adelaide with one arm stretched along the back. Relaxed seated pose with legs spread naturally, confident posture. Head facing camera directly with a warm, executive smile. Adelaide's cultural boulevard setting.",
    "Full body shot of a man standing in a doorway on Bourke Street Melbourne with one hand on the frame. Casual lean in doorway, other hand adjusting cuff, weight on back foot. Head turned toward camera with a cool, street-smart expression. Melbourne's famous street art backdrop.",
    "Full body shot of a man sitting on a waterfront railing along the Esplanade in Cairns with legs dangling. Hands gripping rail beside hips, relaxed coastal pose. Head facing camera directly with a laid-back, tropical smile. North Queensland waterfront atmosphere.",
    # CLASSIC WALKING POSES - Dynamic movement
    "Full body shot of a man confidently walking down Collins Street in Melbourne CBD with modern skyscrapers and trams in the background. Mid-stride with left foot forward, both arms swinging naturally at sides. Head turned directly toward camera with a warm, genuine smile. Urban Australian cityscape with contemporary architecture visible behind.",
    "Full body shot of a man walking down George Street in Sydney with the Harbour Bridge visible in the distance. Natural walking stride with right foot forward, hands relaxed by sides. Head facing camera directly with confident, professional expression. Iconic Sydney street scene with classic Australian architecture.",
    "Full body shot of a man strolling down Queen Street Mall in Brisbane with subtropical palm trees and modern buildings. Casual walking pace with left foot stepping forward, one hand in pocket, other swinging naturally. Head turned to face camera with friendly, approachable smile. Queensland urban landscape.",
    "Full body shot of a man walking along St Kilda Road in Melbourne with Royal Botanic Gardens visible to one side. Confident stride with right foot forward, both hands at sides in natural walking motion. Direct eye contact with camera, warm expression. Tree-lined Melbourne boulevard setting.",
    "Full body shot of a man walking down Hay Street in Perth CBD with Western Australian sunshine and modern office buildings. Mid-stride with left foot forward, right hand adjusting collar while walking. Head facing camera with relaxed, confident smile. Perth's distinctive urban architecture backdrop.",
    "Full body shot of a man strolling through Rundle Mall in Adelaide with heritage buildings and contemporary shops. Natural walking gait with right foot forward, hands positioned naturally while walking. Head turned directly toward camera with genuine, warm expression. South Australian city center atmosphere.",
    "Full body shot of a man walking down Flinders Street in Melbourne near the iconic station. Confident walking pace with left foot stepping forward, one hand casually in pocket. Head facing camera directly with professional, engaging smile. Classic Melbourne streetscape with heritage architecture.",
    "Full body shot of a man walking along Circular Quay in Sydney with Opera House glimpsed in background. Natural stride with right foot forward, both arms in natural walking position. Direct camera gaze with confident, approachable expression. Harbour city urban setting.",
    "Full body shot of a man strolling down James Street in Fortitude Valley, Brisbane with trendy cafes and converted warehouses. Relaxed walking pace with left foot forward, right hand adjusting shirt while walking. Head turned to camera with friendly, casual smile. Brisbane's hip urban district.",
    "Full body shot of a man walking through King William Street in Adelaide with North Terrace cultural precinct visible. Mid-stride with right foot forward, hands swinging naturally while walking. Head facing camera directly with warm, professional expression. Adelaide's cultural boulevard setting.",
    # MORE COOL POSES - Mixed variety
    "Full body shot of a man leaning against a vintage streetlight on Hunter Street Newcastle with crossed arms. Classic model lean, one ankle crossed over other, confident stance. Head turned directly toward camera with a heritage-inspired, noble expression. Newcastle's historic harbour landscape.",
    "Full body shot of a man sitting on sandstone steps at Salamanca Place Hobart with elbows on knees. Forward-leaning seated pose, hands clasped, athletic positioning. Head facing camera directly with an artisan, authentic smile. Tasmania's historic waterfront district atmosphere.",
    "Full body shot of a man standing with one foot on a rock formation in Todd Mall Alice Springs. Adventure pose with hands on hips, chest open to sky. Head turned toward camera with a rugged, outback confidence. Red Centre desert town setting.",
    "Full body shot of a man leaning against a modern railing at Darling Harbour Sydney with arms spread wide. Relaxed lean with arms extended along rail, open body language. Head facing camera directly with a successful, metropolitan smile. Sydney's contemporary waterfront precinct.",
    "Full body shot of a man sitting on a café chair outside on Chapel Street Melbourne with one arm draped over back. Casual seated pose, legs positioned naturally, urban sophistication. Head turned to camera with a trendy, fashion-forward expression. Melbourne's premier shopping and dining strip.",
    "Full body shot of a man standing with hands clasped behind back in Northbridge Perth with chest proudly forward. Military-inspired confident stance, feet planted firmly. Head facing camera directly with a cultural, refined smile. Perth's vibrant entertainment district.",
    "Full body shot of a man leaning against his car door on Crown Street Wollongong with arms crossed high. Cool automotive lean, weight on vehicle, confident stance. Head turned toward camera with a coastal, adventurous expression. NSW coastal city with escarpment views.",
    "Full body shot of a man sitting on a riverfront bench at South Bank Brisbane with one leg crossed over other. Executive relaxed pose, arm along bench back, polished posture. Head facing camera directly with a successful, riverside smile. Brisbane's premier cultural district.",
    # MORE WALKING POSES - Additional movement variety
    "Full body shot of a man walking down Bourke Street in Melbourne with iconic street art and laneways nearby. Confident walking gait with left foot stepping forward, one hand near belt while walking. Direct eye contact with camera, relaxed smile. Melbourne's famous street culture backdrop.",
    "Full body shot of a man strolling along the Esplanade in Cairns with tropical Queensland atmosphere. Natural walking pace with right foot forward, both hands positioned naturally while moving. Head turned toward camera with genuine, warm expression. Tropical North Queensland urban setting.",
    "Full body shot of a man walking down Hunter Street in Newcastle with historic buildings and harbour glimpses. Confident stride with left foot forward, right hand in pocket while walking. Head facing camera directly with professional, friendly smile. Newcastle's heritage urban landscape.",
    "Full body shot of a man walking through Salamanca Place in Hobart with historic sandstone buildings. Mid-stride with right foot forward, both arms in natural walking motion. Direct camera gaze with confident, approachable expression. Tasmania's historic waterfront district.",
    "Full body shot of a man strolling down Todd Mall in Alice Springs with Red Centre architecture and desert atmosphere. Natural walking pace with left foot stepping forward, one hand adjusting cuff while walking. Head turned to camera with warm, genuine smile. Outback Australian town setting.",
    "Full body shot of a man walking along Darling Harbour in Sydney with modern developments and waterfront views. Confident walking gait with right foot forward, hands positioned naturally while moving. Head facing camera directly with relaxed, professional expression. Sydney's modern waterfront precinct.",
    # FINAL COOL POSES - More advertising variety
    "Full body shot of a man standing with hands in pockets on Glenelg Jetty Road Adelaide with weight shifted to one leg. Casual model stance, slightly tilted posture, beachside confidence. Head turned to camera with a seaside, relaxed expression. Adelaide's popular beach suburb.",
    "Full body shot of a man leaning against street art wall on Hindley Street Adelaide with one leg bent behind him. Hip artistic lean, hands in pockets, creative pose. Head facing camera directly with an edgy, artistic smile. Adelaide's vibrant nightlife and street art precinct.",
    "Full body shot of a man sitting on steps in Smith Street Collingwood Melbourne with guitar case beside him. Musician-inspired pose, one elbow on knee, bohemian styling. Head turned toward camera with a creative, alternative expression. Melbourne's eclectic bohemian neighborhood.",
    "Full body shot of a man standing with arms wide on a balcony railing on Cavill Avenue Gold Coast. Open confident pose, embracing the view, vacation vibes. Head facing camera directly with a holiday, energetic smile. Gold Coast's iconic high-rise strip.",
    "Full body shot of a man leaning against a heritage building column on William Street Perth with one hand adjusting tie. Sophisticated lean, business-casual confidence, refined posture. Head turned toward camera with a professional, heritage-inspired expression. Perth's historic main street.",
    "Full body shot of a man sitting at an outdoor table on Lygon Street Carlton Melbourne with espresso cup in hand. Continental café pose, legs crossed, sophisticated casual. Head facing camera directly with a cultured, coffee-culture smile. Melbourne's famous Italian precinct.",
    "Full body shot of a man standing with surfboard against his leg on Jetty Road Glenelg with beach vibes. Surf-inspired pose, board as prop, coastal lifestyle confidence. Head turned to camera with a beach-athletic, sun-kissed expression. Adelaide's historic beach suburb with trams.",
    "Full body shot of a man leaning against a shopping centre pillar on Murray Street Perth CBD with shopping bags at feet. Consumer confidence pose, relaxed shopping stance, metropolitan lifestyle. Head facing camera directly with a successful, shopping-district smile. Perth's main commercial thoroughfare.",
    # HARBOUR SCENES - Spectacular Australian waterfront locations
    "Full body shot of a man leaning against harbour railing at Circular Quay Sydney with Sydney Harbour Bridge and Opera House visible behind. One elbow on rail, relaxed harbour pose, confident maritime styling. Head facing camera directly with an iconic-Australian, harbour-city smile. World-famous Sydney Harbour with ferries and yachts in background.",
    "Full body shot of a man sitting on harbour steps at Darling Harbour Sydney with one leg extended and hands behind for support. Waterfront seated pose, relaxed harbour lifestyle, metropolitan confidence. Head turned toward camera with a sophisticated, harbourside expression. Modern Sydney waterfront with high-rise developments and harbour lights.",
    "Full body shot of a man standing with arms crossed on the jetty at Port Adelaide with industrial harbour and container ships behind. Strong maritime pose, port-city confidence, working harbour authenticity. Head facing camera directly with a maritime-heritage, South Australian smile. Historic port with cranes and shipping infrastructure.",
    "Full body shot of a man leaning against a yacht mast at Constitution Dock Hobart with MONA and Mount Wellington behind. Nautical lean, sailing lifestyle confidence, Tasmanian sophistication. Head turned toward camera with a yacht-club, sophisticated-island expression. Premium marina with luxury yachts and mountain backdrop.",
    "Full body shot of a man sitting on harbour rocks at Fremantle Fishing Boat Harbour with fishing fleet behind. Maritime casual pose, working port atmosphere, Western Australian coastal confidence. Head facing camera directly with a seafood-fresh, fishing-port smile. Authentic fishing harbour with working boats and maritime heritage.",
    "Full body shot of a man standing with one foot on harbour bollard at Wynyard Wharf Tasmania with Spirit of Tasmania ferry visible. Ferry-terminal confidence pose, inter-island travel sophistication, Tasmanian gateway styling. Head turned toward camera with a Bass-Strait, transport-hub expression. Major ferry terminal with interstate connections.",
    # BAR & NIGHTLIFE SCENES - Sophisticated Australian venues
    "Full body shot of a man leaning against polished bar counter in trendy rooftop bar with Melbourne city lights behind. Sophisticated bar lean, evening confidence, nightlife metropolitan styling. Head facing camera directly with a cocktail-hour, rooftop-sophistication smile. Premium rooftop venue with city views and ambient lighting.",
    "Full body shot of a man sitting on bar stool at craft beer brewery in Surry Hills Sydney with exposed brick walls. Artisan brewery pose, craft culture confidence, inner-city brewery sophistication. Head turned toward camera with a craft-beer-savvy, brewery-culture expression. Industrial-chic brewery with beer tanks and tasting paddles.",
    "Full body shot of a man standing with elbow on high table at wine bar in Brisbane CBD with city lights through windows. Wine culture pose, sophisticated evening confidence, Queensland nightlife styling. Head facing camera directly with a wine-connoisseur, evening-executive smile. Contemporary wine bar with ambient lighting and city views.",
    "Full body shot of a man leaning against exposed brick wall in pub beer garden in Adelaide CBD with string lights above. Relaxed pub pose, after-work confidence, South Australian pub culture styling. Head turned toward camera with a beer-garden, evening-social expression. Traditional Australian pub garden with heritage character and social atmosphere.",
    "Full body shot of a man sitting at outdoor bar table in Northbridge Perth with neon bar signs behind. Entertainment district pose, nightlife confidence, Western Australian bar scene styling. Head facing camera directly with a Northbridge-nightlife, entertainment-district smile. Vibrant bar strip with neon signage and urban energy.",
    "Full body shot of a man standing with cocktail glass at upscale hotel bar in Darwin CBD with tropical ambiance. Sophisticated tropical pose, resort-bar confidence, Top End luxury styling. Head turned toward camera with a tropical-executive, resort-sophistication expression. Premium hotel bar with tropical plants and ambient resort lighting.",
    # DIVERSE INDOOR/OUTDOOR MIX - Additional Australian variety
    "Full body shot of a man leaning against modern glass facade at Australian Parliament House Canberra with one hand adjusting cufflink. Political district confidence, national capital sophistication, leadership styling. Head facing camera directly with a parliamentary, national-significance smile. Modern government architecture with national importance and dignity.",
    "Full body shot of a man sitting on modern bench in Queen Street Mall Brisbane shopping center with retail stores behind. Shopping district pose, consumer confidence, Queensland retail sophistication. Head turned toward camera with a shopping-executive, retail-success expression. Premier shopping precinct with modern retail atmosphere.",
    "Full body shot of a man standing with arms crossed in foyer of Australian Museum Sydney with aboriginal art behind. Cultural institution pose, intellectual confidence, heritage sophistication. Head facing camera directly with a museum-curator, cultural-appreciation smile. Major cultural institution with indigenous art and educational atmosphere.",
    "Full body shot of a man leaning against racing barrier at Flemington Racecourse Melbourne with grandstand behind. Racing fashion pose, Melbourne Cup confidence, thoroughbred sophistication. Head turned toward camera with a race-day, sporting-elegance expression. Premium racing facility with grandstands and sporting heritage.",
    "Full body shot of a man sitting at café table on Salamanca Market Hobart with artisan market stalls behind. Weekend market pose, artisan confidence, Tasmanian creative sophistication. Head facing camera directly with a weekend-market, artisan-culture smile. Historic market with handmade goods and creative atmosphere.",
]

# Combine all poses into a single list for random selection
ALL_POSES = FALLBACK_POSES  # list(POSES.values()) + list(DEFAULT_POSES.values()) + FALLBACK_POSES

# WINTER OUTDOOR POSES
WINTER_POSES = [
    "Full body shot of a man leaning casually against a wooden ski resort fence, snowy mountains in background, arms crossed. Head facing camera with a confident, relaxed smile. Alpine ski resort setting with fresh powder snow.",
    "Full body shot of a man standing confidently in front of a chalet with snow-covered roof, hands in pockets, light snow falling. Head facing camera with a warm, genuine smile. Traditional alpine chalet with winter atmosphere.",
    "Full body shot of a man in mid-hike pose on a snowy trail with pine trees behind, one hand in pocket, one holding sunglasses. Head facing camera with an adventurous, energetic smile. Snowy mountain trail setting.",
    "Full body shot of a man leaning against a snow-dusted wooden railing with ski lift in background, arms relaxed. Head facing camera with a casual, confident smile. Ski resort setting with winter sports atmosphere.",
    "Full body shot of a man walking pose in fresh snow path, hands at sides or lightly swinging. Head facing camera with a natural, relaxed smile. Winter trail setting with pristine snow."
]

def generate_random_seed(body_type, skin_color):
    """
    Generate a random seed based on the current time and the body type and skin color.
    This ensures that each generation gets a different seed.

    Args:
        body_type (str): Body type name
        skin_color (str): Skin color name

    Returns:
        int: Random seed
    """
    # Get current timestamp in microseconds for uniqueness
    timestamp = str(time.time())

    # Combine inputs to create a unique string
    unique_string = f"{timestamp}_{body_type}_{skin_color}_{random.randint(1, 10000)}"

    # Create a hash of the string to get a deterministic but unpredictable value
    hash_object = hashlib.md5(unique_string.encode())
    hash_hex = hash_object.hexdigest()

    # Convert the first 8 characters of the hash to an integer
    return int(hash_hex[:8], 16)


def get_pose_for_body_and_skin(body_type, skin_color):
    return (
        "Model is standing naturally and facing the camera on a city sidewalk in New York City. "
        "Arms relaxed at sides or lightly interacting with the hoodie (e.g., adjusting sleeve or pocket). "
        "Face clearly visible, neutral or confident expression. "
        "Urban sidewalk, red-brick buildings, and storefronts in soft focus. "
        "Bright diffused daylight, realistic lighting and shadows. "
        "No snow, no winter elements, no ski resort."
    )
