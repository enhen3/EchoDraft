import shutil
from pathlib import Path
from faster_whisper import download_model
from config import DEFAULT_WHISPER_MODEL_DIR

def main():
    print(f"Preparing to download Whisper model to: {DEFAULT_WHISPER_MODEL_DIR}")
    
    # Ensure parent directory exists
    DEFAULT_WHISPER_MODEL_DIR.parent.mkdir(parents=True, exist_ok=True)

    # faster_whisper.download_model returns the path to the downloaded model
    # We want to ensure it ends up in models/whisper/small-int8
    # download_model("small", ...) usually downloads to cache or specific dir.
    
    print("Downloading 'small' model (int8 quantization)...")
    try:
        # Download to the specific directory we want
        # output_dir logic in faster-whisper: if provided, it downloads THERE.
        # It doesn't append the model name if output_dir is explicit.
        # So we point directly to DEFAULT_WHISPER_MODEL_DIR
        path = download_model("small", output_dir=str(DEFAULT_WHISPER_MODEL_DIR))
        print(f"Model downloaded successfully to: {path}")
    except Exception as e:
        print(f"Error downloading model: {e}")
        print("Please check your network connection.")

if __name__ == "__main__":
    main()

