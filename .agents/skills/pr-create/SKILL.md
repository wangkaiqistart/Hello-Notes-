---
name: pr-create
description: 创建 GitHub Pull Request。自动完成分支创建、代码提交、推送和 PR 创建的完整流程。用法：/pr-create [PR 标题或描述]
---

# 创建 Pull Request

根据当前工作目录的变更，创建一个 GitHub Pull Request。

## 当前上下文

!`bash .Codex/skills/pr-create/scripts/context.sh`

## 执行流程

根据上方注入的上下文，按以下步骤执行：

### 1. 分析上下文

- 如果「未提交的变更」和「领先基准的提交」均为空，提示用户没有可提交的内容并终止
- 如果当前分支是 main/master，需要先创建新分支

### 2. 创建分支（仅当前在 main/master 时）

- 根据变更内容创建语义化分支名：`类型/简短描述`
- 类型：feat / fix / docs / style / refactor / perf / test / chore
- 示例：`feat/add-login-page`、`fix/nav-link`、`docs/update-readme`

### 3. 提交变更（仅存在未提交变更时）

- 暂存相关文件（优先 `git add <具体文件>` 而非 `git add .`）
- 排除敏感文件（.env、credentials 等）
- commit message 格式：`类型: 简短描述`（中文）
- commit message 末尾添加：
  ```
  Co-Authored-By: Codex Opus 4.6 (1M context) <noreply@anthropic.com>
  ```

### 4. 推送并创建 PR

- `git push -u origin <分支名>`
- 使用 `gh pr create` 创建 PR：

```bash
gh pr create --title "简短标题" --body "$(cat <<'EOF'
## 变更概述
- 基于上方上下文中的变更文件和提交生成变更描述

## 测试计划
- [ ] 根据变更类型生成测试项

🤖 Generated with [Codex](https://Codex.ai/code)
EOF
)"
```

- PR 标题 70 字符以内，中文描述
- 如果用户提供了 `$ARGUMENTS`，将其作为 PR 标题

### 5. 输出 PR 链接

## 注意事项

- 绝不直接推送到 main/master 分支
- 如果 `gh` CLI 未安装或未认证，提示用户先运行 `gh auth login`
