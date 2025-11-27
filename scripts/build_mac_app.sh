#!/usr/bin/env bash

set -euo pipefail

# Ensure we are in the project root
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$DIR")"
cd "$PROJECT_ROOT"

APP_NAME="EchoDraft"

echo "Cleaning previous build artifacts..."
rm -rf "build" "dist"

echo "Building macOS app bundle with PyInstaller..."

# Find faster-whisper assets directory
FASTER_WHISPER_ASSETS=$(python3 -c "import faster_whisper; import os; print(os.path.join(os.path.dirname(faster_whisper.__file__), 'assets'))")

# Add src to PYTHONPATH so imports work
export PYTHONPATH="${PROJECT_ROOT}/src:${PYTHONPATH:-}"

python3 -m PyInstaller \
  --noconfirm \
  --windowed \
  --onedir \
  --name "${APP_NAME}" \
  --add-data "models:models" \
  --add-data "${FASTER_WHISPER_ASSETS}:faster_whisper/assets" \
  --paths "src" \
  src/app.py

echo "Build completed."
echo "You can run the app via:"
echo "  dist/${APP_NAME}.app/Contents/MacOS/${APP_NAME}"
