#!/usr/bin/env python3
"""Create an independent knowledge website without overwriting user files."""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlsplit

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
PROFILES = {
    'java': ('Java 工程笔记', '从语言基础到服务端工程，把 Java 知识连接成实践能力。', ['java']),
    'frontend': ('前端工程笔记', '从浏览器到组件与工程，把前端知识连接成实践能力。', ['frontend']),
    'mixed': ('开发者知识图谱', '连接 Java 与前端，让知识跨越技术栈。', ['java', 'frontend']),
}
TOPICS = {
    'java': {'id': 'java', 'label': 'Java 工程', 'description': '语言基础、JVM 与并发、Spring 工程，从原理走向实践。', 'href': '/java/', 'nodes': ['Java', 'JVM', 'Spring']},
    'frontend': {'id': 'frontend', 'label': '前端工程', 'description': '浏览器、TypeScript 与组件设计，把体验做成可靠的工程。', 'href': '/frontend/', 'nodes': ['Web', 'TypeScript', 'UI']},
}


def origin(value):
    parsed = urlsplit(value)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password
            or parsed.query or parsed.fragment or parsed.path not in ('', '/')
            or any(char.isspace() for char in value)):
        raise argparse.ArgumentTypeError('--site 必须是独立 HTTPS origin，例如 https://java.example.com')
    try:
        parsed.port
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    return value.rstrip('/')


def create(args):
    raw_target = Path(args.target).expanduser().absolute()
    # Do not initialize a symlinked destination by accident.
    if raw_target.is_symlink():
        raise ValueError('目标目录不能是符号链接')
    target = raw_target.resolve()
    if target.exists() and not target.is_dir():
        raise ValueError('目标路径不是目录')
    allowed = {'.git', '.DS_Store'}
    blockers = sorted(p.name for p in target.iterdir() if p.name not in allowed) if target.exists() else []
    if blockers:
        raise ValueError('目标目录非空，未写入任何文件：' + ', '.join(blockers[:12]))
    title, description, tracks = PROFILES[args.profile]
    title = args.title or title
    description = args.description or description
    if not title.strip() or not description.strip():
        raise ValueError('名称与简介不能为空')
    name = args.name or f'knowledge-{args.profile}'
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,99}', name):
        raise ValueError('--name 仅接受小写字母、数字和连字符，长度不超过 100')
    templates = ASSETS / 'template'
    if not templates.is_dir() or any(not (ASSETS / 'content' / track).is_dir() for track in tracks):
        raise ValueError('技能模板缺失，请修复技能安装')
    config = {'title': title, 'description': description, 'site': args.site,
              'profile': args.profile, 'topics': [TOPICS[t] for t in tracks]}
    plan = {'target': str(target), 'profile': args.profile, 'site': args.site,
            'title': title, 'topics': tracks, 'dryRun': args.dry_run}
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return target
    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(templates, target, dirs_exist_ok=True)
    (target / 'site.config.json').write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    package = json.loads((target / 'package.json').read_text())
    package['name'] = name
    (target / 'package.json').write_text(json.dumps(package, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    docs = target / 'src/content/docs'
    docs.mkdir(parents=True, exist_ok=True)
    for track in tracks:
        shutil.copytree(ASSETS / 'content' / track, docs / track)
    links = '\n'.join(f"- [{TOPICS[t]['label']}]({TOPICS[t]['href']})：{TOPICS[t]['description']}" for t in tracks)
    (docs / 'start.md').write_text('---\ntitle: 知识目录\ndescription: 按专题和学习路径浏览知识库。\n---\n\n## 选择一条学习路线\n\n' + links + '\n\n先阅读专题概览，再选择一个问题动手实践。示例文章只是起点，可以持续补充工程经验。\n', encoding='utf-8')
    (target / 'CLAUDE.md').symlink_to('AGENTS.md')
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    print('已生成源码；尚未安装依赖或构建。下一步在目标目录执行 npm install。')
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True, help='空目录，或尚不存在的目录')
    parser.add_argument('--profile', choices=PROFILES, default='java')
    parser.add_argument('--title')
    parser.add_argument('--description')
    parser.add_argument('--name', help='npm package name')
    parser.add_argument('--site', type=origin, default='https://kb.example')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        create(args)
    except (ValueError, OSError) as error:
        print(f'初始化失败：{error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
