#!/usr/bin/env bash

set -euo pipefail

echo "======================================"
echo "EchoDraft - 上传到 GitHub"
echo "======================================"
echo ""

# 进入项目目录
cd "$(dirname "$0")"

echo "📁 当前目录: $(pwd)"
echo ""

# 第一步：清理不必要的文件
echo "🧹 步骤 1/5: 清理不必要的文件..."
rm -rf build dist test_unzip 2>/dev/null || true
rm -f *.zip test_silence.wav 2>/dev/null || true
rm -f output/*.md 2>/dev/null || true
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
rm -rf models/whisper/small-int8/.cache 2>/dev/null || true
echo "✅ 清理完成"
echo ""

# 第二步：初始化 Git（如果还没有初始化）
echo "📦 步骤 2/5: 初始化 Git 仓库..."
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git 仓库已初始化"
else
    echo "✅ Git 仓库已存在"
fi
echo ""

# 第三步：添加远程仓库
echo "🔗 步骤 3/5: 配置远程仓库..."
if git remote | grep -q "origin"; then
    echo "远程仓库已存在，更新 URL..."
    git remote set-url origin https://github.com/enhen3/EchoDraft.git
else
    git remote add origin https://github.com/enhen3/EchoDraft.git
fi
echo "✅ 远程仓库: https://github.com/enhen3/EchoDraft.git"
echo ""

# 第四步：添加文件并提交
echo "📝 步骤 4/5: 添加文件并提交..."
git add .
echo ""
echo "将要提交的文件:"
git status --short
echo ""

git commit -m "Initial commit: EchoDraft - 本地语音转写工具

- 支持 Whisper small 模型本地转写
- PyQt6 现代化图形界面
- 支持 CLI 和 GUI 两种模式
- 完全本地处理，保护隐私
- 支持多语言自动识别（中英西法德日韩俄等）
- macOS 原生风格界面设计

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
" || echo "⚠️  没有新的更改需要提交（或已经提交过了）"

echo "✅ 提交完成"
echo ""

# 第五步：推送到 GitHub
echo "🚀 步骤 5/5: 推送到 GitHub..."
git branch -M main
echo "正在推送到 GitHub..."
git push -u origin main

echo ""
echo "======================================"
echo "✅ 成功上传到 GitHub!"
echo "======================================"
echo ""
echo "📍 仓库地址: https://github.com/enhen3/EchoDraft"
echo ""
echo "🎉 完成！你可以访问上面的地址查看你的项目。"
echo ""
