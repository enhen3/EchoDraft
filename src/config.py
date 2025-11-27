from pathlib import Path
import sys


def get_base_dir() -> Path:
    """
    Resolve the base directory of the app.
    Works both in normal Python mode and when frozen by PyInstaller.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    # Running from source in src/ directory, so project root is parent
    return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_dir()
OUTPUT_DIR = BASE_DIR / "output"


def get_models_root() -> Path:
    """
    Resolve the root directory that contains the models folder.
    This works both in normal Python runs and when packaged via PyInstaller.
    """
    candidates = []

    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        meipass = Path(getattr(sys, "_MEIPASS", exe_dir))
        candidates.extend(
            [
                exe_dir / "models",
                exe_dir / "_internal" / "models",
                exe_dir.parent / "Frameworks" / "models",
                meipass / "models",
            ]
        )
    else:
        candidates.append(BASE_DIR / "models")

    for root in candidates:
        if root.exists():
            return root
    # Default to first candidate; caller will handle existence check.
    return candidates[0]


DEFAULT_WHISPER_MODEL_DIR = get_models_root() / "whisper" / "small-int8"


def ensure_output_dir() -> Path:
    """
    Ensure the output directory exists and return its path.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def get_whisper_model_dir() -> Path:
    """
    Resolve local Whisper model directory.
    """
    env_dir = None
    # 将来如果需要支持自定义模型路径，可以通过环境变量 WHISPER_MODEL_DIR 扩展
    # 这里先固定为 DEFAULT_WHISPER_MODEL_DIR，保证行为简单稳定。
    if env_dir:
        model_dir = Path(env_dir).expanduser()
    else:
        model_dir = DEFAULT_WHISPER_MODEL_DIR

    if not model_dir.exists():
        raise FileNotFoundError(
            f"Whisper 模型目录不存在: {model_dir}\n"
            "请下载 small 模型（例如 small-int8），并放在 models/whisper/ 目录下。\n"
            "参考 README.md 中的模型下载说明。"
        )
    return model_dir
