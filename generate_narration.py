"""
One-time script: Generate narration MP3s for the Casa Companion 60s founder story.

Supports two backends:
  1. ElevenLabs TTS (Peter's cloned voice) — set USE_ELEVENLABS=1
  2. Azure gpt-4o-mini-tts (nova voice) — default fallback

Run once, commit the audio files, then delete this script if desired.

Usage:
    pip install httpx python-dotenv
    python generate_narration.py
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

# ====== ElevenLabs config (Peter's clone) ======
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY", "")
ELEVEN_VOICE_ID = "Yg1LMMMKIZnepfULKjaF"  # Uncle Peter v2

# ====== Azure TTS config (fallback) ======
AZURE_API_KEY = os.getenv("AZURE_API_KEY", "")
AZURE_BASE = "https://pwgcerp-9302-resource.openai.azure.com"
TTS_DEPLOYMENT = "gpt-4o-mini-tts"
TTS_API_VERSION = "2025-04-01-preview"

USE_ELEVENLABS = os.getenv("USE_ELEVENLABS", "0") == "1"

NARRATION = [
    # Scene 1: The Loss (0-10s)
    "I lost my mom to cancer when I was seventeen. I have maybe ten memories of her voice. Ten. If I could have had something that kept her voice alive when I was a kid, I would have held onto it for the rest of my life.",
    # Scene 2: The Nephews (10-18s)
    "So I cloned my voice for my nephews. Liam and Logan. Uncle Pete reading stories, even when I was miles away.",
    # Scene 3: GL (18-26s)
    "Then my son was born. And I built more. Stories in Italian, because heritage disappears in one generation if you let it. Music. Games. A whole world in a voice he trusts.",
    # Scene 4: The Reference (26-34s)
    "Teddy Ruxpin's bond. Cabbage Patch's personalization. Furby's personality. But yours. Your voice. Your family's stories.",
    # Scene 5: The Product (34-48s)
    "Casa Companion. Five animals. Three languages. Record twelve phrases and your voice lives inside a toy your child can hold, squeeze, and fall asleep with. No screen. Just your voice.",
    # Scene 6: CTA (48-60s)
    "Everyone else announced it. We built it. Your voice. Their companion.",
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio")


def generate_elevenlabs(text: str, filename: str):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.65,
            "similarity_boost": 0.85,
            "style": 0.4,
            "use_speaker_boost": True,
        },
    }
    resp = httpx.post(url, json=payload, headers=headers, timeout=60.0)
    resp.raise_for_status()
    return resp.content


def generate_azure(text: str, filename: str):
    url = f"{AZURE_BASE}/openai/deployments/{TTS_DEPLOYMENT}/audio/speech?api-version={TTS_API_VERSION}"
    headers = {
        "api-key": AZURE_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini-tts",
        "voice": "nova",
        "input": text,
        "instructions": "Speak warmly and clearly, like a founder telling his personal story in a heartfelt product video. Moderate pace, genuine emotion, pauses between sentences.",
    }
    resp = httpx.post(url, json=payload, headers=headers, timeout=60.0)
    resp.raise_for_status()
    return resp.content


def main():
    backend = "ElevenLabs (Peter's clone)" if USE_ELEVENLABS else "Azure TTS (nova)"
    print(f"Backend: {backend}\n")

    if USE_ELEVENLABS and not ELEVEN_API_KEY:
        print("ERROR: ELEVEN_API_KEY not set.")
        return
    if not USE_ELEVENLABS and not AZURE_API_KEY:
        print("ERROR: AZURE_API_KEY not set.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Generating narration audio files...\n")
    for i, text in enumerate(NARRATION, 1):
        filename = f"narration-{i}.mp3"
        print(f"Scene {i}: {text[:60]}...")

        if USE_ELEVENLABS:
            content = generate_elevenlabs(text, filename)
        else:
            content = generate_azure(text, filename)

        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(content)

        size_kb = len(content) / 1024
        print(f"  {filename}: {size_kb:.1f} KB")

    print(f"\nDone! {len(NARRATION)} files saved to {OUTPUT_DIR}/")
    if not USE_ELEVENLABS:
        print("\nNote: Using Azure TTS placeholder. Set USE_ELEVENLABS=1 when credits are available.")


if __name__ == "__main__":
    main()
