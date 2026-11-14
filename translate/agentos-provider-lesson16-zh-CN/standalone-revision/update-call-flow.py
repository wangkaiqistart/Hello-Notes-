from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

base = Path(__file__).resolve().parent
original = Image.open(base / 'before-provider-call-flow.png').convert('RGB')
updated = original.copy()
font_path = '/System/Library/Fonts/STHeiti Light.ttc'

def label(rect, text, size, color, background=(255, 255, 255)):
    x0, y0, x1, y1 = rect
    scale = 3
    patch = Image.new('RGB', ((x1-x0)*scale, (y1-y0)*scale), background)
    draw = ImageDraw.Draw(patch)
    font = ImageFont.truetype(font_path, size*scale)
    bbox = draw.textbbox((0, 0), text, font=font)
    width, height = bbox[2]-bbox[0], bbox[3]-bbox[1]
    assert width < patch.width-12, (text, width, patch.width)
    draw.text(((patch.width-width)/2-bbox[0], (patch.height-height)/2-bbox[1]), text, font=font, fill=color)
    updated.paste(patch.resize((x1-x0, y1-y0), Image.Resampling.LANCZOS), (x0,y0))

body = (57, 71, 93)
muted = (100, 116, 139)
label((530, 192, 1260, 238), '① 按 Profile 路由到对应的 ProviderAdapter', 29, body)
label((570, 248, 1235, 296), '② 组装消息、模型参数与工具 Schema', 29, body)
label((670, 312, 1100, 363), '提交 begin 后发起调用', 27, (71, 85, 105), original.getpixel((700, 315)))
label((1125, 375, 1310, 409), 'ChatResponse', 25, muted)
label((500, 442, 1320, 488), '③ 提交 complete：状态 / 用量 / 耗时 / 错误码', 29, body)
label((448, 488, 690, 521), '返回 ModelResponse', 23, muted)
output = base.parents[2] / 'public/images/projects/agent-os/provider-call-flow.png'
updated.save(output)
print(output)
