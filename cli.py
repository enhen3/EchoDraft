import sys
from typing import NoReturn

from app import run_cli


def main() -> NoReturn:
    """
    Simple CLI entry wrapper.
    Usage: python3 cli.py input.m4a
    """
    if len(sys.argv) < 2:
        print("用法：python3 cli.py <音频文件路径>")
        sys.exit(1)

    audio_file = sys.argv[1]
    run_cli(audio_file)


if __name__ == "__main__":
    main()

