"""Build editable SVG diagrams for the AI programming notes."""
from pathlib import Path
from redraw_course_diagrams import SVG, BLUE, GREEN, ORANGE, PURPLE, RED, NAVY, INK, GRAY, PALE

OUT = Path(__file__).resolve().parents[1] / 'public/images/ai-programming/notes'


def card(s, x, y, w, h, title, detail='', color=BLUE, size=27):
    s.rect(x, y, w, h, PALE[color], color, 18, 2)
    s.rect(x, y + 20, 6, h - 40, color, 'none', 3, 0)
    s.text(x + 26, y + 39, title, size, NAVY, bold=True)
    lines = detail.split('|') if detail else []
    s.lines(x + 26, y + 74, lines, 22, '#536477', step=31)


def vertical(name, title, subtitle, stages, footer=None):
    s = SVG(name, 820, 170 + len(stages) * 146 + (55 if footer else 0), title, subtitle)
    colors = [BLUE, PURPLE, GREEN, ORANGE]
    for i, (head, detail) in enumerate(stages):
        y = 140 + i * 146
        card(s, 58, y, 704, 112, f'{i + 1:02d}  {head}', detail, colors[i % 4])
        if i < len(stages) - 1:
            s.path([(410, y + 114), (410, y + 140)], '#96a4b4', 3)
    if footer:
        s.text(410, s.h - 35, footer, 21, GRAY, 'middle')
    s.save(OUT)


def learning():
    vertical('learning-path', 'AI 编程的学习路径', '从理解变化，到验证交付，再到经验复用', [
        ('认知', '判断做什么、为什么做；明确人的责任'),
        ('方法', '规定怎么做、怎样检查；形成执行约束'),
        ('项目', '把方法落到架构、代码、测试和部署'),
        ('沉淀', '把判断提炼成规则、Skill、模板和公开成果'),
    ], '目标清楚 · 边界可控 · 结果可查')
    s = SVG('engineering-shift', 900, 910, '工作方式与能力养成', '代码生成加速，目标、取舍与验证仍需要判断')
    for x, title, lines, c in [(40, '逐步手工实现', ['理解需求', '设计', '编码', '测试', '交付'], BLUE), (470, '组织 AI 协作', ['定义目标', '准备上下文', '组织 AI 执行', '验证证据', '交付并沉淀'], PURPLE)]:
        s.panel(x, 140, 390, 410, title, c, size=27, strip=False)
        for i, label in enumerate(lines):
            y = 212 + i * 65
            s.rect(x + 34, y, 322, 43, 'white', c, 10, 1.5)
            s.text(x + 195, y + 30, label, 23, INK, 'middle')
            if i < 4:
                s.path([(x + 195, y + 45), (x + 195, y + 61)], c, 2)
    s.text(450, 607, '个人能力闭环', 28, NAVY, 'middle', True)
    positions = [(40, 640), (335, 640), (630, 640), (630, 760), (335, 760)]
    for (x, y), title, detail, c in zip(positions, ['理解原理', '独立取舍', '借助 AI', '验证结果', '复盘沉淀'], ['形成问题模型', '比较候选方案', '执行具体任务', '检查关键行为', '留下可复用经验'], [BLUE, PURPLE, GREEN, ORANGE, BLUE]):
        s.rect(x, y, 230, 82, PALE[c], c, 14, 2)
        s.text(x + 115, y + 33, title, 25, NAVY, 'middle', True)
        s.text(x + 115, y + 64, detail, 20, GRAY, 'middle')
    for points in [[(274, 681), (331, 681)], [(569, 681), (626, 681)], [(745, 726), (745, 756)], [(626, 801), (569, 801)], [(331, 801), (155, 801), (155, 726)]]:
        s.path(points, '#96a4b4', 3)
    s.save(OUT)
    vertical('tool-evaluation', '从观察信号到工具决策', '让选型经过自己的任务与失败验证', [
        ('观察信号', '宣传、榜单、项目发布；只建立候选清单'),
        ('核对官方信息', '检查仓库、文档、版本、支持范围和维护情况'),
        ('执行真实任务', '用最小任务检查能力、约束和验收结果'),
        ('记录失败与成本', '记录成功率、延迟、调用费用和维护成本'),
        ('作出项目决策', '比较收益与风险；保留替换和回退方式'),
    ])


