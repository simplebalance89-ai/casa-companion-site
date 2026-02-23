"""
Generate 4 slide-specific DALL-E images for promo video.
"""

import os
import time
import httpx

AZURE_KEY = os.getenv("DALLE_API_KEY", "")
AZURE_ENDPOINT = "https://swedencentral.api.cognitive.microsoft.com"
DEPLOYMENT = "dall-e-3"
API_VERSION = "2024-02-01"

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "images")

IMAGES = [
    {
        "filename": "slide1-dad-baby-crow.png",
        "size": "1792x1024",
        "prompt": (
            "A proud father sitting on a soft rug in a modern living room, playing with his infant son. "
            "Between them sits a premium soft black crow plush toy with warm amber glowing eyes and iridescent feathers. "
            "The baby reaches for the crow plush, smiling. Warm natural light streams through a window. "
            "Cozy scene with earth tones. The father gazes at his son with love and pride. "
            "Photorealistic, warm cinematic lighting, shallow depth of field. Premium family lifestyle photography."
        ),
    },
    {
        "filename": "slide5-grandma-cooking-phone.png",
        "size": "1792x1024",
        "prompt": (
            "An Italian grandmother in her 70s cooking sauce in a warm kitchen, stirring a pot on the stove. "
            "She is holding her phone in one hand, smiling warmly at the screen as if recording a voice message or video call. "
            "No toys in the scene. Traditional kitchen with herbs, tomatoes, wooden spoons. "
            "Warm golden light. The feeling of connection through technology across distance. "
            "Photorealistic, warm cinematic lighting, rich warm tones. Emotional, authentic."
        ),
    },
    {
        "filename": "slide8-generation-nostalgia.png",
        "size": "1792x1024",
        "prompt": (
            "A split-generation image: on the left side, a faded warm-toned nostalgic scene of a 1980s child's bedroom "
            "with a Teddy Ruxpin-style cassette tape toy bear and Cabbage Patch-style dolls on a shelf (generic, no brands). "
            "On the right side, a crisp modern scene of a child holding a premium AI-powered plush crow toy with glowing amber eyes, "
            "sitting in a sleek modern nursery. The transition between eras is seamless, showing the evolution of childhood companions. "
            "Photorealistic, cinematic, warm nostalgic tones blending to modern cool tones. No text or logos."
        ),
    },
    {
        "filename": "slide9-exploded-engineering.png",
        "size": "1792x1024",
        "prompt": (
            "A premium plush crow toy shown in an exploded engineering diagram view. The soft plush shell is pulled apart "
            "to reveal the internal components floating in space: a small sleek electronics pod with a speaker, microphone, "
            "Bluetooth chip, battery, and magnetic charging connector. Clean technical illustration style on a dark background. "
            "Labels or lines pointing to each component. The plush shell is soft and premium on the outside, "
            "high-tech on the inside. Product engineering visualization. Clean, technical, premium."
        ),
    },
]


def generate_image(prompt, size, filename, idx, total):
    url = f"{AZURE_ENDPOINT}/openai/deployments/{DEPLOYMENT}/images/generations?api-version={API_VERSION}"
    headers = {"api-key": AZURE_KEY, "Content-Type": "application/json"}
    payload = {"prompt": prompt, "size": size, "n": 1, "quality": "hd", "style": "vivid"}

    print(f"\n[{idx}/{total}] {filename} ({size})")
    print(f"  Prompt: {prompt[:80]}...")

    try:
        resp = httpx.post(url, json=payload, headers=headers, timeout=120.0)
        resp.raise_for_status()
        data = resp.json()
        image_url = data["data"][0]["url"]
        revised = data["data"][0].get("revised_prompt", "")
        if revised:
            print(f"  Revised: {revised[:80]}...")

        img_resp = httpx.get(image_url, timeout=60.0)
        img_resp.raise_for_status()

        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(img_resp.content)

        print(f"  Saved: {filename} ({len(img_resp.content)/1024:.0f} KB)")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main():
    if not AZURE_KEY:
        print("ERROR: DALLE_API_KEY not set.")
        return

    total = len(IMAGES)
    print(f"Generating {total} slide-specific images...\n")

    for i, img in enumerate(IMAGES, 1):
        generate_image(img["prompt"], img["size"], img["filename"], i, total)
        if i < total:
            print("  Waiting 12s...")
            time.sleep(12)

    print("\nDone!")


if __name__ == "__main__":
    main()
