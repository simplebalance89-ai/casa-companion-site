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
NARRATION = [
    # Clip 1 → ps-1 (scene1-father)
    "I build AI for business. When my son was born, I wanted something real. "
    "Nothing existed. So I built one.",

    # Clip 2 → ps-2 (life-boy-crow)
    "Let my nephews try it. Two and four years old. "
    "They wouldn't put it down. That's when I knew.",

    # Clip 3 → ps-heroes (character grid)
    "Ten companions. Each with their own personality. "
    "Corvo, Gufo, Orsetto, Coniglio, Tartaruga, Elefante, Leone, Delfino, Drago, and Xolo.",

    # Clip 4 → ps-5 (heritage)
    "Seventy-five percent of heritage languages are lost by the third generation. "
    "Unless you build something to keep them.",

    # Clip 5 → ps-6 (grandparents/distance)
    "Record twelve phrases. Five minutes. "
    "Grandma reads bedtime stories from a thousand miles away. Not through a screen.",

    # Clip 6 → ps-7 (voice cloning/legacy)
    "We cloned my mother's voice so my son could hear her. "
    "That voice doesn't expire. That's not a feature. That's a legacy.",

    # Clip 7 → ps-8 (this generation)
    "Teddy Ruxpin gave us a bond. Cabbage Patch made it personal. "
    "This is what this generation deserves. Built with real AI.",

    # Clip 8 → ps-9 (engineering)
    "One electronics pod. Ten plush shells. Magnetic dock. Machine washable. "
    "Volume capped. No camera. No screen. No microtransactions.",

    # Clip 9 → ps-10 (features)
    "Bluetooth sync. Parent mode. Teaching mode. "
    "Built for real kids. Built for real parents.",

    # Clip 10 → ps-11 (capisce closer)
    "Casa Companion. Kickstarter May fifth. "
    "Everyone else announced it. We built it. Capisce.",
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
            "Deep male voice. Slow, deliberate pace. New York confidence. "
            "You're a 46-year-old founder telling your story to investors and parents. "
            "Not salesy. Not rushing. Every sentence lands. Natural pauses between thoughts. "
            "Warm but authoritative. The kind of voice that makes people stop and listen."
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