def collaboration():
    s = SVG('collaboration-loop', 900, 920, '人机协作的交付闭环', '人确定目标与边界，AI 执行，独立检查提供证据')
    positions = [(55, 140), (485, 140), (485, 345), (55, 345), (55, 550), (485, 550)]
    items = [('明确目标', '价值、范围、优先级|写出可检查的验收标准', BLUE), ('准备上下文', '接口、规则、依赖与环境|明确权限和文件范围', PURPLE), ('拆成小任务', '按依赖顺序安排|每项都能独立验收', GREEN), ('AI 执行', '按任务修改与验证|记录变更和运行结果', BLUE), ('独立验证', '测试、构建与 Review|核查失败和风险边界', ORANGE), ('人工放行', '决定是否交付|监控、回滚与经验沉淀', GREEN)]
    for (x, y), (title, detail, c) in zip(positions, items):
        card(s, x, y, 360, 140, title, detail, c)
    paths = [[(420, 210), (480, 210)], [(665, 285), (665, 340)], [(480, 415), (420, 415)], [(235, 490), (235, 545)], [(420, 620), (480, 620)]]
    for p in paths:
        s.path(p, '#96a4b4', 3)
    s.rect(55, 770, 790, 105, PALE[RED], RED, 16, 2)
    s.text(450, 809, '未通过：收集证据 → 修正任务 → 有界重试', 26, '#a73237', 'middle', True)
    s.text(450, 849, '需求不清、超出权限或超过预算时停止，交由人处理', 22, INK, 'middle')
    s.path([(235, 694), (235, 752), (450, 752), (450, 766)], RED, 2)
    s.text(450, 602, '通过', 20, GREEN, 'middle')
    s.save(OUT)


def specs():
    s = SVG('sdd-harness', 900, 810, '规格与执行约束如何配合', '把目标、边界、执行和验证放到同一个闭环')
    card(s, 50, 140, 800, 144, 'SDD：定义目标与验收', '目标与非目标 · 输入输出 · 状态与接口|成功条件 · 异常场景 · 验证标准', BLUE)
    s.path([(450, 288), (450, 331)], BLUE, 3)
    s.rect(50, 335, 800, 292, PALE[PURPLE], PURPLE, 18, 2)
    s.text(450, 378, 'Harness：约束执行环境', 28, NAVY, 'middle', True)
    groups = [(75, 408, '知道什么', '项目说明、上下文、规则'), (475, 408, '能做什么', '权限、工具、工作空间'), (75, 510, '如何验收', '流程、测试、Review'), (475, 510, '如何停止', '预算、失败处理、回滚')]
    for x, y, title, detail in groups:
        s.rect(x, y, 350, 86, 'white', '#b69be9', 12, 1.5)
        s.text(x + 175, y + 33, title, 24, '#6c46af', 'middle', True)
        s.text(x + 175, y + 65, detail, 21, INK, 'middle')
    s.path([(450, 631), (450, 671)], GREEN, 3)
    card(s, 50, 675, 800, 100, '可控执行与证据验收', '完成标准由测试、运行结果和独立复核共同确认', GREEN)
    s.save(OUT)
    s = SVG('spec-workflows', 900, 820, '两种规格工作流', '按项目阶段选择流程，具体命令以工具版本为准')
    for x, title, sub, stages, c in [(40, 'Spec-Kit', '从零建立项目约定', ['constitution · 工程原则', 'specify · 明确需求', 'clarify · 澄清歧义', 'plan · 技术计划', 'tasks · 任务拆分', 'implement · 实现验证'], BLUE), (470, 'OpenSpec', '已有系统的增量变更', ['propose · 提出变更', 'apply · 实施与验证', 'archive · 归档结果'], PURPLE)]:
        s.panel(x, 140, 390, 625, title, c, size=30, strip=False)
        s.text(x + 195, 224, sub, 22, GRAY, 'middle')
        step = 75 if len(stages) == 6 else 150
        for i, label in enumerate(stages):
            y = 260 + i * step
            s.rect(x + 25, y, 340, 52, 'white', c, 10, 1.5)
            s.text(x + 195, y + 34, label, 22, INK, 'middle')
            if i < len(stages) - 1:
                s.path([(x + 195, y + 56), (x + 195, y + step - 5)], c, 2)
    s.save(OUT)
    vertical('skill-loading', 'Skill 的渐进式加载', '先判断是否适用，再读取执行所需的内容', [('元数据', '名称与描述：发现能力，判断触发条件'), ('正文', '输入、步骤、边界、失败处理和验收要求'), ('参考资料与脚本', '只在具体步骤需要时读取或运行')], '减少无关上下文，同时保留可执行细节')


