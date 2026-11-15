---
title: 组件状态与单向数据流
description: 区分源状态、派生值和副作用，让组件行为可以解释。
sidebar:
  order: 3
---

## 先确定状态的所有者

同一份业务事实需要清晰的维护入口。多个组件共享数据时，可以把状态提升到共同所有者，通过参数和事件协调，避免多个副本互相同步。

```typescript
const items = [
  { title: '类型边界', published: true },
  { title: '状态设计', published: false },
];
const publishedItems = items.filter((item) => item.published);
const publishedCount = publishedItems.length;
```

已发布列表和数量可以从原列表推导。额外存成可变状态会增加维护不一致的机会。

## 副作用需要生命周期

订阅事件、启动动画或创建 WebGL 资源时，要明确何时开始、何时停止、如何释放。列表中的稳定标识也会影响组件实例能否正确复用。

框架特有的状态机制应核对具体版本；通用原则不能替代对框架行为的验证。

延伸阅读：[React：选择状态结构](https://react.dev/learn/choosing-the-state-structure)。
