"""Embed source diagrams intact and replace prose labels; keep API identifiers."""
from pathlib import Path
from html import escape
import base64
ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT/'public/images/frameworks/spring-ai'
YELLOW='#f9c710'
def patch(x,y,w,h,lines,size=30,fill='white',color='#242424'):
 if isinstance(lines,str):lines=[lines]
 lh=size*1.2;first=y+h/2-(len(lines)-1)*lh/2+size*.35
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'+''.join(f'<text x="{x+w/2}" y="{first+i*lh}" text-anchor="middle" font-size="{size}" fill="{color}">{escape(t)}</text>' for i,t in enumerate(lines))
def save(name,w,h,title,desc,body):
 path=ASSETS/name;data=base64.b64encode(path.read_bytes()).decode();mime='image/png' if name.endswith('.png') else 'image/jpeg'
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc" lang="zh-CN">
<title id="title">{title}</title><desc id="desc">{desc}</desc>
<rect width="{w}" height="{h}" fill="white"/><image width="{w}" height="{h}" href="data:{mime};base64,{data}"/>
<g font-family="'PingFang SC', 'Microsoft YaHei', Arial, sans-serif">{body}</g></svg>'''
 (ASSETS/(path.stem+'-zh.svg')).write_text(svg+'\n')
body=''
for y,label in [(1085,'聚合'),(1122,'持有'),(1153,'继承'),(1189,'类')]:body+=patch(174,y,101,32,label,19)
save('advisors-api-classes.jpg',1600,1276,'Advisors API 类型关系','保留 UML 类型、方法签名及继承聚合关系，图例中文化。CallAdvisor 与 StreamAdvisor 分别对应同步与流式处理。',body)
body=''
for spec in [
(135,242,345,111,['Prompt 转换为','ChatClientRequest'],32),
(1022,246,411,105,['ChatClientResponse','提取 ChatResponse'],32),
(148,750,320,96,'调用前处理',37),
(1062,752,323,92,'调用后处理',37),
(584,1016,405,133,['内部 Advisor','调用模型'],42,YELLOW),
(586,1440,405,85,'聊天模型',48,YELLOW)]:body+=patch(*spec)
save('advisors-flow.jpg',1543,1600,'Advisor 请求与响应流程','沿用黄色节点和六个步骤，左侧请求进入 Advisor 链并调用模型，右侧响应反向经过链并提取模型响应。',body)
body=''
for spec in [
(20,8,680,60,'Advisors：非流式调用',40),
(886,8,690,60,'Advisors：流式调用',40),
(1311,335,238,23,'Flux<ChatClientResponse>',18),
(292,571,133,33,'内部调用',24,'#fffae6'),
(1162,570,131,33,'内部调用',24,'#fffae6'),
(261,745,197,42,'聊天模型',25,YELLOW),
(1133,745,187,42,'聊天模型',25,YELLOW)]:body+=patch(*spec)
save('advisors-non-stream-vs-stream.jpg',1600,812,'Advisor 非流式与流式处理对比','左侧返回单个 ChatClientResponse，右侧返回 Flux 中的多个响应。保留处理链与模型节点，旧 AdvisedResponse 标签同步为 ChatClientResponse。',body)
body=''
for spec in [
(50,207,181,25,'递归 Advisor',16,YELLOW),
(73,317,58,27,'调用前',14),
(151,317,56,27,'调用后',14),
(70,550,125,32,'聊天模型',18),
(42,78,190,39,['上游 Advisor','ABC'],15,YELLOW),
(42,415,190,40,['下游 Advisor','XYZ'],15,YELLOW)]:body+=patch(*spec)
body+='<rect x="0" y="407" width="24" height="124" fill="white"/><text x="17" y="469" text-anchor="middle" transform="rotate(-90 17 469)" font-size="16" fill="#dba900">可重复执行</text>'
save('advisors-recursive.png',291,627,'递归 Advisor 的下游循环','上游 Advisor 只在进入循环前执行，递归 Advisor 的条件判断控制是否重复下游 Advisor 与聊天模型，保留循环范围和返回箭头。',body)
