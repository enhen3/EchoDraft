# EchoDraft

**EchoDraft** 是一个基于 macOS 的本地语音转写工具，拥有漂亮的原生界面。它能够将音频文件（.m4a, .mp3, .wav）快速转换为文字，支持多种语言自动识别。

![EchoDraft Screenshot](https://via.placeholder.com/800x500?text=EchoDraft+Screenshot)

## ✨ 功能特点

- **本地运行**：基于 `faster-whisper`，所有处理都在本地完成，保护隐私，无需联网。
- **多语言支持**：自动识别中文、英文、日语、韩语、法语、德语等多种语言。
- **macOS 风格 UI**：原生 PyQt6 界面，完美融入 macOS 生态。
- **格式支持**：支持常见的音频格式 `.m4a`, `.mp3`, `.wav`。
- **导出方便**：一键复制全文，自动保存 Markdown 格式的转写记录。

## 🚀 快速开始

### 方法一：直接下载应用 (推荐)

请前往 [Releases](https://github.com/enhen3/EchoDraft/releases) 页面下载最新的版本。

**📥 下载说明：**
在 Assets 列表中，你可能会看到多个文件：
- ✅ **`EchoDraft-macOS-vX.X.X.dmg`**：**请下载这个文件**。这是 macOS 的安装程序，下载后即可直接使用。
- ❌ `Source code (zip)` / `Source code (tar.gz)`：这是源代码，仅供开发者研究使用，普通用户**无需下载**。

**📦 安装步骤：**
1. 下载 `.dmg` 文件。
2. 双击打开，将 `EchoDraft.app` 拖入应用程序文件夹。
3. 首次打开时，如果提示“无法打开”或“文件已损坏”：
   - 这通常是因为 macOS 的安全机制。
   - 请打开“系统设置” -> “隐私与安全性”，在下方点击“仍要打开”。
   - 或者在终端中运行以下命令（修复权限）：
     ```bash
     xattr -cr /Applications/EchoDraft.app
     ```
   - 然后再次打开应用即可。
4. 开始使用！

### 方法二：从源码运行

如果你是开发者，或者想要自己构建应用，请按照以下步骤操作：

#### 1. 环境要求

- macOS 10.15+ (支持 Apple Silicon 和 Intel)
- Python 3.9+
- 建议使用虚拟环境

#### 2. 安装依赖

```bash
# 克隆仓库
git clone https://github.com/enhen3/EchoDraft.git
cd EchoDraft

# 创建并激活虚拟环境 (可选)
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 3. 下载模型

由于模型文件较大，未包含在仓库中。请运行以下脚本下载 Whisper 模型 (small-int8)：

```bash
python3 src/download_model.py
```

#### 4. 运行应用

```bash
python3 src/app.py
```

## 🛠️ 构建指南

如果你想打包自己的 `.app` 或 `.dmg`：

1. 确保已安装所有依赖和模型。
2. 运行构建脚本：

```bash
# 构建 .app
./scripts/build_mac_app.sh

# 打包为 .dmg (需先完成上一步)
./scripts/create_dmg.sh
```

构建完成后，文件位于 `dist/` 目录下。

## 📂 项目结构

```
EchoDraft/
├── src/                # 源代码
│   ├── app.py          # GUI 入口
│   ├── whisper_local.py# 转写逻辑
│   ├── config.py       # 配置
│   └── ...
├── scripts/            # 构建与辅助脚本
│   ├── build_mac_app.sh
│   └── create_dmg.sh
├── models/             # 模型文件 (需自行下载)
└── requirements.txt    # Python 依赖
```

## 📄 许可证

MIT License
