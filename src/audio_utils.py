from pathlib import Path
from typing import Set

SUPPORTED_EXTENSIONS: Set[str] = {".m4a", ".mp3", ".wav"}


def is_supported_audio_file(path: Path) -> bool:
    """
    Return True if path is an existing supported audio file.
    """
    return path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS


def validate_audio_file(path_str: str) -> Path:
    """
    Validate that the given path string points to a supported audio file.
    """
    if not path_str:
        raise ValueError("请先选择一个音频文件。")

    path = Path(path_str).expanduser()

    if not path.exists():
        raise ValueError(f"音频文件不存在：{path}")
    if not path.is_file():
        raise ValueError(f"路径不是文件：{path}")
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        exts = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(f"不支持的音频格式：{path.suffix}，目前支持：{exts}")

    return path

