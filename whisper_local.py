from pathlib import Path
from typing import Optional, Callable

from faster_whisper import WhisperModel

from config import get_whisper_model_dir

_model: Optional[WhisperModel] = None


def _load_model() -> WhisperModel:
    """
    Load local faster-whisper model (small quantized).
    """
    model_dir = get_whisper_model_dir()
    model = WhisperModel(str(model_dir), device="cpu", compute_type="int8")
    return model


def get_model() -> WhisperModel:
    """
    Lazily load and cache Whisper model instance.
    """
    global _model
    if _model is None:
        _model = _load_model()
    return _model


def format_timestamp(seconds: float) -> str:
    """
    Convert seconds to HH:MM:SS string.
    """
    total = int(seconds or 0)
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def transcribe_audio(
    audio_path: Path,
    progress_callback: Optional[Callable[[float, str], None]] = None,
) -> str:
    """
    Transcribe audio into a timestamped transcript string.
    Each line is formatted as: [HH:MM:SS - HH:MM:SS] text

    Args:
        audio_path: Path to the audio file
        progress_callback: Optional callback function(progress_percent, detected_language)
                          Called with progress updates during transcription
    """
    model = get_model()

    # Auto-detect language with multi-language support
    # Using initial_prompt to hint the model to preserve original languages
    segments, info = model.transcribe(
        str(audio_path),
        beam_size=5,
        language=None,  # Auto-detect primary language
        task="transcribe",  # Transcribe in original language (not translate)
        vad_filter=True,  # Use voice activity detection for better accuracy
        vad_parameters=dict(min_silence_duration_ms=500),  # Adjust VAD sensitivity
    )

    # Get audio duration and detected language
    duration = info.duration if hasattr(info, "duration") else 0
    detected_language = info.language if hasattr(info, "language") else "unknown"

    lines = []
    for segment in segments:
        start = format_timestamp(segment.start)
        end = format_timestamp(segment.end)
        text = (segment.text or "").strip()
        if not text:
            continue
        lines.append(f"[{start} - {end}] {text}")

        # Report progress based on time processed
        if progress_callback and duration > 0:
            progress = min(100.0, (segment.end / duration) * 100)
            progress_callback(progress, detected_language)

    # Final progress update
    if progress_callback:
        progress_callback(100.0, detected_language)

    return "\n".join(lines)

