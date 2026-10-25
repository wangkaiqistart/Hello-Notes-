"""Keep source artwork, arrows and loop boundaries; localize labels only."""
from pathlib import Path
from html import escape
import base64
r=Path(__file__).resolve().parents[2];assets=r/'public/images/frameworks/spring-ai'
source=assets/'structured-output-self-correction.png'
blue='#1979c8';gray='#868e93';pale='#e7f5ff';pink='#ff8585';red='#ef3333'
def patch(x,y,w,h,lines,size=28,color=blue,fill='white'):
 if isinstance(lines,str):lines=[lines]
 step=size*1.2;first=y+h/2-(len(lines)-1)*step/2+size*.35
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'+''.join(f'<text x="{x+w/2}" y="{first+i*step}" text-anchor="middle" font-size="{size}" fill="{color}">{escape(t)}</text>' for i,t in enumerate(lines))
labels=''.join(patch(*s) for s in [
(22,34,204,106,['自定义返回类型','<T>'],27,blue,pale),
(346,159,160,69,['Schema','生成器'],28,blue,pale),
(452,78,132,35,'生成',28),
(1700,8,181,36,'目标类型',28),
(40,235,133,38,'提供',28),
(286,277,145,40,'提示词',28,gray),
(310,336,120,30,'上下文',24,gray),
(322,390,175,79,['系统消息：','按 JSON Schema','格式返回'],21,blue,pale),
(61,432,90,33,'用户',24,gray),
(157,390,125,35,'问题',26,gray),
(334,513,155,35,'问题',25,gray),
(947,111,545,43,'结构化输出校验 Advisor',31,'white','#adddff'),
(1077,199,226,45,'校验错误',31,'white',pink),
(829,306,162,36,'上下文',26,gray),
(808,357,174,74,['系统消息：','按 JSON Schema','格式返回'],21,blue,pale),
(835,461,122,32,'问题',24,gray),
(809,523,166,33,'校验错误',24,'white',pink),
(1295,397,153,36,'模型回答',27,gray),
(1297,450,149,38,'JSON 结果',23,gray),
(1547,342,52,36,'否',25,red),
(1688,382,61,32,'是',25),
(1788,404,188,77,['类型','转换器'],32,blue,pale),
(888,695,380,43,'结构化响应 <T>',32),
])
labels+='<polygon points="1527,441 1610,390 1695,441 1610,488" fill="white"/><text x="1610" y="433" text-anchor="middle" font-size="21" fill="#ef3333">符合</text><text x="1610" y="461" text-anchor="middle" font-size="21" fill="#ef3333">Schema？</text>'
h=1420/3906*2048
data=base64.b64encode(source.read_bytes()).decode()
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="2048" height="{h}" viewBox="0 0 2048 {h}" role="img" aria-labelledby="title desc" lang="zh-CN">
<title id="title">Schema 校验与自动纠正循环</title><desc id="desc">目标类型生成 JSON Schema，模型回答先进行校验；通过后转换为对象，未通过则将校验错误加入下一轮请求，在重试上限内再次调用模型。</desc>
<rect width="2048" height="{h}" fill="white"/><image width="2048" height="{h}" href="data:image/png;base64,{data}"/>
<g font-family="'PingFang SC', 'Microsoft YaHei', Arial, sans-serif">{labels}</g></svg>'''
(assets/'structured-output-self-correction-zh.svg').write_text(svg+'\n')
