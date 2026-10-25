"""Keep the source UML artwork; localize prose and correct Content.getText()."""

from pathlib import Path
from html import escape
import base64

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'public/images/frameworks/spring-ai'
source = ASSETS / 'spring-ai-message-api.jpg'
data = base64.b64encode(source.read_bytes()).decode()


def patch(x, y, w, h, lines, size=25, fill='white', align='start'):
    if isinstance(lines, str):
        lines = [lines]
    line_height = size * 1.32
    first = y + h / 2 - (len(lines) - 1) * line_height / 2 + size * .35
    tx = x + 5 if align == 'start' else x + w / 2
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>' + ''.join(
        f'<text x="{tx}" y="{first + i * line_height}" font-size="{size}" text-anchor="{align}">{escape(text)}</text>'
        for i, text in enumerate(lines)
    )


body = patch(24, 8, 680, 75, 'Spring AI 消息 API', 55)
body += patch(1260, 56, 488, 105, ['Content 提供文本内容', '与可选的元数据。'], 25)
body += patch(1073, 216, 660, 35, 'Media 承载多模态输入与输出。', 25)
# Leave every UML symbol and connector intact; replace only its legend text.
for y, label in [(158, '聚合'), (189, '持有'), (219, '继承'), (250, '类')]:
    body += patch(110, y, 89, 25, label, 17, '#f0f0f0')
# The reference image still shows getContent(); the 2.0.2 Content API uses getText().
body += patch(879, 113, 350, 34, '+ getText(): String', 27, '#f9c710')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1760" height="1435" viewBox="0 0 1760 1435" role="img" aria-labelledby="title desc" lang="zh-CN">
<title id="title">Spring AI 消息 API</title>
<desc id="desc">保留黄色 UML 类图的层级与连线，展示 Content、Message、MediaContent、四类消息和媒体及工具数据之间的关系。说明中文化，Content 的文本访问方法按 2.0.2 API 修正为 getText。</desc>
<rect width="1760" height="1435" fill="white"/>
<image width="1760" height="1435" href="data:image/jpeg;base64,{data}"/>
<g font-family="Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif" fill="#171717">{body}</g>
</svg>'''
(ASSETS / 'spring-ai-message-api-zh.svg').write_text(svg + '\n')
