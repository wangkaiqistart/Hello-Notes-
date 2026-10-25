"""Preserve source artwork and arrows; replace explanatory labels only."""
from pathlib import Path
import base64
from html import escape
root=Path(__file__).resolve().parents[2]
assets=root/'public/images/frameworks/spring-ai'
data=base64.b64encode((assets/'structured-output-basic.png').read_bytes()).decode()
blue='#1979c8';gray='#868e93';pale='#e7f5ff'
def patch(x,y,w,h,lines,size=30,color=blue,fill='white'):
 if isinstance(lines,str):lines=[lines]
 lh=size*1.24
 first=y+h/2-(len(lines)-1)*lh/2+size*.35
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'+''.join(f'<text x="{x+w/2}" y="{first+i*lh}" text-anchor="middle" font-size="{size}" fill="{color}">{escape(t)}</text>' for i,t in enumerate(lines))
labels=''
for spec in [
 (22,23,280,138,['自定义返回类型','<T>'],36,blue,pale),
 (420,194,290,109,['Schema','生成器'],34,blue,pale),
 (596,104,200,49,'生成',31,blue,'white'),
 (1532,72,250,49,'目标类型',33,blue,'white'),
 (44,286,186,47,'提供',30,blue,'white'),
 (398,352,172,47,'提示词',34,gray,'white'),
 (408,417,162,43,'上下文',29,gray,'white'),
 (423,475,246,137,['系统消息：','按 JSON Schema','格式返回结果'],27,blue,pale),
 (83,550,105,42,'用户',30,gray,'white'),
 (206,480,170,49,'问题',30,gray,'white'),
 (453,650,179,45,'问题',28,gray,'white'),
 (1313,512,206,44,'模型回答',29,gray,'white'),
 (1320,583,191,38,'JSON 结果',25,gray,'white'),
 (1229,671,321,75,['目标：生成符合','输入 Schema 的 JSON'],26,gray,'white'),
 (1720,523,239,105,['类型','转换器'],36,blue,pale),
 (839,898,535,74,'结构化响应 <T>',33,blue,'white')]: labels+=patch(*spec)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="2048" height="974" viewBox="0 0 2048 974" role="img" aria-labelledby="title desc" lang="zh-CN">
<title id="title">结构化输出的默认转换流程</title>
<desc id="desc">用户提供返回类型，生成 JSON Schema 并加入系统上下文；模型返回 JSON 文本，转换器依据目标类型解析为对象。图示提示词驱动方式，格式要求并非严格保证。</desc>
<rect width="2048" height="974" fill="white"/>
<image width="2048" height="974" href="data:image/png;base64,{data}"/>
<g font-family="'PingFang SC', 'Microsoft YaHei', Arial, sans-serif">{labels}</g>
</svg>'''
(assets/'structured-output-basic-zh.svg').write_text(svg+'\n')
