# 🎙 AI Voice Assistant — Termux / Android

A fully working AI voice assistant that runs on your Android phone
inside **Termux** — no PC needed.

---

## 📁 Files

| File | Purpose |
|------|---------|
| `setup.sh` | Install all dependencies (run FIRST) |
| `assistant.py` | Main AI voice assistant |
| `test_mic.py` | Test microphone & setup |
| `run.sh` | Quick launcher |
| `.env` | Your config & API key |

---

## 📱 Requirements

- Android phone (Android 7+)
- **Termux** app → Install from [F-Droid](https://f-droid.org/packages/com.termux/) *(recommended)*
- **Termux:API** app → Install from [F-Droid](https://f-droid.org/packages/com.termux.api/)
- Internet connection (for OpenAI API + Google Speech)
- OpenAI API key → [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

> ⚠️ Use F-Droid versions. Play Store Termux is outdated.

---

## 🚀 Setup (Step by Step)

### Step 1 — Install Apps
1. Install **Termux** from F-Droid
2. Install **Termux:API** from F-Droid
3. Open Termux

### Step 2 — Copy files to Termux
```bash
# In Termux, go to home folder
cd ~

# Create a folder for the assistant
mkdir voice-assistant
cd voice-assistant
```

Copy all 5 files into this folder using any of:
- **Termux file access**: `cp /sdcard/Download/assistant.py .`
- **Termux SSH**: connect from PC and transfer files
- **nano editor**: paste content directly in Termux

### Step 3 — Run setup
```bash
bash setup.sh
```
This installs Python, libraries, and all dependencies automatically.

### Step 4 — Add your API key
```bash
nano .env
```
Replace `your_openai_api_key_here` with your real OpenAI API key.
Press `Ctrl+X → Y → Enter` to save.

### Step 5 — Test microphone
```bash
python test_mic.py
```
Check all tests show ✓.

### Step 6 — Start the assistant!
```bash
bash run.sh
# OR
python assistant.py
```

---

## 🗣 How to Use

Once started, the assistant will:
1. **Speak a greeting** out loud
2. **Listen** for your voice (3 seconds recording)
3. **Transcribe** your speech using Google
4. **Send** it to ChatGPT (OpenAI)
5. **Speak** the reply back

If microphone fails → it falls back to **keyboard typing**.

### Voice Commands
| Say | What happens |
|-----|-------------|
| `quit` / `bye` | Stop the assistant |
| `clear` / `reset` | Forget conversation history |
| `history` | How many exchanges so far |
| `time` | Current time |
| `date` | Today's date |

---

## ⚙️ Customize

Edit `.env` to change:

```env
ASSISTANT_NAME=Jarvis        # Change the name
AI_MODEL=gpt-4o              # Use smarter model
LANGUAGE=hi-IN               # Hindi speech recognition
TTS_LANG=hi                  # Hindi text-to-speech
MEMORY_LIMIT=20              # Remember more conversation
```

Edit the `SYSTEM_PROMPT` in `assistant.py` to change the personality.

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| `termux-tts-speak: not found` | Install Termux:API app + `pkg install termux-api` |
| Microphone permission denied | Run `termux-setup-storage` and allow permissions in Android settings |
| `pip install` fails | Run `pkg install python clang libffi` first |
| Speech not recognized | Check internet connection; try typing instead |
| OpenAI error 401 | API key wrong or expired — check `.env` |
| OpenAI error 429 | Rate limited — wait or upgrade OpenAI plan |
| Audio not playing | Try `pkg install sox ffmpeg` |

---

## 💰 Cost Estimate

Using `gpt-4o-mini` (recommended):
- ~100 voice exchanges ≈ **$0.01–0.05**
- Very affordable for daily use

---

## 🔒 Privacy

- Voice is transcribed by **Google Speech Recognition** (online)
- Text is sent to **OpenAI** servers
- No data stored permanently on your phone beyond the session

---

## 📞 How Speech Works (Flow)

```
Your Voice
    ↓
termux-microphone-record (3s WAV)
    ↓
Google Speech Recognition (online)
    ↓  text
OpenAI GPT API
    ↓  reply text
termux-tts-speak (Android TTS)
    ↓
You hear the answer 🔊
```

---

*Built for Termux on Android. No root required.*
