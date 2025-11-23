# EchoDraft - 本地语音转写工具

本项目在本地运行 Whisper small 模型完成音频转写，将音频文件转换为带时间戳的完整文字稿。支持基于 PyQt6 的现代化图形界面（GUI）与 CLI 两种使用方式，适用于在本地对访谈、录音等进行快速转写。

## ✨ 主要特性

- 🌍 **自动语言检测** - 支持中文、英语、西班牙语、法语等多种语言自动识别
- 📊 **实时进度显示** - 可视化进度条和百分比显示，清楚了解转写进度
- 🎨 **macOS 风格界面** - 采用苹果设计风格，简洁美观
- ⚡ **后台处理** - 使用多线程技术，界面流畅不卡顿
- 🔒 **完全本地运行** - 所有数据在本地处理，保护隐私安全

## 一、环境与依赖

1. 建议使用 Python 3.9+。
2. 可选：创建虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
# Windows: .venv\Scripts\activate
```

3. 安装依赖（依赖 faster-whisper 和 PyQt6）：

```bash
pip install -r requirements.txt
```

## 二、下载并配置 Whisper small 模型

本项目使用本地 faster-whisper small 量化模型（例如 small-int8）。

1. 在 Hugging Face 下载模型（示例）：

- https://huggingface.co/guillaumekln/faster-whisper-small

2. 在项目根目录创建模型目录结构：

```bash
mkdir -p models/whisper
```

3. 将下载好的模型文件放入子目录，例如：

```bash
models/whisper/small-int8/
```

默认代码会从 `models/whisper/small-int8` 读取模型。  
如需自定义目录，可设置环境变量：

```bash
export WHISPER_MODEL_DIR="自定义模型目录路径"
```

## 三、运行方式（Python 直接运行）

### 1. GUI 模式（推荐）

在项目根目录执行：

```bash
python3 app.py
```

然后在界面中：

- 点击「浏览」按钮选择 `.m4a` / `.mp3` / `.wav` 文件
- 点击「开始转写」
- 实时查看转写进度条和检测到的语言
- 转写完成后，结果会显示在界面中，同时自动保存到 `output/` 目录

**界面特点：**
- 采用 macOS 风格设计，简洁美观
- 实时进度条显示转写进度百分比
- 自动检测音频语言（中文、英语、西班牙语等）
- 后台处理，界面不会卡顿
- 转写过程中按钮自动禁用，防止重复操作

同时会在 `output/` 目录下生成一个 Markdown 文件：`<文件名>_transcript.md`

若 `output/` 不存在，程序会自动创建。

### 2. CLI 模式

在项目根目录执行：

```bash
python3 app.py --cli input.m4a
# 或
python3 cli.py input.m4a
```

程序将：

- 本地使用 Whisper small 模型完成转写。
- 将转写结果写入 `output/` 目录（`<文件名>_transcript.md`）。
- 在终端中打印完整转写文本。

## 四、打包为 macOS 应用（.app，可选）

如果希望获得一个可双击启动的 `.app` 应用，可以使用 PyInstaller 进行打包：

1. 安装 PyInstaller（只需在开发机执行一次）：

```bash
python3 -m pip install pyinstaller
```

2. 在项目根目录执行打包脚本：

```bash
./build_mac_app.sh
```

完成后，在 `dist/` 目录下会生成：

- `dist/EchoDraft.app` – 可在 Finder 中双击运行的 GUI 应用。
- `dist/EchoDraft/EchoDraft` – 终端下可执行的独立二进制，可配合 `--cli` 使用。

模型文件会随应用一同打包，无需额外拷贝。

## 五、项目结构

```text
project_root/
  app.py              # GUI + CLI 主入口
  cli.py              # 纯命令行入口包装
  audio_utils.py      # 音频文件检测 / 格式校验
  whisper_local.py    # 本地 faster-whisper 推理逻辑
  config.py           # 路径与配置（模型、输出目录，兼容打包后的路径）
  requirements.txt    # Python 依赖列表
  README.md           # 使用说明
  models/
    whisper/          # 存放 small 模型（例如 small-int8）
  output/             # 输出目录（自动创建）
```

所有路径均基于当前文件相对推导，不依赖任何硬编码绝对路径，可直接复制整个工程到另一台 macOS 机器运行，或在另一台机器上重新打包为 `.app`。

## 六、常见错误排查

- **错误：Whisper 模型目录不存在**
  - 解决：确认已创建 `models/whisper/small-int8/` 并放入 small 模型文件。

- **错误：不支持的音频格式**
  - 解决：目前仅支持 `.m4a`、`.mp3`、`.wav`，请先转换格式后再导入。

如果遇到 faster-whisper 报错提示缺少音频解码依赖，可根据提示选择性安装相关库（如 ffmpeg），但本项目本身不依赖任何额外系统命令行工具。
