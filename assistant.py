#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════╗
║        AI VOICE ASSISTANT - assistant.py        ║
║   Runs on Android via Termux + Termux:API       ║
╚══════════════════════════════════════════════════╝

Features:
  • Speech-to-text (microphone input)
  • GPT-powered AI responses (OpenAI)
  • Text-to-speech output (gTTS + ffmpeg)
  • Conversation memory
  • Wake word detection
  • Termux notification support
"""

import os
import sys
import time
import json
import subprocess
import tempfile
import logging
from datetime import datetime
from pathlib import Path

# ── Load environment variables ─────────────────────────────
from dotenv import load_dotenv
load_dotenv()

import openai
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

# ══════════════════════════════════════════════════════════
#  CONFIGURATION
# ══════════════════════════════════════════════════════════
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Aria")
AI_MODEL       = os.getenv("AI_MODEL", "gpt-4o-mini")
LANGUAGE       = os.getenv("LANGUAGE", "en-US")
TTS_LANG       = os.getenv("TTS_LANG", "en")
WAKE_WORD      = os.getenv("WAKE_WORD", "hey aria").lower()
MEMORY_LIMIT   = int(os.getenv("MEMORY_LIMIT", "10"))

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("VoiceAssistant")

# ══════════════════════════════════════════════════════════
#  SYSTEM PROMPT  (personality of your assistant)
# ══════════════════════════════════════════════════════════
SYSTEM_PROMPT = f"""You are {ASSISTANT_NAME}, a smart, friendly, and concise AI voice assistant running on an Android phone via Termux.

