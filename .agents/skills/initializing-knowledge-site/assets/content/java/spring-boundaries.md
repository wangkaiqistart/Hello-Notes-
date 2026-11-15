---
title: Spring 依赖注入与业务边界
description: 用构造器依赖明确协作关系，把业务规则与外部系统隔开。
sidebar:
  order: 3
---

## 让依赖显式出现

依赖注入让对象从外部获得协作者，而不是在内部查找或创建它们。构造器注入表达对象成立所需的依赖，也方便在测试中替换外部接口。

下面的纯 Java 示例展示相同原则；在 Spring 应用中可把实现交给容器管理，再注入应用服务。

```java
interface Inventory {
    boolean available(String sku);
}

final class CheckoutService {
    private final Inventory inventory;

    CheckoutService(Inventory inventory) {
        this.inventory = inventory;
    }

    boolean canCheckout(String sku) {
        return inventory.available(sku);
    }
}
```

## 检查代理边界

声明式事务等能力通常依赖 Spring 代理。对象内部直接调用自身方法不一定经过代理；分析行为需要核对代理模式、调用路径与实际版本，不能只看到注解就断言事务生效。

延伸阅读：[Spring 依赖注入](https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html)。
