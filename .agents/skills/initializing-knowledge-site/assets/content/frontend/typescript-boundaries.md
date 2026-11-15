---
title: TypeScript 类型与运行时输入
description: 类型断言不会验证接口响应，外部输入仍需要运行时检查。
sidebar:
  order: 2
---

## 类型系统看不到所有事实

TypeScript 类型在编译后会被擦除。把 JSON 断言为接口不会检查字段是否存在或值是否符合预期。网络响应、本地存储和用户输入都属于需要校验的边界。

```typescript
type User = { id: string; name: string };

function isUser(value: unknown): value is User {
  if (typeof value !== 'object' || value === null) return false;
  return (
    'id' in value &&
    typeof value.id === 'string' &&
    'name' in value &&
    typeof value.name === 'string'
  );
}
```

## 把断言当作责任声明

`unknown` 要求使用前先收窄类型。复杂输入可以通过运行时 schema 验证，把错误收敛在边界。`as User` 不改变对象，不补充字段，也不把错误输入变成合法数据。

延伸阅读：[TypeScript 类型收窄](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)。
