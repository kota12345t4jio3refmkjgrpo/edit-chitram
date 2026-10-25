#!/usr/bin/env bash
# One-step installer for the edit-chitram Claude Code skill (Mac / Linux).
# Usage: unzip edit-chitram.zip, then run:  bash edit-chitram/install.sh
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills/edit-chitram"
echo "==> Installing edit-chitram skill to $DEST"
mkdir -p "$HOME/.claude/skills"
if [ "$SRC" != "$DEST" ]; then
  if [ -e "$DEST" ]; then
    echo "!! $DEST already exists (it may hold your learned style). Move it away first, then run again."; exit 1
  fi
  cp -R "$SRC" "$DEST"
fi
cd "$DEST"
command -v node >/dev/null || { echo "!! Node.js 18+ is required: https://nodejs.org"; exit 1; }
command -v ffmpeg >/dev/null || echo "!! ffmpeg not found — install it (Mac: brew install ffmpeg · Ubuntu: sudo apt install ffmpeg)"
echo "==> Installing renderer (Playwright + Chromium)"
npm install --silent
npx playwright-core install chromium
echo "==> Installing Python packages"
(python3 -m pip install --user numpy scipy pillow opencv-python-headless soundfile || pip3 install numpy scipy pillow opencv-python-headless soundfile) >/dev/null 2>&1 || echo "!! pip install failed — run: pip install numpy scipy pillow opencv-python-headless soundfile"
echo "==> Installing footage tools (transcription + cut-outs)"
(python3 -m pip install --user faster-whisper "rembg[cpu]" || pip3 install faster-whisper "rembg[cpu]") >/dev/null 2>&1 || echo "!! optional: pip install faster-whisper rembg[cpu] (needed for footage edits)"
echo ""
echo "✅ Done. Restart Claude Code, give it 10–12 of your videos and say: \"learn my style\"."
