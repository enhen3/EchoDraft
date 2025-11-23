#!/usr/bin/env bash

set -euo pipefail

APP_NAME="EchoDraft"

echo "Cleaning previous build artifacts..."
rm -rf "build" "dist"

echo "Building macOS app bundle with PyInstaller..."

# Find faster-whisper assets directory
FASTER_WHISPER_ASSETS=$(python3 -c "import faster_whisper; import os; print(os.path.join(os.path.dirname(faster_whisper.__file__), 'assets'))")

python3 -m PyInstaller \
  --noconfirm \
  --windowed \
  --onedir \
  --name "${APP_NAME}" \
  --add-data "models:models" \
  --add-data "${FASTER_WHISPER_ASSETS}:faster_whisper/assets" \
  app.py

echo "Build completed."
echo "You can run the app via:"
echo "  dist/${APP_NAME}/${APP_NAME}"