def loop():
    s = SVG('loop-control', 900, 1030, 'Loop Engineering 的运行控制', '每次继续执行，都要有状态、证据和剩余预算')
    stages = [(140, '触发与发现任务', '定时、事件或目标驱动'), (275, '准备上下文与状态', '加载规则、工作空间和上次进度'), (410, '执行并记录', '调用工具，记录操作、结果与成本')]
    for y, title, detail in stages:
        card(s, 170, y, 560, 100, title, detail, BLUE)
        s.path([(450, y + 104), (450, y + 130)], '#96a4b4', 3)
    s.rect(170, 545, 560, 100, PALE[ORANGE], ORANGE, 18, 2)
    s.text(450, 585, '独立验证', 28, NAVY, 'middle', True)
    s.text(450, 620, '测试、检查器、状态读回与运行指标', 22, INK, 'middle')
    s.path([(450, 649), (450, 700)], ORANGE, 3)
    s.text(468, 680, '失败', 21, RED)
    card(s, 170, 705, 560, 105, '检查失败类型与预算', '可修正且预算充足：退避后重试', PURPLE)
    s.path([(170, 760), (85, 760), (85, 325), (165, 325)], PURPLE, 3)
    s.text(100, 545, '重试', 21, PURPLE)
    s.path([(730, 595), (820, 595), (820, 890), (735, 890)], GREEN, 3)
    s.text(800, 572, '成功', 21, GREEN, 'middle')
    card(s, 490, 850, 290, 120, '完成归档', '保存结果与运行记录', GREEN, size=26)
    s.path([(320, 814), (320, 845)], RED, 3)
    card(s, 120, 850, 300, 120, '停止或人工处理', '不可恢复、超权限|超出轮数或成本预算', RED, size=26)
    s.save(OUT)


