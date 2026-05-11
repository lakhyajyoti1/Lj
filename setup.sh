#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#   AI VOICE ASSISTANT - TERMUX SETUP SCRIPT
#   Run this FIRST to install all dependencies
# ============================================================

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║     AI VOICE ASSISTANT - SETUP          ║"
echo "║         Termux / Android                ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ── Step 1: Update Termux packages ─────────────────────────
echo "[1/7] Updating Termux packages..."
pkg update -y && pkg upgrade -y

# ── Step 2: Install system packages ────────────────────────
echo "[2/7] Installing system packages..."
pkg install -y python python-pip \
               portaudio \
               ffmpeg \
               sox \
               termux-api \
               clang \
               libffi \
               openssl \
               libjpeg-turbo

# ── Step 3: Install Termux:API app ─────────────────────────
echo "[3/7] Checking Termux:API..."
echo ""
echo "  ⚠  IMPORTANT: Make sure you have installed"
echo "     'Termux:API' from F-Droid or Play Store!"
echo "     (separate app from Termux itself)"
echo ""
read -p "  Press ENTER when Termux:API is installed..."

# ── Step 4: Setup storage permission ───────────────────────
echo "[4/7] Requesting storage permission..."
termux-setup-storage
sleep 2

# ── Step 5: Install Python libraries ───────────────────────
echo "[5/7] Installing Python libraries (takes a few minutes)..."
pip install --upgrade pip

pip install \
    openai \
    SpeechRecognition \
    gTTS \
    pydub \
    requests \
    python-dotenv \
    pyaudio \
    playsound==1.2.2

# ── Step 6: Create config file ─────────────────────────────
echo "[6/7] Creating config file..."

if [ ! -f ".env" ]; then
cat > .env << 'EOF'
# ── AI Voice Assistant Configuration ──────────────────────
# Get your key at: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Assistant personality (edit freely)
ASSISTANT_NAME=Aria

# AI Model: gpt-4o-mini (cheap) | gpt-4o (smarter)
AI_MODEL=gpt-4o-mini

# Language for speech recognition & TTS
LANGUAGE=en-US
TTS_LANG=en

# Wake word (say this to activate, or press Enter)
WAKE_WORD=hey aria

# Max conversation memory (number of past messages kept)
MEMORY_LIMIT=10
EOF
echo "  ✓ .env config created!"
else
echo "  ✓ .env already exists, skipping."
fi

# ── Step 7: Make scripts executable ────────────────────────
echo "[7/7] Setting permissions..."
chmod +x assistant.py
chmod +x run.sh
chmod +x test_mic.py

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║         SETUP COMPLETE! ✓               ║"
echo "╠══════════════════════════════════════════╣"
echo "║  Next steps:                            ║"
echo "║  1. Edit .env → add your OpenAI API key ║"
echo "║  2. Run: bash test_mic.py  (test mic)   ║"
echo "║  3. Run: bash run.sh       (start!)     ║"
echo "╚══════════════════════════════════════════╝"
echo ""
