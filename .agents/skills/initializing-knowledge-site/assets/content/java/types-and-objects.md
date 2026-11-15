---
title: Java 类型、引用与可变对象
description: 复制引用不会复制对象，final 也不保证对象内部状态不变。
sidebar:
  order: 1
---

## 复制的是什么

引用变量的赋值复制引用值，不复制被引用的对象。两个变量可以指向同一个可变对象，因此通过一个引用修改对象，另一个引用也能观察到变化。

```java
import java.util.ArrayList;
import java.util.List;

class ReferenceExample {
    public static void main(String[] args) {
        List<String> original = new ArrayList<>();
        List<String> alias = original;
        alias.add("Java");
        System.out.println(original.size()); // 1
    }
}
```

## final 的边界

`final` 修饰引用变量时，限制的是变量不能再赋给另一个引用值，不保证对象内部状态不变。表达不可变数据需要限制可变字段和修改入口，并避免泄露可变集合。

跨模块传递集合时应明确调用方是否可以修改它。`List.copyOf(source)` 可生成不可修改的列表，但不会深拷贝其中的可变元素。

延伸阅读：[Java 语言规范：类型与值](https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html)。