Guidelines:
- Keep responses SHORT and spoken naturally (2-4 sentences max unless user asks for detail)
- Avoid markdown, bullet points, or symbols — only plain spoken text
- Be warm, helpful, and slightly witty
- If asked the time/date, provide it directly
- If you don't know something, say so honestly
- Today's date: {datetime.now().strftime("%A, %B %d, %Y")}
"""

# ══════════════════════════════════════════════════════════
#  VOICE ASSISTANT CLASS
# ══════════════════════════════════════════════════════════
class VoiceAssistant:
    def __init__(self):
        # Validate API key
        if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
            print("\n❌ ERROR: OpenAI API key not set!")
            print("   Edit the .env file and add your key.")
            print("   Get one at: https://platform.openai.com/api-keys\n")
            sys.exit(1)

        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.recognizer = sr.Recognizer()
        self.conversation_history = []
        self.is_running = True
        self.session_start = datetime.now()

        # Tune recognizer sensitivity
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        self._banner()

    # ── Print startup banner ───────────────────────────────
    def _banner(self):
        print("\n" + "═"*50)
        print(f"  🎙  {ASSISTANT_NAME} — AI Voice Assistant")
        print(f"  Model : {AI_MODEL}")
        print(f"  Lang  : {LANGUAGE}")
        print(f"  Wake  : '{WAKE_WORD}' (or press Enter)")
        print("═"*50)
        print("  Commands: 'quit' | 'clear' | 'history'")
        print("═"*50 + "\n")

    # ── Send Termux notification ───────────────────────────
    def notify(self, title, message):
        try:
            subprocess.run(
                ["termux-notification",
                 "--title", title,
                 "--content", message,
                 "--priority", "default"],
                capture_output=True, timeout=5
            )
        except Exception:
            pass  # Notification is optional

    # ── Text-to-Speech ─────────────────────────────────────
    def speak(self, text):
        """Convert text to speech and play it."""
        if not text.strip():
            return
        print(f"\n  🔊 {ASSISTANT_NAME}: {text}\n")
        try:
            # Method 1: Use Termux TTS (fastest, no internet)
            result = subprocess.run(
                ["termux-tts-speak", text],
                capture_output=True, timeout=30
            )
            if result.returncode == 0:
                return
        except Exception:
            pass

        # Method 2: gTTS fallback (requires internet)
        try:
            tts = gTTS(text=text, lang=TTS_LANG, slow=False)
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                tts.save(f.name)
                tmp_path = f.name

            # Play via termux-media-player or ffmpeg
            played = False
            try:
                subprocess.run(
                    ["termux-media-player", "play", tmp_path],
                    timeout=60, capture_output=True
                )
                time.sleep(len(text) * 0.06 + 1)
                played = True
            except Exception:
                pass

            if not played:
                try:
                    subprocess.run(
                        ["ffplay", "-nodisp", "-autoexit", tmp_path],
                        capture_output=True, timeout=60
                    )
                except Exception:
                    pass

            os.unlink(tmp_path)
        except Exception as e:
            log.warning(f"TTS failed: {e}")
            print(f"  [TTS unavailable — response shown above]")

    # ── Speech Recognition via Microphone ─────────────────
    def listen(self, prompt="Listening..."):
        """Record microphone and return transcribed text."""
        print(f"  🎤 {prompt}")
        try:
            with sr.Microphone() as source:
                # Short ambient noise calibration
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                try:
                    audio = self.recognizer.listen(
                        source,
                        timeout=8,
                        phrase_time_limit=15
                    )
                except sr.WaitTimeoutError:
                    return ""

            # Try Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(
                    audio,
                    language=LANGUAGE
                )
                print(f"  👤 You said: {text}")
                return text.strip()
            except sr.UnknownValueError:
                print("  [Could not understand audio]")
                return ""
            except sr.RequestError as e:
                print(f"  [Speech service error: {e}]")
                return ""

        except OSError as e:
            # Microphone not available — fall back to text input
            log.warning(f"Microphone error: {e}")
            return ""

    # ── Termux TTS microphone via termux-mic-record ────────
    def listen_termux(self):
        """Alternative: record with termux-microphone-record."""
        tmp = tempfile.mktemp(suffix=".wav")
        try:
            print("  🎤 Recording... (3 seconds)")
            subprocess.run(
                ["termux-microphone-record",
                 "-l", "3", "-f", tmp],
                timeout=8, capture_output=True
            )
            time.sleep(3.5)
            subprocess.run(
                ["termux-microphone-record", "-q"],
                capture_output=True
            )
            if not os.path.exists(tmp):
                return ""

            with sr.AudioFile(tmp) as source:
                audio = self.recognizer.record(source)
            os.unlink(tmp)

            text = self.recognizer.recognize_google(
                audio, language=LANGUAGE
            )
            print(f"  👤 You said: {text}")
            return text.strip()

        except Exception as e:
            log.warning(f"termux-mic-record failed: {e}")
            if os.path.exists(tmp):
                os.unlink(tmp)
            return ""

    # ── Ask OpenAI ─────────────────────────────────────────
    def ask_ai(self, user_text):
        """Send text to OpenAI and get a response."""
        # Add to history
        self.conversation_history.append({
            "role": "user",
            "content": user_text
        })

        # Trim history to memory limit
        if len(self.conversation_history) > MEMORY_LIMIT * 2:
            self.conversation_history = self.conversation_history[-(MEMORY_LIMIT * 2):]

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(self.conversation_history)

        try:
            print("  ⏳ Thinking...")
            response = self.client.chat.completions.create(
                model=AI_MODEL,
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            reply = response.choices[0].message.content.strip()

            # Save assistant reply to history
            self.conversation_history.append({
                "role": "assistant",
                "content": reply
            })
            return reply

        except openai.AuthenticationError:
            return "My API key seems invalid. Please check your dot-env file."
        except openai.RateLimitError:
            return "I'm being rate limited right now. Please wait a moment."
        except openai.APIConnectionError:
            return "I can't reach the internet right now. Check your connection."
        except Exception as e:
            log.error(f"OpenAI error: {e}")
            return "Sorry, something went wrong on my end."

    # ── Handle special commands ────────────────────────────
    def handle_command(self, text):
        """Returns True if it was a special command."""
        t = text.lower().strip()

        if t in ("quit", "exit", "bye", "goodbye", "stop"):
            self.speak(f"Goodbye! Have a great day!")
            self.is_running = False
            return True

        if t in ("clear", "reset", "forget"):
            self.conversation_history.clear()
            self.speak("Conversation cleared. Fresh start!")
            return True

        if t in ("history", "what did we talk about"):
            count = len(self.conversation_history) // 2
            self.speak(f"We've exchanged {count} message pairs this session.")
            return True

        if t in ("time", "what time is it"):
            now = datetime.now().strftime("%I:%M %p")
            self.speak(f"It's {now}")
            return True

        if t in ("date", "what's the date", "what is the date"):
            today = datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"Today is {today}")
            return True

        return False

    # ── Get input (voice + text fallback) ─────────────────
    def get_input(self):
        """Try voice first, fall back to keyboard."""
        # Try Termux microphone API first
        text = self.listen_termux()
        if not text:
            # Try standard PyAudio microphone
            text = self.listen()
        if not text:
            # Keyboard fallback
            try:
                text = input("  ⌨  Type your message: ").strip()
            except (EOFError, KeyboardInterrupt):
                return "quit"
        return text

    # ── Main conversation loop ─────────────────────────────
    def run(self):
        """Start the assistant."""
        self.speak(f"Hello! I'm {ASSISTANT_NAME}, your AI assistant. How can I help you?")
        self.notify(f"{ASSISTANT_NAME} Started", "Your AI assistant is ready!")

        while self.is_running:
            try:
                print("\n" + "─"*50)
                user_input = self.get_input()

                if not user_input:
                    continue

                # Check for special commands
                if self.handle_command(user_input):
                    continue

                # Send to AI and speak reply
                reply = self.ask_ai(user_input)
                self.speak(reply)

            except KeyboardInterrupt:
                print("\n\n  Interrupted by user.")
                self.speak("Shutting down. Goodbye!")
                break
            except Exception as e:
                log.error(f"Loop error: {e}")
                print(f"  ⚠ Error: {e}")

        print("\n  Session ended. Goodbye!\n")


# ══════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
