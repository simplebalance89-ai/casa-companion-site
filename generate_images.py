"""
Generate 30 DALL-E 3 images for Casa Companion Kickstarter launch.
Azure deployment: casa-dalle-sweden / dall-e-3

Usage:
    pip install httpx
    python generate_images.py
"""

import os
import time
import httpx

AZURE_KEY = os.getenv("DALLE_API_KEY", "")
AZURE_ENDPOINT = "https://swedencentral.api.cognitive.microsoft.com"
DEPLOYMENT = "dall-e-3"
API_VERSION = "2024-02-01"

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "images", "generated")

# Consistent style anchors
PLUSH_STYLE = (
    "Premium soft plush toy, about 12 inches tall, high-quality stitching, "
    "huggable and round, subtle warm glowing eyes. "
)
PHOTO_STYLE = "Photorealistic, warm cinematic lighting, shallow depth of field. "
ILLUST_STYLE = "Pixar concept art style, warm friendly illustration, soft colors, whimsical. "
PRODUCT_STYLE = "Studio product photography, clean cream background, premium feel, sharp detail. "
SOCIAL_STYLE = "Square format 1:1, dramatic studio lighting, cream background, premium product shot. "

IMAGES = [
    # === CATEGORY 1: Hero Lifestyle Shots (photorealistic, 1792x1024) ===
    {
        "filename": "life-corvo-bedtime.png",
        "size": "1792x1024",
        "prompt": f"A 4-year-old child in pajamas sitting in bed at night, hugging a {PLUSH_STYLE} black crow plush toy with warm amber glowing eyes and iridescent black feathers. Soft nightlight glow. Cozy bedroom. {PHOTO_STYLE}",
    },
    {
        "filename": "life-gufo-stargazing.png",
        "size": "1792x1024",
        "prompt": f"A 3-year-old child lying on a blanket outdoors at dusk, holding a {PLUSH_STYLE} soft round owl plush toy with big golden glowing eyes. Stars beginning to appear in the sky. Warm evening light. {PHOTO_STYLE}",
    },
    {
        "filename": "life-orsetto-adventure.png",
        "size": "1792x1024",
        "prompt": f"A 5-year-old child in a backyard pretending to explore, carrying a {PLUSH_STYLE} huggable brown bear cub plush toy. Sunny day, green grass, adventure feel. {PHOTO_STYLE}",
    },
    {
        "filename": "life-coniglio-tea-party.png",
        "size": "1792x1024",
        "prompt": f"A 3-year-old child at a small table having a pretend tea party with a {PLUSH_STYLE} soft floppy-eared white bunny plush toy. Gentle indoor lighting, whimsical feel. Pastel warmth. {PHOTO_STYLE}",
    },
    {
        "filename": "life-tartaruga-bath.png",
        "size": "1792x1024",
        "prompt": f"A toddler in a cozy room holding a {PLUSH_STYLE} soft sea turtle plush toy with a shimmering blue-green shell. Calm, soothing environment. Cool ocean tones with warm ambient light. {PHOTO_STYLE}",
    },
    {
        "filename": "life-elefante-family.png",
        "size": "1792x1024",
        "prompt": f"A child sitting with parents on a couch, the child holding a {PLUSH_STYLE} soft gray elephant plush toy with big floppy ears. Warm family moment in a cozy living room. {PHOTO_STYLE}",
    },
    {
        "filename": "life-leone-brave.png",
        "size": "1792x1024",
        "prompt": f"A 5-year-old child standing confidently in a doorway, holding a {PLUSH_STYLE} soft lion plush toy with a golden mane. Morning sunlight streaming in. Empowerment pose. Golden warm tones. {PHOTO_STYLE}",
    },
    {
        "filename": "life-delfino-pool.png",
        "size": "1792x1024",
        "prompt": f"A child sitting at the edge of a swimming pool (not in water), holding a {PLUSH_STYLE} soft blue dolphin plush toy with sparkling eyes. Bright summer day, playful atmosphere. {PHOTO_STYLE}",
    },
    {
        "filename": "life-drago-imagination.png",
        "size": "1792x1024",
        "prompt": f"A 4-year-old child inside a blanket fort, holding a {PLUSH_STYLE} sparkly purple dragon plush toy. Fairy lights in the background. Magical, imaginative atmosphere. Warm fantasy tones. {PHOTO_STYLE}",
    },
    {
        "filename": "life-xolo-heritage.png",
        "size": "1792x1024",
        "prompt": f"A child sitting with a grandparent, the child holding a {PLUSH_STYLE} sleek bronze Xoloitzcuintli hairless dog plush toy. Warm family scene with colorful Mexican textiles and warm wood. Rich earth tones. {PHOTO_STYLE}",
    },

    # === CATEGORY 2: Mode Action Shots (illustrated, 1024x1024) ===
    {
        "filename": "mode-story-time.png",
        "size": "1024x1024",
        "prompt": f"A cute illustrated black crow plush toy sitting on an open storybook, tiny magical characters rising from the pages in golden light. {ILLUST_STYLE}",
    },
    {
        "filename": "mode-calm-breathe.png",
        "size": "1024x1024",
        "prompt": f"A cute illustrated round owl plush toy sitting on a fluffy cloud with closed eyes, peaceful expression, soft pastel stars and crescent moon around it. Dreamy calming atmosphere. {ILLUST_STYLE}",
    },
    {
        "filename": "mode-stem-sparks.png",
        "size": "1024x1024",
        "prompt": f"A cute illustrated brown bear plush toy wearing tiny safety goggles, surrounded by floating atoms, colorful gears, and glowing stars. Bright, curious, educational feel. {ILLUST_STYLE}",
    },
    {
        "filename": "mode-music.png",
        "size": "1024x1024",
        "prompt": f"A cute illustrated white bunny plush toy dancing joyfully with colorful musical notes and rhythm symbols swirling around it. Energetic and playful. {ILLUST_STYLE}",
    },
    {
        "filename": "mode-geography.png",
        "size": "1024x1024",
        "prompt": f"A cute illustrated sea turtle plush toy riding on top of a globe, tiny landmarks like the Eiffel Tower and pyramids dotting the surface. Adventure and discovery feel. {ILLUST_STYLE}",
    },
    {
        "filename": "mode-italian.png",
        "size": "1024x1024",
        "prompt": f"A cute illustrated gray elephant plush toy standing in a tiny Italian piazza, holding a gelato cone. Italian flag colors as accents. Warm, charming, cultural. {ILLUST_STYLE}",
    },
    {
        "filename": "mode-spanish.png",
        "size": "1024x1024",
        "prompt": f"A cute illustrated golden lion plush toy surrounded by colorful papel picado banners and maracas. Festive Mexican cultural celebration feel. {ILLUST_STYLE}",
    },
    {
        "filename": "mode-coding.png",
        "size": "1024x1024",
        "prompt": f"A cute illustrated purple dragon plush toy sitting at a tiny desk with glowing code symbols and circuit patterns floating around. Futuristic but friendly and warm. {ILLUST_STYLE}",
    },

    # === CATEGORY 3: Marketing / Kickstarter Assets (product photography, 1792x1024) ===
    {
        "filename": "marketing-lineup.png",
        "size": "1792x1024",
        "prompt": f"Ten premium plush toys lined up in a row on a clean cream surface. From left to right: black crow, round owl, brown bear, white bunny, blue-green sea turtle, gray elephant, golden lion, blue dolphin, purple dragon, bronze hairless dog. Each about 12 inches, soft premium quality with subtle glowing eyes. {PRODUCT_STYLE}",
    },
    {
        "filename": "marketing-pod-swap.png",
        "size": "1792x1024",
        "prompt": f"Close-up of adult hands removing a small sleek electronics pod from inside a plush bear toy, about to place it into a different plush crow shell sitting nearby. Clean white background. Technical but warm. {PRODUCT_STYLE}",
    },
    {
        "filename": "marketing-magnetic-dock.png",
        "size": "1792x1024",
        "prompt": f"A black crow plush toy sitting on a sleek minimalist magnetic charging dock on a nightstand. Soft warm LED glow on the dock base. Nighttime bedroom ambiance. Premium, minimal, clean. {PRODUCT_STYLE}",
    },
    {
        "filename": "marketing-gift-moment.png",
        "size": "1792x1024",
        "prompt": f"A child's face lighting up with pure joy as they open a premium gift box, revealing a soft brown bear plush toy inside beautiful packaging with gold accents. Birthday or holiday feel. Emotional, warm. {PHOTO_STYLE}",
    },
    {
        "filename": "marketing-washable.png",
        "size": "1792x1024",
        "prompt": f"A fluffy white bunny plush toy coming out of a front-loading washing machine, looking perfectly fluffy and clean. Bright, fun, parent-friendly. Clean white laundry room. {PHOTO_STYLE}",
    },
    {
        "filename": "marketing-no-screen.png",
        "size": "1792x1024",
        "prompt": f"A child lying on the floor talking happily to a round owl plush toy, with a tablet and smartphone pushed aside out of focus in the background. Screen-free play messaging. Warm natural light from a window. {PHOTO_STYLE}",
    },

    # === CATEGORY 4: Social Media / Instagram Grid (square, 1024x1024) ===
    {
        "filename": "social-corvo-close.png",
        "size": "1024x1024",
        "prompt": f"Extreme close-up of a premium black crow plush toy face, warm amber glowing eyes, soft iridescent black feathers. Dramatic studio lighting on cream background. {SOCIAL_STYLE}",
    },
    {
        "filename": "social-gufo-close.png",
        "size": "1024x1024",
        "prompt": f"Extreme close-up of a premium round owl plush toy face, big golden glowing eyes, soft brown and cream feather texture. Soft studio lighting on cream background. {SOCIAL_STYLE}",
    },
    {
        "filename": "social-orsetto-close.png",
        "size": "1024x1024",
        "prompt": f"Extreme close-up of a premium brown bear plush toy face, warm kind eyes, soft fluffy brown fur texture. Warm studio lighting on cream background. {SOCIAL_STYLE}",
    },
    {
        "filename": "social-group-pile.png",
        "size": "1024x1024",
        "prompt": f"All ten premium plush companion toys (crow, owl, bear, bunny, turtle, elephant, lion, dolphin, dragon, hairless dog) piled together in a cozy heap on a cream blanket. Overhead shot. Warm, inviting. {SOCIAL_STYLE}",
    },
    {
        "filename": "social-child-hug.png",
        "size": "1024x1024",
        "prompt": f"A child's arms wrapped tightly around a black crow plush toy, face buried in it lovingly. Shot from behind and side. Emotional, intimate moment. Soft warm lighting. {SOCIAL_STYLE}",
    },
    {
        "filename": "social-size-reference.png",
        "size": "1024x1024",
        "prompt": f"A premium brown bear plush toy standing next to a child's small hand for size reference, showing the toy is about 12 inches tall. Clean white background. Simple scale reference product shot. {SOCIAL_STYLE}",
    },
]


