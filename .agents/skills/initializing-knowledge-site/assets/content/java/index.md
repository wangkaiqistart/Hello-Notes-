---
title: Java 工程路线
description: 按语言基础、JVM 与并发、Spring 工程三条线学习 Java。
sidebar:
  order: 0
---

## 从语言到运行时，再到应用

语言规则决定程序怎样表达，JVM 决定代码怎样执行，框架把这些能力组织成可交付的应用。遇到框架问题时回到语言与运行时，通常比只记注解更有效。

1. [类型与对象](/java/types-and-objects/)：理解引用、可变性和边界。
2. [JVM 与线程协作](/java/jvm-and-concurrency/)：区分可见性与原子性。
3. [Spring 依赖注入](/java/spring-boundaries/)：明确对象的协作关系。

## 怎样记录工程经验

每篇笔记先记录具体问题，用最小示例验证结论，再写下适用边界。性能、并发和框架行为应注明 JDK/框架版本与复现方式，不能用单次测试代替普遍结论。
