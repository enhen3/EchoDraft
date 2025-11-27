#!/usr/bin/env bash

set -euo pipefail

# Ensure we are in the project root
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$DIR")"
cd "$PROJECT_ROOT"

echo "======================================"
echo "创建 EchoDraft DMG 镜像文件"
echo "======================================"
echo ""

# 检查dist目录中的app是否存在
if [ ! -d "dist/EchoDraft.app" ]; then
    echo "❌ 错误：dist/EchoDraft.app 不存在"
    echo "请先运行 ./scripts/build_mac_app.sh 创建应用"
    exit 1
fi

echo "📦 找到应用: dist/EchoDraft.app"
echo ""

# 设置变量
APP_NAME="EchoDraft"
VERSION="1.0.0"
DMG_NAME="${APP_NAME}-macOS-v${VERSION}"
TEMP_DMG="temp.dmg"
FINAL_DMG="${DMG_NAME}.dmg"
VOLUME_NAME="${APP_NAME}"
SOURCE_FOLDER="dist/${APP_NAME}.app"
SIZE="1200m"  # DMG 大小（应用约1GB，留一些余量）

echo "🗑️  清理旧文件..."
rm -f "${TEMP_DMG}" "${FINAL_DMG}"

echo "📁 创建临时挂载目录..."
mkdir -p dmg_temp
cp -R "${SOURCE_FOLDER}" dmg_temp/

# 创建使用说明
cat > dmg_temp/使用说明.txt << 'EOF'
====================================
EchoDraft - 使用说明
====================================

📦 安装方法：

1. 将 EchoDraft.app 拖到你的"应用程序"文件夹
2. 首次打开时，右键点击应用，选择"打开"
   （或在终端运行：xattr -cr /Applications/EchoDraft.app）
3. 开始使用！

✨ 功能特点：

- 🎙️ 本地语音转写（支持多种音频格式）
- 🌍 自动识别多种语言（中英西法德日韩俄等）
- 🔒 完全离线运行，保护隐私
- 📊 实时进度显示
- 🎨 macOS 原生风格界面

🎯 支持的音频格式：

- .m4a
- .mp3
- .wav

📖 详细文档：

https://github.com/enhen3/EchoDraft

⚠️  系统要求：

- macOS 10.15 或更高版本
- Apple Silicon (M1/M2/M3/M4) 或 Intel 处理器
- 2GB 可用内存
- 1.5GB 可用磁盘空间

🆘 遇到问题？

访问 GitHub 仓库获取帮助：
https://github.com/enhen3/EchoDraft/issues

====================================
EOF

echo "💿 创建 DMG 镜像..."
hdiutil create -srcfolder dmg_temp -volname "${VOLUME_NAME}" -fs HFS+ \
    -fsargs "-c c=64,a=16,e=16" -format UDRW -size ${SIZE} "${TEMP_DMG}"

echo "📝 挂载 DMG 进行设置..."
DEVICE=$(hdiutil attach -readwrite -noverify -noautoopen "${TEMP_DMG}" | \
    egrep '^/dev/' | sed 1q | awk '{print $1}')

MOUNT_POINT="/Volumes/${VOLUME_NAME}"

echo "⏳ 等待挂载完成..."
sleep 2

echo "🎨 设置 DMG 外观..."
# 设置图标大小和排列
echo '
   tell application "Finder"
     tell disk "'${VOLUME_NAME}'"
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
' | osascript || true

echo "💾 同步并卸载..."
sync
hdiutil detach "${DEVICE}"

echo "🗜️  压缩 DMG..."
hdiutil convert "${TEMP_DMG}" -format UDZO -imagekey zlib-level=9 -o "${FINAL_DMG}"

echo "🧹 清理临时文件..."
rm -f "${TEMP_DMG}"
rm -rf dmg_temp
rm -f "${TEMP_DMG}.sha256"

echo "✅ 计算校验和..."
shasum -a 256 "${FINAL_DMG}" | tee "${FINAL_DMG}.sha256"

echo ""
echo "======================================"
echo "✅ DMG 创建成功！"
echo "======================================"
echo ""
echo "📦 文件: ${FINAL_DMG}"
ls -lh "${FINAL_DMG}"
echo ""
echo "🔐 SHA256 校验和:"
cat "${FINAL_DMG}.sha256"
echo ""
echo "🎉 完成！现在可以将这个 DMG 文件分享给其他人了。"
echo ""
