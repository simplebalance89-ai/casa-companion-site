"""
One-time script: Generate narration MP3s for the Casa Companion 30s promo.
Uses Azure TTS (gpt-4o-mini-tts, voice: nova).

Run once, commit the audio files, then delete this script if desired.

Usage:
    pip install httpx python-dotenv
    python generate_narration.py
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

AZURE_API_KEY = os.getenv("AZURE_API_KEY", "")
AZURE_BASE = "https://pwgcerp-9302-resource.openai.azure.com"
TTS_DEPLOYMENT = "gpt-4o-mini-tts"
TTS_API_VERSION = "2025-04-01-preview"

NARRATION = [
    "What if your child could hear your voice... anytime they needed you?",
    "Meet Casa Companion. An AI plush toy that speaks in your voice.",
    "Record twelve phrases. We clone your voice. Your stories. Your goodnight.",
    "Three languages. Solar charging. Machine washable. Built to grow with your child.",
    "Five companions. Corvo the Crow. Gufo the Owl. Orsetto the Bear. Volpe the Fox. Coniglio the Bunny.",
    "Eyes that show emotion. Listening. Thinking. Speaking. Happy.",
    "Starting at seventy-nine dollars. Early bird pricing on Kickstarter.",
    "Casa Companion. Your voice. Their companion.",
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio")


def generate_audio(text: str, filename: str):
    url = f"{AZURE_BASE}/openai/deployments/{TTS_DEPLOYMENT}/audio/speech?api-version={TTS_API_VERSION}"

    headers = {
        "api-key": AZURE_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gpt-4o-mini-tts",
        "voice": "nova",
        "input": text,
        "instructions": "Speak warmly and clearly, like a narrator for a heartfelt product video. Moderate pace, genuine emotion.",
    }

    resp = httpx.post(url, json=payload, headers=headers, timeout=60.0)
    resp.raise_for_status()

    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(resp.content)

    size_kb = len(resp.content) / 1024
    print(f"  {filename}: {size_kb:.1f} KB")


def main():
    if not AZURE_API_KEY:
        print("ERROR: AZURE_API_KEY not set. Add it to .env or environment.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Generating narration audio files...\n")
    for i, text in enumerate(NARRATION, 1):
        filename = f"narration-{i}.mp3"
        print(f"Scene {i}: {text[:60]}...")
        generate_audio(text, filename)

    print(f"\nDone! {len(NARRATION)} files saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
