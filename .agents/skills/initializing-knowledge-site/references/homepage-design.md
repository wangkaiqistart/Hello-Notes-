# 首页设计与本地 SVG

## 使用 Unslop

页面风格必须使用 `unslop`，参照其 SKILL.md、references/signs.md 与 references/tokens.md。先审视现有页面（新项目则审视模板），记录五行方向，再按间距、颜色、图标、文案、字体、布局、细节、视觉、动效九个层次处理。用户已经指定风格并授权创建时直接落实；需要用户决策时遵循会话已有授权，避免重复确认。每次最多三轮浏览器视觉比较，其余功能检查可用 DOM 和构建。

模板方向：产品是 Java/前端工程知识的阅读与记录站；性格是严谨、耐读、带一点手稿感；世界是工程手册与索引页；视觉重点是可展开的 Three.js 分层知识页；签名细节是同一套索引连线。

## 视觉基线

暖白纸面（#f7f4ee）、墨色文字（#1f1b16）、单一青绿强调（#176b62），4px 间距刻度、400/500 字重、中文具体文案。页面正文安静，丰富细节集中在一处有意义的知识页模型。不要生成泛用宇宙、发光球、粒子星云、渐变字、伪造数据或全大写宽字距标签。Java/前端站应使用对应名词与真实内容，不能只换品牌名。

## 本地 SVG 图片

- 所有产品插图、图标、favicon 与静态降级画面都用原创 SVG，保存到项目 `public/images/` 或 `src/assets/`。模板已提供知识分层页、Java 结构、前端布局和统一线图标。
- SVG 有 xmlns、viewBox，说明图有 title，HTML 引用提供准确 alt；纯装饰图用空 alt。图标统一 18px / 1.5 线宽。
- 不使用外部图片 URL、data URI、foreignObject、脚本或 image 内嵌 PNG/JPEG 冒充矢量。不能把截图作为产品插图；截图是验收证据。
- 插图紧跟用途说明，不直接跟在标题后当装饰；手机不溢出。

## Three.js 场景

Three.js 是交互画面而非静态图片，使用 canvas，本地 SVG 用于无 WebGL/无 JS/减少动态效果降级。来自本地依赖动态 import，仅首页加载；使用低面数哑光纸页和知识连线，不使用昂贵后处理或远程模型。桌面像素比上限 1.5，手机 1。

初次短暂展开后静止，拖动检查层次，点击播放才连续演示；按钮可暂停。没有滚动劫持或指针视差。减少动态效果时显示 SVG。离屏/后台停 RAF；ResizeObserver 更新尺寸；pagehide 释放 GPU/observer/事件，bfcache pageshow 重新初始化，context lost 显示 SVG。

## 检查

正常状态截图确认真正 Three.js 模型出现；`data-scene-state`（loading/running/paused/fallback）供诊断，不显示给读者。检查静止、拖动、播放/暂停、减少动态效果和手机布局。正文不加载 Three.js。

设计方法来源：Unslop by **Damir Sokolovsky**（[@heydamir](https://x.com/heydamir)），<https://heydamir.design/unslop>，**CC BY 4.0**。本说明按中文知识站、Three.js 与本地 SVG 需求改编；保留此署名，生成项目 README 也保留署名。
