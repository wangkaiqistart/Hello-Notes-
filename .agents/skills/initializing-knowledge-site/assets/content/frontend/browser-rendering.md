---
title: 浏览器布局与页面渲染
description: 从 DOM 和 CSS 理解布局，定位横向溢出与不必要的重排。
sidebar:
  order: 1
---

## 结构和样式共同决定布局

HTML 提供结构，CSS 决定呈现规则，浏览器再计算布局、绘制与合成。改变几何尺寸可能影响其他元素布局，某些 transform 和 opacity 变化可以走不同的合成路径；实际效果需要性能工具验证。

```css
.reading-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(16rem, 22rem);
  gap: 2rem;
}

@media (max-width: 48rem) {
  .reading-layout {
    grid-template-columns: minmax(0, 1fr);
  }
}
```

`minmax(0, 1fr)` 允许网格项收缩，有助于处理长代码和长链接。代码块通常还需要独立的横向滚动，而不是让整个页面溢出。

## 批量读写尺寸

循环中交替读取尺寸和修改样式，可能使浏览器反复完成布局。先收集读取结果，再统一更新；复杂动画应结合性能录制判断，而非仅凭代码形式推断流畅程度。

延伸阅读：[浏览器如何工作](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work)。
