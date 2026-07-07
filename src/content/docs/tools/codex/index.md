---
title: Codex 从 0 到 1 全攻略
description: OpenAI Codex 完整使用指南
---

## 下载安装

下载地址：https://openai.com/codex/for-work/

## 实现一个笔记软件
![笔记软件](https://my-website1.oss-cn-chengdu.aliyuncs.com/%E6%88%AA%E5%B1%8F2026-06-23%2023.21.26.png)

![笔记软件](https://my-website1.oss-cn-chengdu.aliyuncs.com/%E6%88%AA%E5%B1%8F2026-06-23%2023.28.09.png)

![批准操作](https://my-website1.oss-cn-chengdu.aliyuncs.com/%E6%88%AA%E5%B1%8F2026-06-23%2023.30.16.png)

请求审批： 操作沙箱以外的操作始终需要审批，很安全。

替我审批：引入了一个专门负责安全审查的 agent ，当 Codex 准备执行操作的时候，这个 agent 会首先提你把关，安全的直接放行，危险的直接拦截，拿不定主意的时候，才会弹窗让你来做决定。

完全访问权限：没有任何的安全校验。


思考深度越高，花费时间越多， 消耗的 token 也越多，但代码质量也会更好一些。

![](https://my-website1.oss-cn-chengdu.aliyuncs.com/%E6%88%AA%E5%B1%8F2026-06-23%2023.36.26.png)


如果返回了某次操作，可以直接修改上一个消息。Codex 只支持修改最后一条消息，至于更靠前的那些消息，不支持编辑。

如果要编辑更靠前的消息，可以考虑使用 fork 功能来间接时间。

![](https://my-website1.oss-cn-chengdu.aliyuncs.com/%E6%88%AA%E5%B1%8F2026-06-23%2023.45.03.png)

可以对预览的网站和 代码添加注释，直接让 codex 专注于修改这一块。



fork 的作用是基于当前回话，再复制一个新的会话出来，这个新会话就只到 目前所选的消息为止，后面的消息全部不保留。

有两个选项， 一个是 fork into local ，另一个是 fork into new worktree ，这两者最大的区别在于新会话的代码存放地址不同。

第一个选项会使用当前目录作为新会话代码存放地址（只会处理会话，不会对代码做任何修改，只能使用 git 来回滚代码），第二个选项会创建一个新的目录来存放新的代码，非常适合在两个会话分别处理两个不同的功能点。


fork into new worktree 同样不会回滚代码，它只是把当前项目目录里面的所有代码，复制到一个新的目录里面，仅此而已。

两者唯一的区别就是代码的位置，local 是继续沿用原来的目录，new work tree 是开启一个新的目录


## AGENT.md
