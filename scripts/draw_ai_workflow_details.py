"""Draw supplementary AI workflow diagrams without regenerating existing images."""

from draw_ai_notes_diagrams import OUT, card, vertical
from redraw_course_diagrams import SVG, BLUE, GREEN, ORANGE, PURPLE, RED, NAVY, INK, GRAY, PALE


def development_loop():
    s = SVG(
        'development-loop', 1100, 1150,
        '从任务到证据的开发循环',
        '本地检查指导修正，独立验收决定是否交接',
    )
    stages = [
        ('任务与基线', '读取契约、依赖与边界；准备隔离工作空间', BLUE),
        ('复现失败', '确认测试真正捕获目标行为，而非环境错误', PURPLE),
        ('最小实现', '只处理当前任务；保留变更与操作记录', BLUE),
        ('快速验证', '运行目标回归、类型或构建；读取失败证据', ORANGE),
        ('独立验收', '核对规格与代码质量；执行外部必要检查', PURPLE),
        ('交接与下一项', '保存版本、结果和限制；按依赖推进', GREEN),
    ]
    for i, (head, detail, color) in enumerate(stages):
        y = 140 + i * 145
        card(s, 60, y, 680, 110, f'{i + 1:02d}  {head}', detail, color)
        if i < len(stages) - 1:
            s.path([(400, y + 114), (400, y + 140)], '#96a4b4', 3)
    s.path([(744, 630), (775, 630), (775, 485), (744, 485)], ORANGE, 3)
    card(s, 805, 400, 255, 148, '允许重试', '失败原因可修正|有新证据|预算和范围允许', ORANGE, size=26)
    s.path([(775, 630), (775, 680), (800, 680)], RED, 3)
    card(s, 805, 605, 255, 150, '停止并交接', '需求或权限不明|无新证据|预算耗尽', RED, size=26)
    s.path([(744, 775), (775, 775), (775, 680)], RED, 3)
    s.text(550, 1045, '验收受保护：不能靠删测试、松断言或跳过场景变绿', 27, NAVY, 'middle', True)
    s.text(550, 1091, '新的任务上下文读取外置状态；人工审查与真实使用形成外层反馈', 23, GRAY, 'middle')
    s.save(OUT)


def spec_artifacts():
    vertical(
        'spec-artifacts', '规格产物的约束与追踪',
        '每一层都需要审查，变更后主动核对下游',
        [
            ('工程原则 · constitution', '质量、安全、兼容性与不可随意改变的约定'),
            ('行为规格 · spec', '用户场景、边界、失败行为与可判定的验收'),
            ('技术计划 · plan', '实现方案、接口、依赖和关键取舍'),
            ('任务清单 · tasks', '小增量、依赖顺序、文件范围与检查步骤'),
            ('实现与验证证据', '代码、测试和运行记录；反向核对规格与计划'),
        ],
        '勾选任务只表示进度，完成需要证据',
    )


def superpowers_workflow():
    vertical(
        'superpowers-workflow', 'Superpowers 的执行主线',
        '流程随任务裁剪，规格与质量都要检查',
        [
            ('澄清与设计', '确认目标、非目标、约束与候选方案'),
            ('准备工作空间', '隔离文件与分支；确认环境和测试基线'),
            ('拆分计划', '写清依赖、修改范围和每项验证步骤'),
            ('逐项实现', '按需使用子 Agent；测试先红，再绿，再重构'),
            ('审查与修正', '核对规格符合性和代码质量，补充相关回归'),
            ('验证与交接', '检查整体差异，报告结果、限制与后续选择'),
        ],
        '子 Agent 隔离上下文，worktree 隔离工作文件',
    )


if __name__ == '__main__':
    development_loop()
    spec_artifacts()
    superpowers_workflow()
