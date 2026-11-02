"""Redraw course diagrams as editable SVG. Run from any working directory.

Source URLs and known inconsistencies are recorded in the adjacent sources.json.
Only SVG primitives and selectable text are emitted; no raster image is embedded.
"""

from html import escape
from pathlib import Path
import json

OUT = Path(__file__).resolve().parents[1] / "public/images/ai-programming/course"
BLUE, GREEN, ORANGE, PURPLE, RED = "#4b94df", "#50b467", "#e69d4c", "#8a58ff", "#e94e50"
NAVY, INK, GRAY = "#1b3e70", "#333333", "#777777"
PALE = {BLUE: "#eaf3fc", GREEN: "#edf8ee", ORANGE: "#fff8e8", PURPLE: "#f3eeff", RED: "#fff0f0"}
STONE, TEAL, MINT = "#f1efe7", "#50cbaa", "#e0f5ef"


class SVG:
    def __init__(self, name, w, h, title, subtitle=None, plain=False):
        self.name, self.w, self.h = name, w, h
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(title)}</title>',
                      '<desc id="desc">组件关系与执行流程。文字、矩形、路径与箭头均为可编辑矢量元素；方案差异见配套正文。</desc>',
                      '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/></marker></defs>',
                      '<g font-family="Arial, PingFang SC, Microsoft YaHei, sans-serif">']
        self.rect(0, 0, w, h, "#ffffff" if plain else "#f8f9ff", "none", 0, 0)
        if not plain:
            self.text(w / 2, 60, title, 38, NAVY, "middle", True)
            if subtitle:
                self.text(w / 2, 100, subtitle, 23, "#888888", "middle")

    def rect(self, x, y, w, h, fill="white", stroke=BLUE, radius=16, sw=3, dash=False):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"' + (' stroke-dasharray="12 9"' if dash else '') + '/>')

    def text(self, x, y, value, size=22, color=INK, anchor="start", bold=False, mono=False):
        font = ' font-family="Menlo, Consolas, monospace"' if mono else ''
        self.parts.append(f'<text x="{x}" y="{y}" xml:space="preserve" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{700 if bold else 400}"{font}>{escape(str(value))}</text>')

    def lines(self, x, y, values, size=22, color=INK, anchor="start", step=None, bold=False, mono=False):
        for i, value in enumerate(values):
            self.text(x, y + i * (step or size * 1.6), value, size, color, anchor, bold, mono)

    def path(self, points, color=GRAY, width=3, arrow=True, dash=False):
        d = "M " + " L ".join(f"{x},{y}" for x, y in points)
        self.parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"' + (' marker-end="url(#arrow)"' if arrow else '') + (' stroke-dasharray="9 7"' if dash else '') + '/>')

    def circle(self, x, y, r, fill, stroke="none", sw=2):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def box(self, x, y, w, h, title, subtitle=None, fill=STONE, stroke="#cbc9bf", size=29, subsize=25, dash=False):
        self.rect(x, y, w, h, fill, stroke, 28, 2, dash)
        self.text(x + w / 2, y + h / 2 + (10 if subtitle is None else -4), title, size, INK, "middle", subtitle is not None)
        if subtitle:
            self.text(x + w / 2, y + h / 2 + 35, subtitle, subsize, "#444444", "middle")

    def panel(self, x, y, w, h, title, color=BLUE, size=24, strip=True):
        self.rect(x, y, w, h, PALE.get(color, "white"), color, 16, 3)
        if strip:
            self.rect(x + 1, y + 1, w - 2, 16, color, "none", 12, 0)
            self.rect(x + 1, y + 10, w - 2, 7, color, "none", 0, 0)
        self.text(x + w / 2, y + 48, title, size, color, "middle", True)

    def save(self, directory=None):
        self.parts.extend(["</g>", "</svg>"])
        (directory or OUT).mkdir(parents=True, exist_ok=True)
        ((directory or OUT) / f"{self.name}.svg").write_text("\n".join(self.parts) + "\n")


def cognition():
    s = SVG("cognition-seven-layers", 1860, 1116, "AI 编程工具七层架构", "从模型原料到方法论，每一层有独立职责，层间协作构成完整工程体系")
    rows = [
        (RED, "#ffe2e2", "方法论层", "用工具的思想", ["SDD", "Harness Engineering", "Vibe Coding"]),
        (ORANGE, "#ffe9d8", "工作流层", "AI 自动化运行", ["Headless Mode", "GitHub Actions", "CI/CD 触发", "事件触发"]),
        ("#e66e70", "#fff0f0", "协议生态层", "连接外部世界", ["MCP", "gh CLI", "REST API", "内部系统"]),
        (PURPLE, "#f3eeff", "协作机制层", "AI 团队协作", ["Subagents", "Worktrees", "Plan Mode"]),
        ("#d4a73b", "#fff8df", "配置约束层", "让 AI 遵守规则", ["CLAUDE.md", "AGENTS.md", "Skills", "Hooks", "Permissions"]),
        (GREEN, "#e0f2e9", "工具层", "每天直接打交道", ["Cursor", "Claude Code", "Copilot", "Windsurf", "Aider"]),
        (BLUE, "#def0fc", "模型层", "AI 的原料", ["Claude", "GPT-4o", "Gemini", "DeepSeek", "Qwen"]),
    ]
    for i, (c, bg, title, sub, pills) in enumerate(rows):
        y = 127 + i * 136
        s.rect(35, y, 1748, 128, bg, c, 17)
        s.circle(87, y + 64, 36, c)
        s.text(87, y + 75, 7 - i, 30, "white", "middle", True)
        s.text(167, y + 47, title, 27, "#222222", bold=True)
        s.text(167, y + 89, sub, 22, "#666666")
        n = len(pills)
        xs = {3: [513, 961, 1409], 4: [457, 793, 1129, 1465], 5: [429, 697, 965, 1233, 1501]}[n]
        pw = 260 if n < 5 else 248
        for x, text in zip(xs, pills):
            s.rect(x, y + 40, pw, 48, c, "none", 24, 0)
            s.text(x + pw / 2, y + 72, text, 21, "white", "middle", True)
    for y1, y2, c, label in [(135, 383, RED, "杠杆价值"), (407, 791, PURPLE, "工程能力"), (815, 1063, BLUE, "工具基础")]:
        s.path([(1799, y1), (1811, y1), (1811, y2), (1799, y2)], c, 4, False)
        cy = (y1 + y2) / 2
        s.parts.append(f'<text transform="translate(1838 {cy}) rotate(-90)" text-anchor="middle" font-size="22" font-weight="700" fill="{c}">{label}</text>')
    s.save()


def agentos():
    s = SVG("agentos-overview", 1472, 1040, "AgentOS 单体应用架构", plain=True)
    s.rect(56, 40, 1360, 956, "none", "#bcbcaf", 44, 2, True)
    s.text(112, 89, "AgentOS 单体应用（Spring Boot，单二进制）", 26, bold=True)
    s.text(736, 138, "入口层", 26, anchor="middle", bold=True)
    s.box(396, 156, 300, 88, "CLI Channel")
    s.box(776, 156, 300, 88, "Web Service")
    s.path([(546, 244), (656, 312)])
    s.path([(926, 244), (816, 312)])
    s.box(496, 316, 480, 116, "ReAct 循环（引擎）", "PromptBuilder   ToolExecutor", MINT, TEAL)
    for x, title, sub in [(96, "Provider", "LLM 调用抽象"), (556, "Memory", "会话加长期记忆"), (1016, "Tool", "内置加 MCP Client")]:
        start = 616 if x == 96 else 856 if x == 1016 else 736
        s.path([(start, 432), (x + 180, 538)], "#99998c", 2)
        s.box(x, 540, 360, 116, title, sub)
    s.path([(736, 656), (736, 732)], "#99998c", 2)
    s.box(496, 736, 480, 100, "存储层", "SQLite（Session、审计） 文件系统")
    for x, label in [(96, "LLM 厂商 API"), (1016, "外部 MCP server")]:
        s.path([(x + 180, 656), (x + 180, 900)], "#99998c", 2)
        s.text(x + 180, 701, "外接", 24, anchor="middle", bold=True)
        s.box(x, 904, 360, 80, label, fill="none", dash=True, size=26)
    s.save()
    s = SVG("agentos-layers", 1472, 720, "AgentOS 四层结构", plain=True)
    rows = [
        ("接入层", "CLI Channel   Web Service（REST API）", "消息进出的两个入口"),
        ("引擎层", "ReActLoop   PromptBuilder   ToolExecutor", "Agent 的大脑"),
        ("能力层", "Provider   Memory   Tool", "给引擎提供 LLM、上下文、执行能力"),
        ("基础层", "Profile/Bootstrap/Skill 加载  Session  SQLite  配置密钥", "工程地基"),
    ]
    for i, (title, line, sub) in enumerate(rows):
        y = 72 + 160 * i
        s.rect(136, y, 1200, 128, MINT if i == 1 else STONE, TEAL if i == 1 else "#cbc9bf", 28, 2)
        s.text(246, y + 76, title, 32, anchor="middle", bold=True)
        s.text(822, y + 53, line, 27, anchor="middle", bold=True)
        s.text(822, y + 98, sub, 25, anchor="middle")
    s.save()
    s = SVG("agentos-boundary", 1274, 524, "Spring AI 使用边界", plain=True)
    for x, title in [(75, "只用这部分"), (674, "禁用这部分")]:
        s.text(x + 262.5, 75, title, 29, anchor="middle", bold=True)
    s.box(75, 112, 525, 106, "Provider 抽象与协议转换", "向各家 LLM 适配", MINT, TEAL)
    s.box(75, 240, 525, 106, "@Tool 的 Schema 生成", "扫描方法生成 JSON Schema", MINT, TEAL)
    s.box(674, 112, 525, 106, "自动 tool 执行", "否则 tool 会被调两次", dash=True)
    s.box(674, 240, 525, 106, "tool 调度由 AgentOS 控制", "ReActLoop 加 ToolExecutor", dash=True)
    s.text(637, 437, "Spring AI 只做协议适配器和 schema 生成器，不做循环引擎", 27, anchor="middle", bold=True)
    s.save()
    s = SVG("agentos-react", 1472, 840, "AgentOS ReAct 循环", plain=True)
    for y, title, sub, fill in [(60, "接收用户消息", None, STONE), (216, "组装 Prompt", "注入 Bootstrap、Memory、历史", MINT), (372, "调用 LLM Provider", None, MINT)]:
        s.box(556, y, 360, 100, title, sub, fill, TEAL if fill == MINT else "#cbc9bf", subsize=22)
        s.path([(736, y + 100), (736, y + 152 if y < 372 else 524)], "#99998c", 2)
    s.parts.append(f'<path d="M736 528 L920 588 L736 648 L552 588 Z" fill="{STONE}" stroke="#cbc9bf" stroke-width="2"/>')
    s.text(736, 598, "有 Tool 调用？", 28, anchor="middle", bold=True)
    s.path([(736, 648), (736, 708)], "#99998c", 2)
    s.text(756, 689, "无", 24)
    s.box(556, 712, 360, 92, "返回最终响应", fill=MINT, stroke=TEAL)
    s.path([(920, 588), (1032, 588)], "#99998c", 2)
    s.text(968, 568, "有", 24)
    s.box(1036, 538, 320, 100, "执行 Tool", "结果回填对话历史", size=28, subsize=24)
    s.path([(1196, 538), (1196, 266), (920, 266)], "#99998c", 2)
    s.text(1216, 404, "回填后继续循环", 23)
    s.save()
    s = SVG("agentos-memory", 1274, 600, "AgentOS 记忆层统一门面", plain=True)
    s.box(468, 68, 338, 94, "ReAct 循环")
    s.path([(637, 162), (637, 240)], "#99998c", 2)
    s.text(660, 213, "只调一个接口", 24)
    s.box(430, 244, 414, 108, "MemoryService", "三层统一门面，对外只暴露一个接口", MINT, TEAL, subsize=21)
    for x, title, sub in [(150, "SessionManager", "会话记忆（SQLite）"), (712, "LongTermMemory", "长期记忆（MEMORY.md）")]:
        s.path([(537 if x == 150 else 737, 352), (x + 206, 446)], "#99998c", 2)
        s.text(x + 206, 410, "委托", 24, anchor="middle")
        s.box(x, 450, 412, 110, title, sub)
    s.save()


def when_overview():
    s = SVG("when-overview", 1932, 1040, "When 整体架构", "业务方 → When集群（无差别多节点）→ 外部依赖 → 下游Sink")
    s.panel(28, 133, 240, 280, "调用方", PURPLE, strip=False)
    for i, label in enumerate(["订单服务", "推送服务", "任务系统", "任意业务"]):
        s.rect(48, 193 + i * 52, 200, 40, "white", "#b593ff", 8, 1.5)
        s.text(148, 221 + i * 52, label, 21, "#6330db", "middle")
    s.path([(268, 273), (304, 273)], PURPLE)
    s.text(288, 252, "HTTP", 17, PURPLE, "middle")
    s.panel(28, 453, 240, 320, "设计原则", ORANGE, size=22, strip=False)
    s.lines(148, 526, ["无差别节点", "HTTP外 gRPC内", "Redis=真理源", "ETCD不造轮", "Sink可插拔", "90%AI完成"], 18, "#555555", "middle", 40)
    s.panel(308, 133, 1160, 760, "When 集群（无差别多节点架构）", BLUE, strip=False)
    modules = ["接入层 HTTP API", "路由层（一致性Hash）", "时间轮调度引擎", "副本同步器", "Sink 投递器", "ETCD 客户端", "Redis 客户端", "可观测模块"]
    for i, (x, c, dark) in enumerate([(328, BLUE, "#2c5180"), (688, GREEN, "#1c5e1e"), (1048, ORANGE, "#8d5000")]):
        s.rect(x, 188, 348, 602, PALE[c], c, 17)
        s.rect(x + 1, 189, 346, 60, dark, "none", 15, 0)
        s.rect(x + 1, 218, 346, 31, dark, "none", 0, 0)
        s.text(x + 174, 218, f"节点 {i + 1}", 21, "white", "middle", True)
        if i == 0:
            s.text(x + 174, 243, "(Controller★)", 18, "white", "middle")
        for j, label in enumerate(modules):
            s.rect(x + 12, 261 + j * 64, 324, 52, "white", c, 8, 1.5)
            s.text(x + 174, 294 + j * 64, label, 18, dark, "middle")
    s.text(888, 866, "节点间通过 gRPC 互相路由（消息转发 + 副本同步）", 22, BLUE, "middle")
    for y, h, label, c, lines in [(133, 200, "ETCD 集群", BLUE, ["· 节点注册 + 心跳 Lease", "· Controller 选举", "· Watch 事件驱动", "· 配置动态下发"]), (365, 200, "Redis", RED, ["· 消息体持久化", "· 时间索引存储", "· key按消息ID拆分", "· TTL自动清理"])]:
        s.panel(1508, y, 400, h, label, c, strip=False)
        s.lines(1530, y + 73, lines, 19, step=29)
        s.path([(1468, y + 100), (1503, y + 100)], c)
    s.panel(1508, 593, 400, 300, "下游 Sink", GREEN, strip=False)
    for i, (c, label, sub) in enumerate([(BLUE, "HTTP", "业务回调接口"), (ORANGE, "Kafka", "消息总线Topic"), (PURPLE, "gRPC★", "内部RPC服务"), ("#888888", "更多...", "SPI扩展接入")]):
        y = 657 + i * 56
        s.rect(1520, y, 376, 44, "white", c, 8, 1.5)
        s.text(1544, y + 29, label, 21, c, bold=True)
        s.text(1628, y + 29, sub, 19, "#666666")
    s.path([(1468, 743), (1503, 743)], GREEN)
    s.rect(28, 917, 1880, 88, "#f4f4f4", "#cccccc", 16, 2)
    s.text(968, 950, 'Controller 是“角色”不是“专用节点”——集群中一台普通节点同时承担 Controller 职责，节点同构，运维简单', 22, anchor="middle", bold=True)
    s.text(968, 983, "★ gRPC Sink 在3周MVP之后实现；When内部节点间通信已使用gRPC", 21, "#888888", "middle")
    s.save()


def when_cluster():
    s = SVG("when-cluster", 1936, 1198, "When 集群协调机制", "全部基于 ETCD · 事件驱动而非主动探测 · 声明式集群状态管理")
    s.rect(32, 131, 520, 660, "#1e1e30", BLUE)
    s.text(52, 168, "ETCD key 空间", 23, BLUE, bold=True)
    tree = [("/when/", "#dddfff"), ("  nodes/", "#b4efa2"), ("    node-1 {ip,port} ←Lease", "#90e5f8"), ("    node-2 {ip,port} ←Lease", "#90e5f8"), ("    node-3 {ip,port} ←Lease", "#90e5f8"), ("  controller node-1 ←Lease", "#ffc17a"), ("  timewheels/", "#b4efa2"), ("    tw-001 {master:node-1,", "#90e5f8"), ("            slave:node-2}", "#90e5f8"), ("    tw-002 {master:node-2,", "#90e5f8"), ("            slave:node-3}", "#90e5f8"), ("  config/", "#b4efa2"), ("    cluster_size 3", "#ffdfa0"), ("    timewheel_count 12", "#ffdfa0")]
    for i, (line, color) in enumerate(tree):
        s.text(52, 199 + i * 38, line, 18, color, mono=True)
    sections = [
        (BLUE, "① 节点注册与保活", ["启动 → PUT /when/nodes/node-N + Lease(TTL=10s)", "后台线程每3s续约 KeepAlive（独立线程）", "续约停止 → ETCD自动删key → 其他节点感知"]),
        (PURPLE, "② Controller 选举", ["所有节点同时尝试 Txn: IF NOT EXISTS PUT /when/controller", "首个成功的节点成为 Controller（原子保证）", "Controller故障 → Lease过期 → Watch触发 → 重新选举"]),
        (RED, "③ 节点故障检测与切换", ["Controller Watch /when/nodes/ 前缀", "DELETE事件 → 检查故障节点的Master时间轮", "更新 ETCD tw-N: Slave→Master → 新Master感知并接管"]),
        (GREEN, "④ 节点加入与Rebalance", ["新节点 PUT /when/nodes/node-new", "Controller感知 → 计算负载均衡 → 迁移Slave副本到新节点", "优先迁Slave（不影响写入路径）→ 同步完成后正式承担Slave"]),
    ]
    for i, (c, title, lines) in enumerate(sections):
        y = 131 + 224 * i
        s.rect(592, y, 760, 200, "#fafaff", c)
        s.rect(593, y + 1, 758, 51, c, "none", 14, 0)
        s.rect(593, y + 30, 758, 22, c, "none", 0, 0)
        s.text(972, y + 35, title, 23, "white", "middle", True)
        for j, line in enumerate(lines):
            s.circle(620, y + 69 + j * 44, 8, c)
            s.text(640, y + 76 + j * 44, line, 18)
    s.panel(1392, 131, 520, 930, "故障切换时间线", RED, strip=False)
    s.path([(1436, 203), (1436, 935)], "#dddddd", 2, False)
    timeline = [("T+0s", "Master节点故障（进程崩溃/网络断）", RED), ("T+3s", "ETCD Lease续约停止", ORANGE), ("T+10s", "Lease TTL到期 → key自动删除", ORANGE), ("T+10s", "Controller Watch触发DELETE事件", BLUE), ("T+11s", "Controller更新ETCD: Slave→Master", BLUE), ("T+11s", "新Master Watch到tw-N变化", GREEN), ("T+12s", "新Master从Redis加载未投递消息", GREEN), ("T+15s", "Controller为tw-N分配新Slave", "#888888")]
    for i, (time, line, c) in enumerate(timeline):
        y = 203 + i * 98
        s.circle(1436, y, 12, c)
        s.text(1456, y + 7, time, 17, c, bold=True)
        s.text(1548, y + 7, line, 17)
    s.rect(1412, 966, 480, 76, "#ffd0d0", RED, 13)
    s.text(1652, 994, "SLA: Master故障后 Slave 在10秒内接管", 21, "#c90000", "middle", True)
    s.text(1652, 1025, "已写入Redis的消息:绝对不丢 · 正在投递的消息:至少一次", 15, "#666666", "middle")
    s.rect(32, 1091, 1880, 88, PALE[BLUE], BLUE)
    s.text(972, 1124, "核心设计：Controller 不主动 ping 节点，而是被动响应 ETCD Watch 事件流——「主动探测」变「事件驱动」", 22, "#2c5180", "middle", True)
    s.text(972, 1157, "Lease由独立线程续约，GC停顿和业务线程繁忙不影响心跳——只有真正“节点失能”才触发切换", 20, "#555555", "middle")
    s.save()


def when_timewheel():
    s = SVG("when-timewheel", 2102, 1236, "多层时间轮设计", "4层嵌套覆盖1秒~30天 · O(1)插入触发 · 到期降级 · 调度循环不做重IO")
    for x, y, w, h, c, title in [(32, 124, 860, 860, "#b67816", "第四层 · 30天"), (92, 184, 740, 740, RED, "第三层 · 24小时"), (152, 244, 620, 620, GREEN, "第二层 · 60分钟"), (212, 304, 500, 500, BLUE, "第一层 · 60秒")]:
        s.rect(x, y, w, h, "white", c, 14, 4)
        s.rect(x + 1, y + 1, w - 2, 16, c, "none", 10, 0)
        s.text(x + w / 2, y + 47, title, 24, c, "middle", True)
    s.lines(462, 386, ["60 槽，步长=1秒", "覆盖范围：1秒~60秒"], 18, GRAY, "middle", 28)
    s.rect(232, 454, 460, 160, "#fffbef", "#b67816", 10, 2)
    s.text(462, 491, "插入示例：delay=90分钟", 22, "#b67816", "middle", True)
    s.lines(462, 525, ["→ 第三层 slot=1（1小时后降级）", "→ 降到第二层 slot=30（30分钟）", "→ 降到第一层 tick=0 触发投递"], 18, "#666666", "middle", 28)
    for x, y, c in [(482, 650, "#b67816"), (542, 700, RED), (602, 750, GREEN)]:
        s.path([(x, 614), (x, y)], c)
        s.text(x + 9, y - 9, "到期降级", 17, c)
    s.panel(932, 124, 560, 500, "调度循环（关键路径设计）", BLUE)
    s.lines(956, 205, ["while running:", "  msgs = wheel[pointer]", "  // O(1) 取槽", "  for msg in msgs:", "    if layer==0:", "      sink_pool.submit(", "        deliver, msg) // 异步", "    else:", "      lower_wheel.add(msg)", "      // 降级", "  pointer = (pointer+1) % size", "  sleep_until_next_slot()", "  // 补偿耗时，防漂移"], 18, step=24, mono=True)
    s.panel(932, 644, 560, 180, "性能指标", GREEN, strip=False)
    for i, (label, value) in enumerate([("插入复杂度:", "O(1)"), ("触发复杂度:", "O(1)"), ("内存占用:", "O(slots × layers)"), ("精度误差:", "< 1秒（slot步长）")]):
        s.text(956, 711 + i * 31, label, 18, bold=True)
        s.text(1472, 711 + i * 31, value, 18, "#338b3a", "end")
    s.panel(1532, 124, 540, 700, "集群分布策略", PURPLE)
    s.rect(1552, 194, 500, 200, "white", "#b68cff", 10, 1.5)
    s.text(1802, 231, "消息分片规则", 23, "#6f36d9", "middle", True)
    s.lines(1562, 263, ["shard = msgId % nodeCount", "· 同一消息始终在同一节点", "· Master 节点负责本 shard 调度", "· Slave 跟随复制，不独立触发", "· rebalance 时重新分配 shard"], 18, step=30)
    for i, c in enumerate([BLUE, GREEN, ORANGE]):
        y = 418 + i * 124
        s.rect(1552, y, 500, 104, "white", c, 10)
        s.rect(1553, y + 1, 498, 16, c, "none", 10, 0)
        s.text(1802, y + 44, f"节点{i}", 23, c, "middle", True)
        s.text(1802, y + 73, "(Master)" if i == 0 else "(Slave)", 18, GRAY, "middle")
        s.text(2036, y + 73, f"shard {i},{i+3},{i+6}…", 16, GRAY, "end")
    s.panel(1552, 838, 500, 110, "Rebalance 触发条件", ORANGE, size=20, strip=False)
    s.lines(1802, 912, ["节点加入 / 离开 / 故障转移", "→ ETCD Watch 事件驱动重分片"], 18, GRAY, "middle", 27)
    s.rect(32, 994, 2040, 220, "#fafafa", "#cccccc", 16, 2)
    s.text(1052, 1030, "4层时间轮参数汇总", 23, anchor="middle", bold=True)
    xs = [122, 312, 532, 822, 1212]
    for x, label in zip(xs, ["层", "槽数", "步长", "覆盖范围", "溢出处理"]):
        s.text(x, 1064, label, 20, "#555555", "middle", True)
    s.path([(42, 1074), (2062, 1074)], "#dddddd", 2, False)
    for i, row in enumerate([("L1", "60", "1秒", "1s ~ 60s", "无（最小粒度）"), ("L2", "60", "1分钟", "1m ~ 60m", "降级到 L1"), ("L3", "24", "1小时", "1h ~ 24h", "降级到 L2"), ("L4", "30", "1天", "1d ~ 30d", "降级到 L3")]):
        for x, label in zip(xs, row):
            s.text(x, 1101 + i * 29, label, 18, anchor="middle")
    s.save()


def when_ha():
    s = SVG("when-ha", 1930, 1346, "主从复制与故障转移机制", "消息写入主节点 → 同步从节点 → ETCD 监听心跳 → 10s 内完成选主")
    s.panel(24, 120, 860, 800, "正常运行：写入与复制", BLUE, size=28)
    s.text(244, 222, "① 客户端写入", 21, BLUE, "middle")
    for x, y, title, c, sub in [(84, 230, "Master 节点", BLUE, "接受写入请求 / 广播复制"), (84, 450, "Slave 节点 A", GREEN, "接受复制 / 只读查询"), (504, 450, "Slave 节点 B", GREEN, "接受复制 / 只读查询")]:
        s.rect(x, y, 320, 120, "white", c, 12)
        s.rect(x + 1, y + 1, 318, 16, c, "none", 10, 0)
        s.text(x + 160, y + 50, title, 26, c, "middle", True)
        s.text(x + 160, y + 88, sub, 18, "#555555", "middle")
    s.path([(244, 350), (244, 446)], "#999999")
    s.path([(404, 330), (664, 446)], "#999999")
    s.text(192, 406, "② 复制", 21)
    s.text(572, 406, "② 复制", 21)
    for x, y in [(244, 350), (244, 570), (664, 570)]:
        s.path([(x, y), (444, 650)], PURPLE, dash=True, arrow=False)
    s.rect(264, 650, 360, 80, PALE[PURPLE], PURPLE, 12)
    s.text(444, 681, "ETCD 心跳监控", 23, PURPLE, "middle", True)
    s.text(444, 713, "TTL=5s，逾期标记宕机", 18, "#555555", "middle")
    s.rect(64, 790, 780, 100, "#e9f8ff", BLUE, 12)
    s.text(454, 825, "复制延迟保证", 23, BLUE, "middle", True)
    s.text(454, 863, "同步复制 < 50ms | 磁盘持久化后 ACK | Slave 积压监控", 18, "#555555", "middle")
    s.panel(924, 120, 980, 1100, "故障转移时序（目标 < 10s）", RED, size=28)
    s.path([(1024, 258), (1024, 1060)], "#cccccc", 2, False)
    events = [("T=0s", "Master 宕机", "ETCD TTL 租约到期，心跳停止", RED), ("T=5s", "ETCD 感知", "TTL 超时，/nodes/master 键消失", ORANGE), ("T=5.5s", "Slave 感知", "Watch 事件触发，候选人竞争选主", PURPLE), ("T=6s", "Slave A 当选", "抢占 /election/master，成为新 Controller", PURPLE), ("T=6.5s", "角色切换", "新 Master 开始接受写入，Slave B 重建复制链", GREEN), ("T=8s", "服务恢复", "对外服务正常，完成故障转移", GREEN)]
    for i, (time, title, sub, c) in enumerate(events):
        y = 226 + i * 150
        s.circle(1024, y + 32, 21, c, "white", 3)
        s.text(1024, y + 38, time, 12, "white", "middle", True)
        s.rect(1064, y, 800, 120, "white", c, 12)
        s.rect(1065, y + 1, 798, 16, c, "none", 10, 0)
        s.text(1104, y + 46, title, 24, c, bold=True)
        s.text(1104, y + 84, sub, 20, "#555555")
    s.rect(944, 1130, 940, 72, "#ffe7e7", RED, 12)
    s.text(1414, 1160, "故障转移 SLA", 22, "#c90000", "middle", True)
    s.text(1414, 1189, "TTL(5s) + Watch延迟(0.5s) + 选主(0.5s) + 切换(1s) = 约7s < 10s目标", 18, "#666666", "middle")
    s.rect(24, 1240, 1880, 88, PALE[PURPLE], PURPLE)
    s.text(964, 1275, "数据一致性保证：写入 Master 后同步复制，ACK 前不响应客户端 → 零丢失保证", 23, "#6f36d9", "middle", True)
    s.text(964, 1308, "脑裂防护：ETCD 强一致选主，同一时刻只有一个节点持有 /election/master 锁", 20, GRAY, "middle")
    s.save()


def when_lifecycle():
    s = SVG("when-lifecycle", 1928, 1228, "延时消息写入与投递流程", "写入：Redis先于返回业务方 · 投递：调度循环只触发，Sink异步执行")
    left = [
        ("业务方 POST /api/v1/messages", "携带延时时长、Sink配置、消息内容"),
        ("参数校验", "延时范围/Sink类型/消息体大小 ≤64KB"),
        ("生成 message_id", "Snowflake算法，全局唯一，含节点ID"),
        ("路由决策", "一致性Hash(message_id) → 选定 tw-N"),
        ("gRPC转发（如需）", "如果tw-N的Master不在本节点，转发过去"),
        ("Redis持久化", "Pipeline: SET消息体 + SET时间索引（必须先于返回）"),
        ("写入内存时间轮", "插入到对应层和槽位，O(1)复杂度"),
        ("异步同步Slave", "gRPC发给Slave，不阻塞业务方返回"),
        ("返回 message_id", "status=pending，此时消息已安全落盘"),
    ]
    right = [
        ("时间轮tick推进", "每秒推进一槽，取出槽内全部消息"),
        ("消息降级判断", "若在上层时间轮 → 插入下一层重新等待"),
        ("到达第一层", "进入投递流程，提交到Sink投递器线程池"),
        ("异步执行Sink", "HTTP POST / Kafka Send，不阻塞调度循环"),
        ("投递成功", "异步删除Redis消息体和索引，同步Slave删除"),
        ("投递失败·可重试", "指数退避(30s→1m→2m→4m→8m)，重入时间轮"),
        ("投递失败·不可重试", "HTTP 4xx等，直接标记 failed，保留Redis备查"),
        ("超过5次重试", "状态→failed，消息留Redis供运维排查"),
        ("取消流程", "DELETE API → 定位Master → 内存+Redis删除，O(1)"),
    ]
    for x, c, title, rows in [(24, BLUE, "写入流程", left), (944, GREEN, "投递与重试流程", right)]:
        s.rect(x, 128, 880, 896, PALE[c], c)
        s.rect(x + 1, 129, 878, 71, c, "none", 14, 0)
        s.rect(x + 1, 160, 878, 40, c, "none", 0, 0)
        s.text(x + 440, 174, title, 27, "white", "middle", True)
        for i, (head, detail) in enumerate(rows):
            y = 217 + i * 88
            s.rect(x + 16, y, 848, 80, "white", c, 10, 1.5)
            s.circle(x + 44, y + 40, 20, c)
            s.text(x + 44, y + 47, i + 1, 19, "white", "middle", True)
            s.text(x + 76, y + 29, head, 21, c, bold=True)
            s.text(x + 76, y + 57, detail, 18)
            if i < 8:
                s.path([(x + 44, y + 80), (x + 44, y + 87)], c, 2)
    s.rect(24, 1052, 1880, 136, PALE[ORANGE], ORANGE)
    s.text(964, 1090, "两个关键顺序约束（违反则丢消息或重复投递）", 24, "#8d5000", "middle", True)
    for x, c, label, detail in [(44, BLUE, "写入约束", "Redis持久化 → 写内存时间轮 → 返回业务方（顺序不可颠倒）"), (984, GREEN, "投递约束", "Sink投递成功 → 删Redis → 认为完成（中间故障 = 至少一次语义）")]:
        s.rect(x, 1109, 120, 36, c, "none", 5, 0)
        s.text(x + 60, 1134, label, 18, "white", "middle", True)
        s.text(x + 170, 1134, detail, 19)
    s.save()


def when_sink():
    s = SVG("when-sink", 1938, 1392, "Sink 插件架构：SPI 扩展机制", "一个 SPI 接口 → N 种投递实现 → 用户零成本扩展")
    s.panel(488, 124, 960, 200, "Sink 接口（SPI 契约）", PURPLE, size=27)
    s.lines(968, 211, ["public interface Sink {", "  String type(); // 唯一标识符", "  void deliver(Message m) throws Exception; // 投递", "}"], 19, anchor="middle", step=28, mono=True)
    s.rect(488, 338, 960, 56, "#efffef", GREEN, 10, 2)
    s.text(968, 374, "META-INF/services/com.when.sink.Sink → ServiceLoader 自动发现", 21, "#338b3a", "middle")
    columns = [
        (28, BLUE, "HTTP Sink（内置）", [("trigger_type:", "http"), ("endpoint_url:", "https://your-api.com/callback"), ("method:", "POST / GET"), ("headers:", "Content-Type / Auth"), ("retry:", "最多 3 次，指数退避")], ["① 到期 → 取出消息配置", "② 构造 HTTP 请求体", "③ 发起调用，等待 200", "④ 非 200 → 放回重试队列"]),
        (678, RED, "Kafka Sink（内置）", [("trigger_type:", "kafka"), ("bootstrap:", "broker1:9092,broker2"), ("topic:", "delay-callback"), ("key:", "消息 ID（幂等去重）"), ("acks:", "acks=all 保证写入")], ["① 到期 → 取出消息", "② 序列化 payload", "③ KafkaProducer.send()", "④ 等待 RecordMetadata"]),
        (1328, GREEN, "自定义 Sink（扩展）", [("trigger_type:", "my-mq"), ("step1:", "implement Sink interface"), ("step2:", "register in META-INF/services"), ("step3:", "jar 放入 plugins/ 目录"), ("step4:", "重启服务自动加载")], ["① 实现 type() 返回唯一标识", "② 实现 deliver() 业务逻辑", "③ SPI 文件声明实现类", "④ 热插拔，无需修改核心"]),
    ]
    for x, c, title, pairs, steps in columns:
        s.path([(968, 398), (x + 290, 450)], PURPLE)
        s.rect(x, 454, 580, 120, "white", c, 14, 4)
        s.rect(x + 1, 455, 578, 16, c, "none", 12, 0)
        s.text(x + 290, 500, title, 27, c, "middle", True)
        s.text(x + 290, 540, "实现类 → ServiceLoader 注册", 18, "#666666", "middle")
        s.rect(x, 594, 580, 300, "#fafafa", "#dddddd", 12, 2)
        s.text(x + 290, 628, "配置参数", 22, anchor="middle", bold=True)
        s.path([(x + 20, 643), (x + 560, 643)], "#e7e7e7", 1.5, False)
        for i, (key, value) in enumerate(pairs):
            s.text(x + 24, 671 + i * 44, key, 17, "#555555", bold=True)
            s.text(x + 564, 671 + i * 44, value, 17, "#666666", "end")
        s.rect(x, 910, 580, 260, "#f8f7ff", "#cfcee0", 12, 2)
        s.text(x + 290, 944, "执行步骤", 22, anchor="middle", bold=True)
        s.path([(x + 20, 958), (x + 560, 958)], "#e7e7e7", 1.5, False)
        s.lines(x + 24, 986, steps, 18, "#555555", step=44)
    s.rect(28, 1234, 1880, 144, "#fffbef", "#b67816", 16)
    s.text(968, 1270, "插件目录 & 热加载", 23, "#b67816", "middle", True)
    s.text(968, 1303, "when-server/plugins/ → my-sink-1.0.jar | SPI loader 扫描 → 注入 SinkRegistry | type 唯一性校验", 21, "#555555", "middle")
    s.text(968, 1337, "内置插件打包进主 jar；第三方插件放 plugins/ 目录；重启后自动合并到 type→Sink 注册表", 19, "#888888", "middle")
    s.save()


def when_deployment():
    s = SVG("when-deployment", 2110, 1272, "部署拓扑：3节点集群", "docker-compose 本地 3 节点 · 生产最小 3 节点保证 HA")
    s.panel(30, 126, 960, 860, "docker-compose 集群（本地开发 / CI）", BLUE, 28)
    s.panel(1030, 126, 1040, 860, "K8s 生产部署（参考架构）", GREEN, 28)
    s.rect(50, 196, 920, 100, PALE[PURPLE], PURPLE, 12)
    s.text(510, 234, "ETCD 集群（3节点）", 23, PURPLE, "middle", True)
    s.text(510, 264, "etcd-0:2379 etcd-1:2379 etcd-2:2379 — Raft 共识", 18, "#666666", "middle")
    for i, (x, c, role) in enumerate([(50, BLUE, "Master（初始）"), (350, GREEN, "Slave A"), (650, ORANGE, "Slave B")]):
        s.path([(x + 146, 326), (x + 146, 300)], PURPLE, 2, dash=True)
        s.rect(x, 326, 292, 220, "white", c, 14, 4)
        s.rect(x + 1, 327, 290, 16, c, "none", 12, 0)
        s.text(x + 146, 369, f"when-node-{i}", 23, c, "middle", True)
        s.lines(x + 146, 399, [role, f"port: {8080+i} / {9090+i}", "时间轮 · 状态机", "复制 · Sink 分发", f"./data/node-{i}:/data"], 17, "#888888", "middle", 28)
        if i < 2:
            s.path([(x + 292, 436), (x + 299, 436)], "#888888", 2)
    for x, w, c, title, sub in [(50, 444, RED, "Redis（单节点 / Sentinel）", "redis:6379 RDB+AOF 持久化"), (514, 456, "#b67816", "Nginx / HAProxy", ":8080 → node-0/1/2 轮询")]:
        s.path([(510, 546), (x + w / 2, 576)], c, 2, arrow=False, dash=True)
        s.rect(x, 576, w, 90, "#fffaf0" if c != RED else "#fff5f5", c, 12)
        s.text(x + w / 2, 612, title, 21, c, "middle", True)
        s.text(x + w / 2, 643, sub, 18, "#666666", "middle")
    s.rect(50, 692, 920, 272, "#f8f8f8", "#cccccc", 12, 2)
    s.text(510, 724, "docker-compose.yml（关键片段）", 21, anchor="middle", bold=True)
    s.lines(66, 750, ["services:", "  when-node-0:", "    image: when-server:latest", "    environment:", "      - WHEN_NODE_ID=0", "      - WHEN_ETCD_ENDPOINTS=etcd-0:2379,etcd-1:2379", "      - WHEN_REDIS_HOST=redis", "    volumes: [./data/node-0:/data]", '    ports: ["8080:8080","9090:9090"]'], 15, step=24, mono=True)
    s.rect(1050, 196, 1000, 130, "#efffef", GREEN, 12)
    s.text(1550, 233, "StatefulSet: when-node（3 replicas）", 23, "#338b3a", "middle", True)
    s.lines(1550, 267, ["有序启动 · 稳定网络标识 · PVC 独立持久卷", "when-node-0/1/2.when-svc — 各节点稳定 DNS"], 18, "#777777", "middle", 30)
    configs = [(1050, 352, GREEN, "Service（ClusterIP）", "when-svc:8080", "内部服务发现"), (1560, 352, "#b67816", "Ingress / LoadBalancer", "对外 :80 / :443", "限流 · TLS 终止"), (1050, 488, ORANGE, "ConfigMap", "etcd-endpoints, node-count", "redis-host, sink-config"), (1560, 488, RED, "Secret", "redis-password / etcd-cert", "api-token")]
    for x, y, c, title, sub, extra in configs:
        s.rect(x, y, 490, 110, "white" if y == 352 else PALE.get(c, "white"), c, 10, 2)
        s.text(x + 245, y + 36, title, 21, c, "middle", True)
        s.text(x + 245, y + 69, sub, 18, "#666666", "middle")
        s.text(x + 245, y + 98, extra, 16, "#888888", "middle")
    for x, y, w, h, c, title, sub in [(1050, 624, 1000, 84, PURPLE, "PVC: each-node-pvc（ReadWriteOnce）", "Pod 重启不丢数据 · StorageClass 按需配置"), (1050, 732, 490, 84, BLUE, "External ETCD", "生产建议独立部署"), (1560, 732, 490, 84, RED, "Redis Cluster / Sentinel", "生产高可用配置")]:
        s.rect(x, y, w, h, PALE[c], c, 10)
        s.text(x + w / 2, y + 35, title, 21, c, "middle", True)
        s.text(x + w / 2, y + 64, sub, 18, "#666666", "middle")
    s.rect(30, 1012, 2040, 110, "#fafafa", "#cccccc", 16, 2)
    s.text(1050, 1047, "环境选型对比", 23, anchor="middle", bold=True)
    for x, c, title, sub in [(50, BLUE, "本地开发", "docker-compose · 1/3节点均可 · 快速验证"), (726, GREEN, "CI / 集成测试", "docker-compose 3节点 · 故障转移自动化测试"), (1402, RED, "生产", "K8s StatefulSet · 外部ETCD · Redis Sentinel")]:
        s.rect(x, 1068, 656, 40, "white", c, 8, 1.5)
        s.text(x + 26, 1096, title, 20, c, bold=True)
        s.text(x + 180, 1096, sub, 16, "#555555")
    s.rect(30, 1140, 2040, 112, PALE[PURPLE], PURPLE)
    s.text(1050, 1178, "高可用设计：3节点容忍1节点故障 · ETCD Raft保证选主一致性 · PVC保证数据不丢", 23, "#6f36d9", "middle", True)
    s.lines(1050, 1208, ["扩容：增加Slave节点（不影响Master）· Sink横向扩展 · Redis分片可选", "监控：JVM metrics → Prometheus → Grafana · ETCD metrics · Redis INFO"], 18, "#888888", "middle", 28)
    s.save()


def provenance():
    base = "https://static001.infoq.cn/resource/image/"
    refs = [
        ("cognition-seven-layers", "0a/54/0a68413f9dbd3153b40a101e2661a654", "03-05 5. 认知篇：AI 编程市场观察和工具全景.html"),
        ("agentos-overview", "55/d5/55a755810905b687a3a8eccf503432d5", "03-18 18. 项目篇 OryxOS：技术方案文档.html"),
        ("agentos-layers", "8b/c3/8b1e501518bf0258513c17968ef7a2c3", "03-18 18. 项目篇 OryxOS：技术方案文档.html"),
        ("agentos-boundary", "9c/57/9c0530bb15f2da00971bf52649796957", "03-18 18. 项目篇 OryxOS：技术方案文档.html"),
        ("agentos-react", "9a/47/9a6d1bd19b98c62d5839512407a1ce47", "03-18 18. 项目篇 OryxOS：技术方案文档.html"),
        ("agentos-memory", "7f/ac/7fe51cd4e23b8cff897118929214cbac", "03-18 18. 项目篇 OryxOS：技术方案文档.html"),
        ("when-overview", "38/4b/38f1a8f1fae2276e6d10afddb34eea4b", "03-22 22. 项目篇 When：技术方案文档.html"),
        ("when-cluster", "f4/0d/f490901bd6401245959a42837b90cf0d", "03-22 22. 项目篇 When：技术方案文档.html"),
        ("when-timewheel", "fb/e8/fb7d3547da98b3c8eac6d146f3f6d8e8", "03-22 22. 项目篇 When：技术方案文档.html"),
        ("when-ha", "f3/b3/f319dce2e856c84ed29ccedbd6fe96b3", "03-22 22. 项目篇 When：技术方案文档.html"),
        ("when-lifecycle", "bd/65/bd1972b16b5c7961facbd91c09d80465", "03-22 22. 项目篇 When：技术方案文档.html"),
        ("when-sink", "5b/a5/5b58b09717cc9899d872d50e22d6c1a5", "03-22 22. 项目篇 When：技术方案文档.html"),
        ("when-deployment", "42/81/42663ca60076c41fe1ec3485e61c9e81", "03-22 22. 项目篇 When：技术方案文档.html"),
    ]
    data = {"course": "JK - 2026年企业级AI编程实战营【系统课】", "method": "使用可编辑 SVG 图元与文字按原图重绘；非像素级复刻。调整少量文字间距和容器高度以消除遮挡，透明图补白色背景。", "generator": "scripts/redraw_course_diagrams.py", "caveats": {"when-cluster": "原图TTL=10s，时间线恢复至12s，与10s目标不一致；独立心跳线程仍可能受全局GC停顿影响。", "when-timewheel": "原图含取模分片示意，与正文一致性Hash口径不同；O(1)、内存及精度为图中简化指标。", "when-ha": "保留原图同步复制、两个Slave、5s TTL及Controller/时间轮Master混用；正文采用异步副本与分离角色，零丢失与切换SLA未经验证。", "when-lifecycle": "原图成功后删除Redis及取消删除为早期流程示意；最终状态保留、投递权和幂等须独立设计，SET/Pipeline不等于磁盘落盘。", "when-sink": "原图同时含热加载和重启加载；SPI不自动实现动态热加载，重试次数与生命周期图不同。", "when-deployment": "原图固定主从拓扑与StatefulSet为示意，不能代替按时间轮分配角色或后续部署方案；PVC并不保证零丢失。"}, "images": [{"svg": f"{name}.svg", "source": base + path + ".png", "document": doc} for name, path, doc in refs]}
    (OUT / "sources.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cognition()
    agentos()
    when_overview()
    when_cluster()
    when_timewheel()
    when_ha()
    when_lifecycle()
    when_sink()
    when_deployment()
    provenance()


if __name__ == "__main__":
    main()
