"""
One-time script: Generate 10 narration MP3s for the Casa Companion founder story promo.

Architecture: 1 audio clip = 1 slide. Each clip maps to exactly one visual slide.
Audio-driven timeline: JS plays clip N, shows slide N, advances on clip.onended.

Backend: Azure gpt-4o-mini-tts (nova voice).

Usage:
    pip install httpx python-dotenv
    python generate_narration.py
"""

import os
import httpx
from dotenv import load_dotenv

# Load .env from demo/ directory (shared Azure credentials)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "demo", ".env"))

AZURE_API_KEY = os.getenv("AZURE_API_KEY", "")
AZURE_BASE = "https://pwgcerp-9302-resource.openai.azure.com"
TTS_DEPLOYMENT = "gpt-4o-mini-tts"
TTS_API_VERSION = "2025-04-01-preview"

NARRATION = [
    # Clip 1 — scene1-father.png
    "I build AI tools for business. ERP solutions. Enterprise software. "
    "When my first son was born, I wanted something that would actually get him playing, learning, and off a screen. "
    "Nothing existed. So I built one.",

    # Clip 2 — life-boy-crow.png
    "Started as a custom GPT on my phone. Just ChatGPT. "
    "I saw the potential, but I saw the limitations. "
    "Flew to Florida and let my nephews try it. Two and four years old. "
    "They wouldn't put it down. We were in the car and all five of us wouldn't put it down. "
    "Mom and dad jumped in. My first prototype. All of us laughing, bonding, communicating. No screen. "
    "That's when I knew.",

    # Clip 3 — scene3-heroes.png
    "So I built it the right way. The way I build for work. "
    "Ten companions. Each with their own personality. "
    "Corvo the Crow. Gufo the Owl. Orsetto the Bear. Coniglio the Bunny. "
    "Tartaruga the Sea Turtle. Elefante the Elephant. Leone the Lion. "
    "Delfino the Dolphin. Drago the Dragon. And Xolo.",

    # Clip 4 — life-nonna-kitchen.png
    "Stories in Italian, because heritage disappears in one generation if you let it. "
    "Seventy-five percent of heritage languages are lost by the third generation. "
    "Your grandmother's Italian. Your grandfather's Spanish. Their lullabies. Gone. "
    "Unless you build something to keep them.",

    # Clip 5 — life-grandparent-distance.png
    "Seventy million grandparents in America. "
    "Forty-two percent live in a different state than their grandchildren. "
    "They spend thousands every year. But what they really want to give can't be bought in a store. "
    "Record twelve phrases. Five minutes. That voice lives inside the toy. "
    "Grandma reads bedtime stories from a thousand miles away. "
    "Not through a screen. Through a companion the child holds and falls asleep with.",

    # Clip 6 — banner-father-recording.png
    "This was born from losing my mother at a very early age. "
    "Her spirit lives with my son and me. "
    "So we cloned her voice so my son could hear her. And you can too. "
    "For all family generations. "
    "When a grandparent records their voice in Casa Companion, that voice doesn't expire. "
    "It doesn't require a subscription. "
    "Your child can hear Nonna say buonanotte ten years from now. Twenty years from now. "
    "That's not a feature. That's a legacy.",

    # Clip 7 — scene5-crow.png
    "Teddy Ruxpin gave us a bond with a toy. Cabbage Patch made it personal. Furby gave it personality. "
    "This is what this generation deserves. But built with real AI. "
    "Seven agents built in. Stories. Languages. Sign language. Music. Brain games. Milestones. "
    "No screen. Just your voice.",

    # Clip 8 — eng-exploded.png
    "One electronics pod. Fifteen plush shells. Magnetic charging dock. Machine washable. "
    "Volume capped at eighty-five decibels. No camera. No screen. No microtransactions. Ever. "
    "Built for real kids. Built for real parents.",

    # Clip 9 — packaging-unbox.png → packaging-box.png → packaging-shelf.png
    "Casa Companion. Coming to Kickstarter May fifth, twenty twenty-six. "
    "Early bird pricing. Limited quantities. "
    "Your voice. Their companion.",

    # Clip 10 — banner-crow-cinematic.png
    "Everyone else announced it. We built it.",
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
        "voice": "nova",
        "input": text,
        "instructions": (
            "Speak warmly and clearly, like a founder telling his personal story "
            "in a heartfelt product video. Moderate pace, genuine emotion, natural pauses "
            "between sentences. Slightly slower on emotional moments."
        ),
    }
    resp = httpx.post(url, json=payload, headers=headers, timeout=90.0)
    resp.raise_for_status()
    return resp.content


def main():
    if not AZURE_API_KEY:
        print("ERROR: AZURE_API_KEY not set. Check demo/.env")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Clean old narration files
    for f in os.listdir(OUTPUT_DIR):
        if f.startswith("narration-") and f.endswith(".mp3"):
            os.remove(os.path.join(OUTPUT_DIR, f))
            print(f"  Removed old {f}")

    print(f"\nGenerating {len(NARRATION)} narration clips (Azure TTS, nova voice)...\n")

    for i, text in enumerate(NARRATION, 1):
        filename = f"narration-{i}.mp3"
        print(f"Clip {i}/{len(NARRATION)}: {text[:60]}...")
        content = generate_azure(text, i)
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(content)
        size_kb = len(content) / 1024
        print(f"  {filename}: {size_kb:.1f} KB")

    print(f"\nDone! {len(NARRATION)} files saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
