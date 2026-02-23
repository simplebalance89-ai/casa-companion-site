"""
Generate 16 narration MP3s for the Casa Companion founder story promo.

Architecture: 1 audio clip = 1 slide. Each clip maps to exactly one visual slide.
Audio-driven timeline: JS plays clip N, shows slide N, advances on clip.onended.

Backend: Azure gpt-4o-mini-tts (onyx voice).

Usage:
    pip install httpx python-dotenv
    python generate_narration.py
"""

import os
import httpx

AZURE_API_KEY = os.getenv("AZURE_API_KEY", "")
AZURE_BASE = "https://pwgcerp-9302-resource.openai.azure.com"
TTS_DEPLOYMENT = "gpt-4o-mini-tts"
TTS_API_VERSION = "2025-04-01-preview"

# 16 clips, 1:1 with 16 slides. One sentence per slide. Image-heavy.
# V4 — expanded from V3, split into single sentences
NARRATION = [
    # Clip 1 → ps-1 (founder intro)
    "Half my life in music. The other half building enterprise software "
    "for some of the biggest companies in the country.",

    # Clip 2 → ps-2 (the realization)
    "When my son was born, I combined everything I knew. AI was transforming "
    "my business. But for my child? Nothing.",

    # Clip 3 → ps-3 (the mission)
    "No real companion. Nothing to hold, learn from, bond with — "
    "away from a screen. So I built one.",

    # Clip 4 → ps-4 (florida test)
    "Took it to Florida for my nephews. They wouldn't put it down. "
    "The whole family bonded over one toy.",

    # Clip 5 → ps-heroes (character grid)
    "Ten companions. Each with their own personality. "
    "Corvo, Gufo, Orsetto, Coniglio, Tartaruga, Elefante, Leone, Delfino, Drago, and Xolo.",

    # Clip 6 → ps-6 (heritage languages)
    "Seventy-five percent of heritage languages disappear by the third generation.",

    # Clip 7 → ps-7 (grandparents bridge)
    "A toy that connects grandparents to grandchildren. "
    "A bridge across distance, language, and time.",

    # Clip 8 → ps-8 (daddy away)
    "Dad's on a business trip. But tonight, he's still helping with homework. "
    "Still reading the bedtime story.",

    # Clip 9 → ps-9 (voice companion)
    "Not through a screen. Through a companion that carries his voice.",

    # Clip 10 → ps-10 (mother's legacy — dark slide)
    "I lost my mother at an early age. I only have about ten memories of her voice. "
    "But if we find enough, my son will hear her. That's not a feature. That's a legacy.",

    # Clip 11 → ps-11 (this generation)
    "Teddy Ruxpin gave us a bond. Cabbage Patch made it personal. "
    "This is what this generation deserves.",

    # Clip 12 → ps-12 (engineering)
    "One pod. Ten shells. Magnetic dock. Machine washable. "
    "No camera. No screen. No microtransactions.",

    # Clip 13 → ps-13 (features)
    "Bluetooth sync. Parent mode. Homework helper. All languages. Built with Capo AI.",

    # Clip 14 → ps-14 (growth)
    "Right now, Capo AI is built for ages one through five. But this is software. "
    "It grows with your child.",

    # Clip 15 → ps-15 (sync / future)
    "Memories, homework, bedtime stories — all synced to your phone. "
    "Think Alexa and Siri, but done right.",

    # Clip 16 → ps-16 (capisce closer)
    "Casa Companion. US made and built. Taking back childhood. "
    "Kickstarter May fifth. Capisce.",
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio")


def generate_azure(text: str, clip_num: int):
    url = f"{AZURE_BASE}/openai/deployments/{TTS_DEPLOYMENT}/audio/speech?api-version={TTS_API_VERSION}"
    headers = {
        "api-key": AZURE_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini-tts",
        "voice": "onyx",
        "input": text,
        "instructions": (
            "Deep male voice. Brisk, confident pace. New York energy. "
            "You're a founder pitching to investors. Keep it tight. No long pauses. "
            "Sentences land fast. Move to the next line quickly. "
            "Warm but punchy. Like a 60-second pitch, not a fireside chat."
        ),
    }
    resp = httpx.post(url, json=payload, headers=headers, timeout=90.0)
    resp.raise_for_status()
    return resp.content


def main():
    if not AZURE_API_KEY:
        print("ERROR: AZURE_API_KEY not set.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Clean old narration files
    for f in os.listdir(OUTPUT_DIR):
        if f.startswith("narration-") and f.endswith(".mp3"):
            os.remove(os.path.join(OUTPUT_DIR, f))
            print(f"  Removed old {f}")

    print(f"\nGenerating {len(NARRATION)} narration clips (Azure TTS, onyx voice)...\n")

    for i, text in enumerate(NARRATION, 1):
        filename = f"narration-{i}.mp3"
        print(f"Clip {i}/{len(NARRATION)}: {text[:60]}...")
        content = generate_azure(text, i)
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(content)
        size_kb = len(content) / 1024
        print(f"  {filename}: {size_kb:.1f} KB")

    print(f"\nDone! {len(NARRATION)} clips saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
