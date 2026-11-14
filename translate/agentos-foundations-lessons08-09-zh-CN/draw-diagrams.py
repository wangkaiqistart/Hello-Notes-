from pathlib import Path
from html import escape

OUTPUT = Path(__file__).resolve().parents[2] / 'public/images/projects/agent-os'
OUTPUT.mkdir(parents=True, exist_ok=True)
FONT = 'Arial, PingFang SC, Microsoft YaHei, sans-serif'
INK, MUTED = '#334155', '#64748b'
PALETTES = {'purple': ('#eef2ff', '#818cf8'), 'blue': ('#eff6ff', '#60a5fa'), 'gold': ('#fffbeb', '#f59e0b'), 'green': ('#ecfdf5', '#34d399'), 'gray': ('#f8fafc', '#cbd5e1')}

class Diagram:
    def __init__(self, width, height, title, desc):
        self.width, self.height = width, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">', f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>', '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"/></marker></defs>', f'<rect width="{width}" height="{height}" rx="18" fill="white"/><g font-family="{FONT}">']
    def text(self, x, y, text, size=25, bold=False, color=INK):
        self.parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(text)}</text>')
    def box(self, x, y, w, h, title, lines=(), palette='blue', title_size=29, body_size=23):
        fill, stroke = PALETTES[palette]
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        count=len(lines);top=y+(h-(title_size+count*32))/2+title_size-4
        self.text(x+w/2,top,title,title_size,True)
        for i,line in enumerate(lines):self.text(x+w/2,top+36+i*32,line,body_size,color=MUTED)
    def arrow(self, path):
        self.parts.append(f'<path d="{path}" fill="none" stroke="#94a3b8" stroke-width="2.5" stroke-linejoin="round" marker-end="url(#arrow)"/>')
    def save(self, name):
        self.parts.extend(['</g></svg>'])
        (OUTPUT/name).write_text('\n'.join(self.parts)+'\n')

# Five conceptual components, retaining the source's card-based presentation.
d=Diagram(1000,555,'Agent 的五个组件','Loop 协调模型决策、工具行动与记忆，工具作用于受控环境，结果进入下一次决策。')
d.box(50,25,900,90,'Loop · 协调下一步', ['继续 / 完成 / 超限 / 超时 / 中断'], 'purple')
d.arrow('M 500 115 L 500 175')
d.box(40,185,270,135,'LLM · 决策',['选择工具与参数','或形成最终回答'],'blue')
d.box(365,185,270,135,'Tools · 行动',['执行结构化请求','返回结果或错误'],'gold')
d.box(690,185,270,135,'Memory · 状态',['会话过程','可复用的长期事实'],'green')
d.arrow('M 310 250 L 365 250');d.arrow('M 635 250 L 690 250')
d.arrow('M 825 320 L 825 370 L 175 370 L 175 320')
d.text(500,360,'观察结果进入下一次决策',24,color=MUTED)
d.box(50,415,900,110,'Environment · 交互对象与约束',['文件 / 网络 / 业务服务 / 用户入口 / 凭证与白名单'],'gray')
d.save('foundations-components.svg')

# Main runtime flow; no pure-text intermediate response that silently continues.
d=Diagram(1000,730,'一次轮次的模型与工具循环','轮次开始后构造 Prompt，ChatModel 返回回答或工具意图；执行工具后回填完整历史，检查直接返回与循环约束。')
d.box(95,25,600,76,'开始轮次',['会话租约 · 轮次记录 · 截止时间'],'purple',28,23)
d.arrow('M 395 101 L 395 135')
d.box(95,140,600,76,'构造 Prompt',['指令 + 记忆 + 历史；工具放请求选项'],'gray',28,23)
d.arrow('M 395 216 L 395 255')
d.box(95,260,600,88,'Provider → ChatModel',['请求一次模型，记录 llm_calls'],'blue',28,23)
d.arrow('M 695 302 L 770 302');d.text(735,282,'回答',21,color=MUTED)
d.box(775,260,190,88,'结束轮次',['保存最终结果'],'green',27,22)
d.arrow('M 395 348 L 395 410');d.text(480,387,'工具意图',23,color=MUTED)
d.box(95,415,600,105,'ToolExecutor → ToolCallingManager',['执行受治理的 ToolCallback','记录 tool_invocations'],'gold',26,23)
d.arrow('M 695 607 L 870 607 L 870 348');d.text(831,580,'直接返回',23,color=MUTED)
d.arrow('M 395 520 L 395 565')
d.box(95,570,600,76,'回填完整历史',['助手工具请求 + 工具结果'],'gray',28,23)
d.arrow('M 95 607 L 40 607 L 40 303 L 95 303')
d.text(500,702,'每次继续前检查：迭代上限 / 工具限额 / 剩余时间 / 取消 / 租约',24,color=MUTED)
d.save('foundations-runtime.svg')

# Four responsibility layers, with source-era SQLite and ProfileLoader corrected.
d=Diagram(1000,810,'AgentOS 四层职责','三种触发源进入同一引擎，Provider、Memory 与 Tool 提供能力，支撑层承载定义加载、关系存储、白名单和审计。')
d.box(40,25,920,110,'入口与触发',['CLI Channel     ·     REST     ·     AgentScheduler'],'purple',30,25)
d.arrow('M 500 135 L 500 175')
d.box(40,180,920,125,'运行引擎',['AgentService → ReActLoop','PromptBuilder 组装上下文 · ToolExecutor 发起工具执行'],'blue',30,24)
d.arrow('M 500 305 L 500 350')
d.text(500,381,'可替换能力',30,True)
d.box(40,410,285,105,'ProviderService',['具名 ChatModel 映射'],'blue',27,23)
d.box(358,410,285,105,'MemoryService',['会话 + 长期记忆'],'green',27,23)
d.box(676,410,285,105,'ToolRegistry',['本地 / MCP 回调'],'gold',27,23)
d.arrow('M 500 515 L 500 555')
d.box(40,560,920,135,'支撑设施',['AgentLoader / ContextLoader · PostgreSQL / Flyway','WhitelistSandbox · 日志 · 模型与工具审计'],'gray',30,24)
d.text(500,749,'Agent 定义与长期记忆文件位于工作区；模型服务与 MCP 可在应用外部。',23,color=MUTED)
d.text(500,783,'图示为目标职责关系；多租户、强隔离和集群能力需另行建设。',23,color=MUTED)
d.save('foundations-layers.svg')
print('Wrote 3 diagrams')