def generate_image(prompt: str, size: str, filename: str, idx: int, total: int):
    """Generate one image via Azure DALL-E 3."""
    url = f"{AZURE_ENDPOINT}/openai/deployments/{DEPLOYMENT}/images/generations?api-version={API_VERSION}"
    headers = {
        "api-key": AZURE_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "size": size,
        "n": 1,
        "quality": "hd",
        "style": "vivid",
    }

    print(f"\n[{idx}/{total}] {filename} ({size})")
    print(f"  Prompt: {prompt[:80]}...")

    try:
        resp = httpx.post(url, json=payload, headers=headers, timeout=120.0)
        resp.raise_for_status()
        data = resp.json()

        image_url = data["data"][0]["url"]
        revised_prompt = data["data"][0].get("revised_prompt", "")
        if revised_prompt:
            print(f"  Revised: {revised_prompt[:80]}...")

        # Download the image
        img_resp = httpx.get(image_url, timeout=60.0)
        img_resp.raise_for_status()

        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(img_resp.content)

        size_kb = len(img_resp.content) / 1024
        print(f"  Saved: {filename} ({size_kb:.0f} KB)")
        return True

    except httpx.HTTPStatusError as e:
        print(f"  ERROR: {e.response.status_code} - {e.response.text[:200]}")
        return False
    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return False


def main():
    if not AZURE_KEY:
        print("ERROR: DALLE_API_KEY not set.")
        print("Usage: DALLE_API_KEY=<key> python generate_images.py")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total = len(IMAGES)
    print(f"Generating {total} images via Azure DALL-E 3 (HD quality)...")
    print(f"Output: {OUTPUT_DIR}\n")

    success = 0
    failed = 0

    for i, img in enumerate(IMAGES, 1):
        ok = generate_image(img["prompt"], img["size"], img["filename"], i, total)
        if ok:
            success += 1
        else:
            failed += 1

        # Rate limiting — DALL-E 3 has limits per minute
        if i < total:
            print("  Waiting 12s (rate limit)...")
            time.sleep(12)

    print(f"\n{'='*50}")
    print(f"Done! {success} succeeded, {failed} failed.")
    print(f"Images saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
