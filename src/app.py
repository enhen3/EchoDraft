import argparse
import sys
from pathlib import Path

from PyQt6 import QtWidgets, QtCore, QtGui

from audio_utils import validate_audio_file
from config import ensure_output_dir
from whisper_local import transcribe_audio


# macOS-style color palette
COLORS = {
    "bg": "#FFFFFF",
    "surface": "#F5F5F7",
    "primary": "#007AFF",
    "primary_hover": "#0051D5",
    "text": "#1D1D1F",
    "text_secondary": "#86868B",
    "border": "#D2D2D7",
    "success": "#34C759",
}

# macOS-style stylesheet
MACOS_STYLE = f"""
QMainWindow {{
    background-color: {COLORS['bg']};
}}

QWidget {{
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
    font-size: 13px;
    color: {COLORS['text']};
}}

QLabel {{
    color: {COLORS['text']};
    font-size: 13px;
}}

QLabel#title {{
    font-size: 20px;
    font-weight: 600;
    color: {COLORS['text']};
    padding: 10px 0;
}}

QLabel#statusLabel {{
    color: {COLORS['text_secondary']};
    font-size: 12px;
}}

QLineEdit {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    color: {COLORS['text']};
}}

QLineEdit:focus {{
    border: 2px solid {COLORS['primary']};
    padding: 7px 11px;
}}

QPushButton {{
    background-color: {COLORS['primary']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
}}

QPushButton:hover {{
    background-color: {COLORS['primary_hover']};
}}

QPushButton:pressed {{
    background-color: {COLORS['primary_hover']};
}}

QPushButton:disabled {{
    background-color: {COLORS['border']};
    color: {COLORS['text_secondary']};
}}

QPushButton#secondaryButton {{
    background-color: {COLORS['surface']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
}}

QPushButton#secondaryButton:hover {{
    background-color: #E8E8ED;
}}

QPlainTextEdit {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 12px;
    font-size: 13px;
    line-height: 1.5;
    color: {COLORS['text']};
}}

QProgressBar {{
    border: none;
    border-radius: 4px;
    background-color: {COLORS['surface']};
    height: 8px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {COLORS['primary']};
    border-radius: 4px;
}}
"""


def save_transcript(audio_path: Path, transcript: str) -> Path:
    """
    Write transcript to a markdown file and return its path.
    In app mode: saves to ~/Documents/EchoDraft/
    In dev mode: saves to output/ directory.
    """
    output_dir = ensure_output_dir()
    base_name = audio_path.stem

    out_path = output_dir / f"{base_name}_transcript.md"
    out_path.write_text(transcript, encoding="utf-8")
    return out_path


def run_cli(audio_file: str) -> None:
    """
    CLI entry: transcribe audio and print transcript.
    """
    try:
        audio_path = validate_audio_file(audio_file)
        print(f"音频文件：{audio_path}")
        print("开始转写，请稍候...")

        def progress_callback(progress: float, language: str) -> None:
            print(f"\r进度: {progress:.1f}% (检测到语言: {language})", end="", flush=True)

        transcript = transcribe_audio(audio_path, progress_callback=progress_callback)
        print()  # New line after progress

        out_path = save_transcript(audio_path, transcript)

        print("转写完成，结果已保存：")
        print(f"  transcript: {out_path}")

        print("\n=== 转写全文 ===\n")
        print(transcript or "(转写结果为空)")

    except Exception as exc:
        print(f"\n发生错误：{exc}", file=sys.stderr)
        sys.exit(1)


class TranscribeWorker(QtCore.QThread):
    """
    Background worker thread for audio transcription.
    """

    progress_updated = QtCore.pyqtSignal(float, str)  # progress, language
    finished = QtCore.pyqtSignal(str)  # transcript
    error = QtCore.pyqtSignal(str)  # error message

    def __init__(self, audio_path: Path) -> None:
        super().__init__()
        self.audio_path = audio_path

    def run(self) -> None:
        try:
            transcript = transcribe_audio(
                self.audio_path, progress_callback=self._progress_callback
            )
            self.finished.emit(transcript)
        except Exception as exc:
            self.error.emit(str(exc))

    def _progress_callback(self, progress: float, language: str) -> None:
        self.progress_updated.emit(progress, language)


