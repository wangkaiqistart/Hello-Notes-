"""Retain source artwork; localize prose and correct verified old API labels."""
from pathlib import Path
from html import escape
import base64
ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT/'public/images/frameworks/spring-ai'
YELLOW='#f9c710'
def patch(x,y,w,h,lines,size=30,fill='white'):
 if isinstance(lines,str):lines=[lines]
 step=size*1.2;first=y+h/2-(len(lines)-1)*step/2+size*.35
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'+''.join(f'<text x="{x+w/2}" y="{first+i*step}" text-anchor="middle" font-size="{size}" fill="#242424">{escape(t)}</text>' for i,t in enumerate(lines))
def save(source,target,w,h,title,desc,labels):
 data=base64.b64encode((ASSETS/source).read_bytes()).decode()
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc" lang="zh-CN">
<title id="title">{title}</title><desc id="desc">{desc}</desc>
<rect width="{w}" height="{h}" fill="white"/><image width="{w}" height="{h}" href="data:image/jpeg;base64,{data}"/>
<g font-family="'PingFang SC', 'Microsoft YaHei', Arial, sans-serif">{''.join(patch(*s) for s in labels)}</g></svg>'''
 (ASSETS/target).write_text(svg+'\n')
save('structured-output-api.jpg','structured-output-api-zh.svg',2048,1044,'结构化输出转换器 API 数据流','格式指令和用户输入组成 Prompt；ChatModel 返回 ChatResponse，提取文本后由 Converter 转为类型 T。保留来源节点和连线，返回类型按 2.0.2 API 校正。',[
 (83,220,320,65,'原始输入',37),
 (1680,207,290,92,['结构化','输出 (T)'],35),
 (606,332,312,32,'格式指令',25),
 (318,461,220,38,'用户输入',25),
 (593,677,351,90,['输入与','格式指令'],35),
 (1202,677,292,91,['原始输出','（文本）'],35),
 (184,782,140,36,'数据流',25,'#efefef'),
 (184,835,115,36,'数据',25,'#efefef'),
 (184,897,145,69,['Spring AI','类'],25,'#efefef'),
 (884,946,344,50,'+ call(Prompt) : ChatResponse',23,YELLOW),
])
save('structured-output-hierarchy4.jpg','structured-output-hierarchy-zh.svg',2048,998,'结构化输出转换器类关系','保留接口、继承箭头与依赖关系，图例中文化；BeanOutputConverter 的映射器更新为 2.0.2 使用的 JsonMapper。',[
 (1821,43,96,28,'持有',18,'#efefef'),
 (1821,85,96,28,'继承',18,'#efefef'),
 (1821,126,96,28,'类',18,'#efefef'),
 (895,906,301,51,'JsonMapper',35),
])
