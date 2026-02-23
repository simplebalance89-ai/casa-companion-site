"""
Generate 10 narration MP3s for the Casa Companion founder story promo.

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

# 10 clips, 1:1 with 10 slides. NO gaps. NO empty clips.
# V3 — full rewrite, Peter's story
NARRATION = [
    # Clip 1 → ps-1 (the founder)
    "Half my life in music. The other half building enterprise software for some of the biggest "
    "companies in the country. When my son was born, I combined everything I knew. AI was transforming "
    "my business and my life. But for my child? Nothing. No real companion. Nothing to hold, learn from, "
    "bond with away from a screen. So I built one.",

    # Clip 2 → ps-2 (florida test)
    "Took it to Florida for my nephews. They wouldn't put it down. Mom and dad chimed in. "
    "The whole family bonded over one toy. That's when I knew.",

    # Clip 3 → ps-heroes (character grid)
    "Ten companions. Each with their own personality. "
    "Corvo, Gufo, Orsetto, Coniglio, Tartaruga, Elefante, Leone, Delfino, Drago, and Xolo.",

    # Clip 4 → ps-5 (heritage/grandparents)
    "Seventy-five percent of heritage languages disappear by the third generation. "
    "This is a toy that connects grandparents to grandchildren. A bridge across distance, language, and time.",

    # Clip 5 → ps-6 (daddy away/homework)
    "Dad's on a business trip. But tonight, he's still helping with homework. "
    "Still reading the bedtime story. Not through a screen. Through a companion that carries his voice.",

    # Clip 6 → ps-7 (mother's voice/legacy)
    "I lost my mother at an early age. I haven't been able to clone her voice yet. "
    "I only have about ten memories of it. But if we find enough, my son will hear her. "
    "That's not a feature. That's a legacy.",

    # Clip 7 → ps-8 (this generation)
    "Teddy Ruxpin gave us a bond. Cabbage Patch made it personal. "
    "This is what this generation deserves. Built with Capo AI.",

    # Clip 8 → ps-9 (engineering + features)
    "One pod. Ten shells. Magnetic dock. Machine washable. Bluetooth sync. "
    "Parent mode. Teaching mode. No camera. No screen. No microtransactions.",

    # Clip 9 → ps-10 (growth/future)
    "Right now, Capo AI is built for ages one through five. But this is software. It updates. "
    "It grows with your child. Memories, homework, bedtime stories, all synced to your phone. "
    "Think Alexa and Siri, but done right. Parent models coming soon. We're just getting started.",

    # Clip 10 → ps-11 (capisce closer)
    "Casa Companion. Working with families. US made and built. "
    "Taking back childhood the way I was raised and the way a new generation will be. "
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
