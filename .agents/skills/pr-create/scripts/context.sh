#!/bin/bash
# 收集 PR 创建所需的 git 上下文信息

echo "=== 当前分支 ==="
git branch --show-current

echo ""
echo "=== 基准分支 ==="
git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}' || echo "main"

BASE=$(git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}')
BASE=${BASE:-main}

echo ""
echo "=== 领先基准的提交 ==="
git log "origin/${BASE}..HEAD" --oneline 2>/dev/null || echo "(无领先提交)"

echo ""
echo "=== 变更文件统计 ==="
git diff --stat "origin/${BASE}" 2>/dev/null || git diff --stat

echo ""
echo "=== 未提交的变更 ==="
git status --short

echo ""
echo "=== 最近提交风格 ==="
git log --oneline -5
