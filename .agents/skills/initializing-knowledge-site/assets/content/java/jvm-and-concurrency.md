---
title: JVM 内存与线程协作的边界
description: 区分可见性、原子性与顺序约束，避免把 volatile 当作通用并发控制。
sidebar:
  order: 2
---

## 共享状态需要什么保证

多个线程访问同一个可变对象时，需要分别考虑可见性、原子性与顺序约束。JVM 内存布局和 Java 内存模型解决不同层面的问题：前者描述运行时区域，后者规定线程间的可观察行为。

## 为什么 volatile 不能保护递增

`volatile` 读写提供可见性与特定的顺序保证，但 `count++` 仍由读取、计算和写入组成。两个线程可能基于相同的旧值计算，导致更新丢失。

```java
import java.util.concurrent.atomic.AtomicInteger;

class Counter {
    private final AtomicInteger count = new AtomicInteger();

    int increment() {
        return count.incrementAndGet();
    }
}
```

## 选择同步边界

单一变量的独立原子操作可以采用原子类；维护多个字段的不变量时，通常需要围绕完整临界区设计锁或其他协调机制。线程安全集合不会自动让多个调用组成的业务流程成为原子操作。

延伸阅读：[Java 内存模型](https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html#jls-17.4)。
