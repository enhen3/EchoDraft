#!/usr/bin/env bash

set -euo pipefail

echo "======================================"
echo "从现有应用创建 EchoDraft DMG"
echo "======================================"
echo ""

# 先重新构建应用（使用新名称）
echo "🔨 步骤 1/3: 重新构建应用（使用 EchoDraft 名称）..."
./build_mac_app.sh

echo ""
echo "📦 步骤 2/3: 准备 DMG 内容..."

# 设置变量
APP_NAME="EchoDraft"
VERSION="1.0.0"
DMG_NAME="${APP_NAME}-macOS-v${VERSION}"
TEMP_DMG="temp.dmg"
FINAL_DMG="${DMG_NAME}.dmg"
VOLUME_NAME="${APP_NAME}"
SIZE="1200m"

# 清理
rm -f "${TEMP_DMG}" "${FINAL_DMG}" "${FINAL_DMG}.sha256" 2>/dev/null || true
rm -rf dmg_temp 2>/dev/null || true

# 创建临时目录
mkdir -p dmg_temp

# 复制应用
if [ -d "dist/${APP_NAME}.app" ]; then
    echo "✅ 复制应用: dist/${APP_NAME}.app"
    cp -R "dist/${APP_NAME}.app" dmg_temp/
else
    echo "❌ 错误：应用不存在"
    exit 1
fi

# 创建使用说明
cat > dmg_temp/使用说明.txt << 'EOF'
====================================
EchoDraft - 使用说明
====================================

📦 安装步骤：

1. 将 EchoDraft.app 拖到"应用程序"文件夹
2. 首次打开：右键点击应用 → 选择"打开"
3. 在弹出对话框中再次点击"打开"
4. 开始使用！

⚠️  如果提示"文件已损坏"：

打开终端，运行：
xattr -cr /Applications/EchoDraft.app

然后双击应用即可。

✨ 主要功能：

🎙️ 本地语音转写
  - 支持 .m4a / .mp3 / .wav 格式
  - 完全离线运行，保护隐私

🌍 多语言识别
  - 自动识别中英西法德日韩俄等语言
  - 保留原语言，不做翻译

📊 实时进度
  - 可视化进度条
  - 显示检测到的语言

🎨 macOS 风格界面
  - 原生设计风格
  - 简洁易用

💻 系统要求：

- macOS 10.15+
- Apple Silicon (M1/M2/M3/M4)
- 2GB 内存
- 1.5GB 磁盘空间

📖 详细文档：
https://github.com/enhen3/EchoDraft

🆘 问题反馈：
https://github.com/enhen3/EchoDraft/issues

====================================
祝使用愉快！
====================================
EOF

# 创建 README
cat > dmg_temp/README.txt << 'EOF'
====================================
EchoDraft - Audio Transcription Tool
====================================

📦 Installation:

1. Drag EchoDraft.app to your Applications folder
2. First time: Right-click the app → Select "Open"
3. Click "Open" again in the dialog
4. Start using!

⚠️  If you see "File is damaged":

Open Terminal and run:
xattr -cr /Applications/EchoDraft.app

Then double-click the app.

✨ Features:

🎙️ Local Audio Transcription
  - Supports .m4a / .mp3 / .wav
  - Completely offline, privacy protected

🌍 Multi-language Support
  - Auto-detect Chinese, English, Spanish, French, etc.
  - Preserves original language

📊 Real-time Progress
  - Visual progress bar
  - Language detection display

🎨 macOS Native UI
  - Apple design style
  - Clean and intuitive

💻 Requirements:

- macOS 10.15+
- Apple Silicon (M1/M2/M3/M4)
- 2GB RAM
- 1.5GB Disk Space

📖 Documentation:
https://github.com/enhen3/EchoDraft

🆘 Issues:
https://github.com/enhen3/EchoDraft/issues

====================================
EOF

echo ""
echo "💿 步骤 3/3: 创建 DMG 镜像..."

# 创建初始 DMG
hdiutil create -srcfolder dmg_temp -volname "${VOLUME_NAME}" -fs HFS+ \
    -fsargs "-c c=64,a=16,e=16" -format UDRW -size ${SIZE} "${TEMP_DMG}"

# 挂载 DMG
DEVICE=$(hdiutil attach -readwrite -noverify -noautoopen "${TEMP_DMG}" | \
    egrep '^/dev/' | sed 1q | awk '{print $1}')

MOUNT_POINT="/Volumes/${VOLUME_NAME}"

# 等待挂载
sleep 2

# 设置外观
echo "🎨 设置 DMG 外观..."
osascript << EOF || true
tell application "Finder"
  tell disk "${VOLUME_NAME}"
    open
    set current view of container window to icon view
    set toolbar visible of container window to false
    set statusbar visible of container window to false
    set the bounds of container window to {100, 100, 900, 600}
    set viewOptions to the icon view options of container window
    set arrangement of viewOptions to not arranged
    set icon size of viewOptions to 128
    delay 1
    close
  end tell
end tell
EOF

# 卸载
sync
hdiutil detach "${DEVICE}" || true

# 压缩为最终版本
echo "🗜️  压缩 DMG..."
hdiutil convert "${TEMP_DMG}" -format UDZO -imagekey zlib-level=9 -o "${FINAL_DMG}"

# 清理
rm -f "${TEMP_DMG}"
rm -rf dmg_temp

# 计算校验和
echo "✅ 计算校验和..."
shasum -a 256 "${FINAL_DMG}" > "${FINAL_DMG}.sha256"

echo ""
echo "======================================"
echo "✅ DMG 创建成功！"
echo "======================================"
echo ""
ls -lh "${FINAL_DMG}"
echo ""
echo "🔐 SHA256:"
cat "${FINAL_DMG}.sha256"
echo ""
echo "📍 文件位置: $(pwd)/${FINAL_DMG}"
echo ""
echo "🎉 现在可以将这个 DMG 文件上传到 GitHub Release 了！"
echo "   这个格式比 zip 更可靠，不会出现损坏问题。"
echo ""
