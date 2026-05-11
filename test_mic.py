#!/usr/bin/env python3
"""
  test_mic.py — Test microphone and speech recognition
  Run this BEFORE starting the assistant to verify setup.
"""

import os
import sys
import subprocess
import tempfile
import time

print("\n" + "═"*50)
print("  🎤  MICROPHONE & AUDIO TEST")
print("═"*50 + "\n")

# ── Test 1: Termux API available? ─────────────────────────
print("[Test 1] Checking termux-api...")
result = subprocess.run(["which", "termux-tts-speak"], capture_output=True)
if result.returncode == 0:
    print("  ✓ termux-tts-speak found")
else:
    print("  ✗ termux-api not found. Install Termux:API app + 'pkg install termux-api'")

# ── Test 2: TTS works? ────────────────────────────────────
print("\n[Test 2] Testing text-to-speech...")
print("  You should hear: 'Hello from your AI assistant'")
result = subprocess.run(
    ["termux-tts-speak", "Hello from your AI assistant"],
    capture_output=True, timeout=15
)
if result.returncode == 0:
    print("  ✓ TTS working!")
else:
    print("  ✗ TTS failed. Check Termux:API app is installed.")

# ── Test 3: Microphone recording ──────────────────────────
print("\n[Test 3] Testing microphone (say something!)...")
tmp = tempfile.mktemp(suffix=".wav")
try:
    subprocess.run(
        ["termux-microphone-record", "-l", "3", "-f", tmp],
        timeout=5, capture_output=True
    )
    time.sleep(4)
    subprocess.run(["termux-microphone-record", "-q"], capture_output=True)

    if os.path.exists(tmp) and os.path.getsize(tmp) > 0:
        print(f"  ✓ Audio recorded ({os.path.getsize(tmp)} bytes)")
        os.unlink(tmp)
    else:
        print("  ✗ No audio file created. Check microphone permission.")
except Exception as e:
    print(f"  ✗ Microphone error: {e}")

# ── Test 4: SpeechRecognition ─────────────────────────────
print("\n[Test 4] Testing SpeechRecognition library...")
try:
    import speech_recognition as sr
    r = sr.Recognizer()
    print("  ✓ SpeechRecognition imported OK")
except ImportError:
    print("  ✗ SpeechRecognition not installed. Run: pip install SpeechRecognition")

# ── Test 5: OpenAI ────────────────────────────────────────
print("\n[Test 5] Testing OpenAI library...")
try:
    import openai
    print("  ✓ OpenAI library imported OK")
except ImportError:
    print("  ✗ OpenAI not installed. Run: pip install openai")

# ── Test 6: .env config ───────────────────────────────────
print("\n[Test 6] Checking .env config...")
from dotenv import load_dotenv
load_dotenv()
key = os.getenv("OPENAI_API_KEY", "")
if key and key != "your_openai_api_key_here":
    print(f"  ✓ API key found (starts with: {key[:8]}...)")
else:
    print("  ✗ API key not set! Edit .env and add your OpenAI API key.")

# ── Summary ───────────────────────────────────────────────
print("\n" + "═"*50)
print("  Test complete!")
print("  If all ✓ → run: python assistant.py")
print("═"*50 + "\n")