class MainWindow(QtWidgets.QMainWindow):
    """
    PyQt6-based main window for the transcriber with macOS styling.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("EchoDraft")
        self.resize(900, 700)

        # Apply macOS style
        self.setStyleSheet(MACOS_STYLE)

        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)

        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QtWidgets.QLabel("音频转写工具", self)
        title.setObjectName("title")
        layout.addWidget(title)

        # File selection area
        file_group = QtWidgets.QWidget(self)
        file_layout = QtWidgets.QVBoxLayout(file_group)
        file_layout.setContentsMargins(0, 0, 0, 0)
        file_layout.setSpacing(8)

        file_label = QtWidgets.QLabel("音频文件", self)
        file_layout.addWidget(file_label)

        file_row = QtWidgets.QHBoxLayout()
        file_row.setSpacing(10)

        self.path_edit = QtWidgets.QLineEdit(self)
        self.path_edit.setPlaceholderText("选择 .m4a / .mp3 / .wav 文件")
        file_row.addWidget(self.path_edit, stretch=1)

        self.browse_btn = QtWidgets.QPushButton("浏览", self)
        self.browse_btn.setObjectName("secondaryButton")
        self.browse_btn.clicked.connect(self.browse_file)
        file_row.addWidget(self.browse_btn)

        file_layout.addLayout(file_row)
        layout.addWidget(file_group)

        # Progress bar
        progress_group = QtWidgets.QWidget(self)
        progress_layout = QtWidgets.QVBoxLayout(progress_group)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(8)

        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QtWidgets.QLabel("就绪", self)
        self.status_label.setObjectName("statusLabel")
        progress_layout.addWidget(self.status_label)

        layout.addWidget(progress_group)

        # Start button
        self.start_btn = QtWidgets.QPushButton("开始转写", self)
        self.start_btn.clicked.connect(self.start_transcribe)
        self.start_btn.setMinimumHeight(40)
        layout.addWidget(self.start_btn)

        # Transcript area with copy button
        transcript_header = QtWidgets.QHBoxLayout()
        transcript_label = QtWidgets.QLabel("转写结果", self)
        transcript_header.addWidget(transcript_label)
        transcript_header.addStretch()

        self.copy_btn = QtWidgets.QPushButton("📋 复制全部", self)
        self.copy_btn.setObjectName("secondaryButton")
        self.copy_btn.setMaximumWidth(120)
        self.copy_btn.clicked.connect(self.copy_transcript)
        self.copy_btn.setEnabled(False)
        transcript_header.addWidget(self.copy_btn)

        layout.addLayout(transcript_header)

        self.text_edit = QtWidgets.QPlainTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlaceholderText("转写结果将在此处显示...")
        layout.addWidget(self.text_edit, stretch=1)

        self.worker = None

    def copy_transcript(self) -> None:
        """Copy transcript text to clipboard."""
        text = self.text_edit.toPlainText()
        if text:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(text)
            # Show temporary success message
            original_text = self.copy_btn.text()
            self.copy_btn.setText("✓ 已复制!")
            QtCore.QTimer.singleShot(2000, lambda: self.copy_btn.setText(original_text))

    def browse_file(self) -> None:
        dlg = QtWidgets.QFileDialog(self, "选择音频文件")
        dlg.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        dlg.setNameFilter("Audio Files (*.m4a *.mp3 *.wav);;All Files (*)")
        if dlg.exec():
            files = dlg.selectedFiles()
            if files:
                self.path_edit.setText(files[0])

    def start_transcribe(self) -> None:
        audio_path_str = self.path_edit.text().strip()
        try:
            audio_path = validate_audio_file(audio_path_str)
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "错误", str(exc))
            return

        # Disable UI during transcription
        self.start_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        self.path_edit.setEnabled(False)
        self.copy_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("正在加载模型...")
        self.text_edit.clear()

        # Start background worker
        self.worker = TranscribeWorker(audio_path)
        self.worker.progress_updated.connect(self.on_progress_updated)
        self.worker.finished.connect(self.on_transcribe_finished)
        self.worker.error.connect(self.on_transcribe_error)
        self.worker.start()

    def on_progress_updated(self, progress: float, language: str) -> None:
        self.progress_bar.setValue(int(progress))
        lang_name = self.get_language_name(language)
        self.status_label.setText(f"转写中... {progress:.0f}% (检测到语言: {lang_name})")

    def on_transcribe_finished(self, transcript: str) -> None:
        try:
            audio_path = Path(self.path_edit.text())
            out_path = save_transcript(audio_path, transcript)

            self.text_edit.setPlainText(transcript or "")
            self.status_label.setText(f"✓ 转写完成！已保存至: {out_path.name}")

            # Enable copy button if there's content
            self.copy_btn.setEnabled(bool(transcript))
        except Exception as exc:
            self.status_label.setText(f"保存失败: {exc}")

        # Re-enable UI
        self.start_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        self.path_edit.setEnabled(True)
        self.progress_bar.setVisible(False)

    def on_transcribe_error(self, error_msg: str) -> None:
        QtWidgets.QMessageBox.critical(self, "转写失败", error_msg)
        self.status_label.setText("转写失败")

        # Re-enable UI
        self.start_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        self.path_edit.setEnabled(True)
        self.progress_bar.setVisible(False)

    @staticmethod
    def get_language_name(code: str) -> str:
        """Convert language code to readable name."""
        lang_map = {
            "zh": "中文",
            "en": "English",
            "es": "Español",
            "fr": "Français",
            "de": "Deutsch",
            "ja": "日本語",
            "ko": "한국어",
            "ru": "Русский",
            "pt": "Português",
            "it": "Italiano",
        }
        return lang_map.get(code, code)


def launch_gui() -> None:
    """
    Launch PyQt6-based desktop app.
    """
    app = QtWidgets.QApplication(sys.argv)

    # Set app-wide font for better macOS integration
    font = QtGui.QFont(".AppleSystemUIFont", 13)
    app.setFont(font)

    window = MainWindow()
    window.show()
    app.exec()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="本地 Whisper 语音转写工具（支持 GUI 与 CLI）"
    )
    parser.add_argument(
        "--cli",
        metavar="AUDIO_FILE",
        help="以命令行模式运行分析，如：python3 app.py --cli input.m4a",
    )
    args, unknown = parser.parse_known_args()

    # When packaged with PyInstaller, multiprocessing may invoke the program
    # internally with additional arguments (e.g. resource_tracker). In that
    # case we simply exit silently.
    if unknown and "-c" in unknown and "multiprocessing.resource_tracker" in " ".join(
        unknown
    ):
        return

    if args.cli:
        run_cli(args.cli)
    else:
        launch_gui()


if __name__ == "__main__":
    main()
