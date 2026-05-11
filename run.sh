#!/data/data/com.termux/files/usr/bin/bash
# ── run.sh — Quick launcher for AI Voice Assistant ────────

cd "$(dirname "$0")"

echo ""
echo "  🚀 Starting AI Voice Assistant..."
echo "  Press Ctrl+C to stop."
echo ""

python assistant.py