def project_diagrams():
    vertical('agentos-modules', 'AgentOS 的实现顺序', '先打通最小执行闭环，再补齐扩展能力', [('工程地基与模型接入', '日志、监控、API 规范 → Provider'), ('执行与工具', 'ReAct → CLI / Notify → Tool'), ('状态与运行环境', 'Memory → Sandbox → 定时任务'), ('接口与扩展', 'Web Service → 主流程串联 → 插件化 → 动态管理')])
    s = SVG('agentos-dependencies', 900, 680, 'AgentOS 能力依赖', '箭头表示主要依赖与集成方向')
    card(s, 50, 140, 320, 100, 'Provider', '统一模型调用', BLUE)
    card(s, 530, 140, 320, 100, 'ReAct', '组织模型与工具循环', PURPLE)
    s.path([(375, 190), (525, 190)], BLUE, 3)
    for x, title, detail in [(50, 'Memory / Tool', '上下文记忆与工具执行'), (530, 'CLI / Channel / Sandbox', '消息入口与执行边界')]:
        card(s, x, 335, 320, 110, title, detail, GREEN, size=23)
    s.path([(690, 245), (690, 285), (210, 285), (210, 330)], PURPLE, 3)
    s.path([(690, 245), (690, 330)], PURPLE, 3)
    card(s, 290, 530, 320, 100, 'Web Service', '将能力开放给业务系统', ORANGE)
    s.path([(210, 450), (210, 580), (285, 580)], GREEN, 3)
    s.save(OUT)
    s = SVG('agentos-components', 900, 740, 'Agent 运行底座的五个组件', '模型、循环、记忆、工具与执行环境各自承担职责')
    card(s, 270, 305, 360, 118, 'ReAct Loop', '调度执行、累积状态与终止', PURPLE)
    around=[(40, 140, 'Provider', '屏蔽模型厂商差异', BLUE), (500, 140, 'Memory', '保存会话与跨会话记忆', GREEN), (40, 540, 'Tools', '连接工具与外部能力', ORANGE), (500, 540, 'Environment', '限制文件、命令与网络', BLUE)]
    for x, y, title, detail, c in around:
        card(s, x, y, 360, 110, title, detail, c)
    for p in [[(360, 305), (220, 254)], [(540, 305), (680, 254)], [(360, 423), (220, 536)], [(540, 423), (680, 536)]]:
        s.path(p, '#96a4b4', 3)
    s.save(OUT)
    s = SVG('when-architecture', 900, 1000, 'When 节点内的数据流', '协调、持久化、内存调度与异步投递分别承担职责')
    stages=[(140, 'HTTP API / gRPC API', '统一接收外部请求与内部转发', BLUE), (285, '接入与路由 → 消息服务 → 状态机', '按时间轮归属处理请求和状态变更', PURPLE), (500, 'Redis 持久化', '保存消息与状态，成功后才进入调度', RED), (645, '多层时间轮', '内存索引与到期触发', GREEN), (790, 'Due Handler → Sink SPI', '取得投递权，异步投递并更新状态', ORANGE)]
    for y, title, detail, c in stages:
        card(s, 170, y, 670, 100, title, detail, c, size=25)
    for a,b in [(240,285),(385,500),(600,645),(745,790)]:
        s.path([(505,a+4),(505,b-5)], '#96a4b4',3)
    s.rect(25, 400, 275, 76, PALE[BLUE], BLUE, 14, 2)
    s.text(162, 432, 'ETCD 协调', 24, NAVY, 'middle', True)
    s.text(162, 461, '节点、角色与时间轮归属', 19, INK, 'middle')
    s.path([(300, 438), (350, 438), (350, 390)], BLUE, 2)
    s.save(OUT)
    vertical('when-replication', '异步副本与恢复路径', 'Redis 保存权威状态，内存副本减少恢复时间', [('写入 Redis', '先持久化消息和状态，写入失败则不返回成功'), ('加入 Master 时间轮', '接收、调度并投递当前时间轮的消息'), ('异步同步到 Slave', '同步不阻塞业务返回；失败后标记 out-of-sync'), ('故障后重建与接管', '补齐 Redis 中的未完成消息，再恢复调度')])
    s = SVG('when-state-machine', 900, 1070, '延时消息状态流转', '成功、重试、失败和取消需要各自明确的状态与条件')
    stages = [('Submit → PERSISTED', '提交并完成持久化'), ('SCHEDULED → DUE', '进入时间轮，等待到期'), ('DELIVERING', '取得投递权后异步调用 Sink')]
    for i,(title,detail) in enumerate(stages):
        y=140+i*150
        card(s,170,y,560,100,title,detail,BLUE if i<2 else PURPLE)
        if i<2:s.path([(450,y+104),(450,y+145)],'#96a4b4',3)
    outcomes=[(35,'DELIVERED','投递成功',GREEN),(335,'RETRYING','可重试失败',ORANGE),(635,'FAILED','不可重试或超限',RED)]
    s.path([(450,544),(450,600),(150,600)],'#96a4b4',2,False)
    s.path([(450,600),(750,600)],'#96a4b4',2,False)
    for x,title,detail,c in outcomes:
        card(s,x,660,230,110,title,detail,c,size=22)
        s.path([(x+115,600),(x+115,655)],c,2)
    s.path([(450,775),(450,840),(885,840),(885,340),(735,340)],ORANGE,2)
    s.text(680,823,'退避后重新入轮',21,ORANGE,'middle')
    card(s,170,900,560,100,'CANCELLED','仅允许的状态可取消；与投递竞争时执行原子校验',RED,size=26)
    s.path([(170,340),(15,340),(15,950),(165,950)],RED,2)
    s.text(35,865,'取消',21,RED)
    s.save(OUT)


def main():
    learning()
    collaboration()
    specs()
    loop()
    project_diagrams()


if __name__ == '__main__':
    main()
