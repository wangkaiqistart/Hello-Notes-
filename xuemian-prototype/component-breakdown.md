# 学面通原型页面结构与组件化拆分

## 1. 页面结构拆分

当前产品应按「全局布局 + 三个业务页面」拆，而不是把学习室、面试间、笔记本都塞进同一个通用聊天页面。

```text
App
├─ AppShell
│  ├─ AppHeader
│  │  ├─ BrandBlock
│  │  ├─ ModuleTabs
│  │  └─ TopActions
│  ├─ AppWorkspace
│  │  ├─ StudyPage
│  │  ├─ InterviewPage
│  │  └─ NotesPage
│  └─ AppToast
```

页面职责：

- 学习室：围绕「学习会话」展开，核心对象是学习主题、材料、问答消息、学习路径。
- 面试间：围绕「模拟面试记录」展开，核心对象是一场面试、当前问题、回答输入、评分、复盘。
- 笔记本：围绕「笔记库」展开，核心对象是笔记、来源、标签、编辑内容。

## 2. 组件化拆分

### 全局组件

```text
components/layout/
├─ AppHeader.vue
├─ ModuleTabs.vue
├─ AppWorkspace.vue
└─ AppToast.vue

components/common/
├─ IconButton.vue
├─ SearchField.vue
├─ HistoryCard.vue
├─ ActionButton.vue
├─ StatusBadge.vue
└─ ConfirmPopover.vue
```

全局组件说明：

- `AppHeader`：品牌、当前学习目标、模块导航、搜索/通知/用户入口。
- `ModuleTabs`：控制学习室、面试间、笔记本页面切换。
- `AppToast`：承接创建、删除、发送、保存等轻反馈。
- `HistoryCard`：可复用历史卡片，但通过 props 区分学习会话、面试记录、笔记。
- `ConfirmPopover`：删除会话/面试记录/笔记前的确认组件。

### 学习室组件

```text
pages/study/
├─ StudyPage.vue
├─ StudySessionRail.vue
├─ StudySessionCard.vue
├─ StudyWorkbench.vue
├─ LearningPath.vue
├─ ChatStream.vue
├─ ChatMessage.vue
└─ StudyComposer.vue
```

组件职责：

- `StudySessionRail`：学习会话列表、搜索、新建、筛选。
- `StudySessionCard`：会话标题、模式、时间、摘要、重命名、删除。
- `StudyWorkbench`：右侧学习内容容器。
- `LearningPath`：重点提炼、知识精讲、刷题巩固、笔记沉淀。
- `ChatStream`：AI 和用户消息流。
- `StudyComposer`：问题输入、上传材料、知识精讲、刷题模式、发送。

### 面试间组件

```text
pages/interview/
├─ InterviewPage.vue
├─ InterviewRecordRail.vue
├─ InterviewRecordCard.vue
├─ InterviewWorkbench.vue
├─ InterviewStage.vue
├─ InterviewAnswerBar.vue
├─ InterviewModeChips.vue
└─ InterviewScorePanel.vue
```

组件职责：

- `InterviewRecordRail`：面试记录列表、搜索、新建模拟面试、筛选。
- `InterviewRecordCard`：岗位/公司/题型、分数、复盘状态、重命名、删除。
- `InterviewStage`：当前面试问题、候选人/面试官状态、追问提示。
- `InterviewAnswerBar`：输入你的回答、附件、语音、发送。
- `InterviewModeChips`：简历优化、模拟面试、面试复盘、知识精讲。
- `InterviewScorePanel`：综合分、结构表达、项目深度、技术准确。

### 笔记本组件

```text
pages/notes/
├─ NotesPage.vue
├─ NoteLibraryRail.vue
├─ NoteFilterTabs.vue
├─ NoteCard.vue
├─ NoteEditor.vue
├─ NoteToolbar.vue
└─ NoteContentEditor.vue
```

组件职责：

- `NoteLibraryRail`：笔记库列表、搜索、新建笔记、更多操作。
- `NoteFilterTabs`：全部、学习生成、面试复盘等来源筛选。
- `NoteCard`：笔记标题、来源、时间、重命名、删除。
- `NoteEditor`：笔记标题、保存状态、编辑器容器。
- `NoteToolbar`：加粗、斜体、列表、引用、同步学习计划。
- `NoteContentEditor`：富文本编辑区域。

## 3. 数据对象拆分

### 学习会话

```ts
type StudySession = {
  id: string;
  title: string;
  mode: 'explain' | 'quiz' | 'material';
  summary: string;
  updatedAt: string;
  messages: ChatMessage[];
  learningStep: 'extract' | 'explain' | 'practice' | 'note';
};
```

### 面试记录

```ts
type InterviewRecord = {
  id: string;
  title: string;
  company?: string;
  position?: string;
  round: string;
  score: number;
  status: 'ongoing' | 'reviewed' | 'pendingReview';
  currentQuestion: string;
  answers: InterviewAnswer[];
  metrics: {
    structure: number;
    projectDepth: number;
    accuracy: number;
  };
};
```

### 笔记

```ts
type Note = {
  id: string;
  title: string;
  sourceType: 'study' | 'interview' | 'manual';
  sourceTitle?: string;
  tags: string[];
  updatedAt: string;
  content: string;
};
```

## 4. 路由结构建议

如果后续用 Vue Router，建议这样拆：

```text
/
├─ /study
├─ /study/:sessionId
├─ /interview
├─ /interview/:recordId
├─ /notes
└─ /notes/:noteId
```

路由设计原则：

- 顶部模块切换只改变一级页面。
- 左侧列表选择改变当前资源 ID。
- 学习室、面试间、笔记本不要共用同一个历史列表。
- 跨模块关联通过 `sourceType`、`sourceId` 表达，不通过混合列表表达。

## 5. 交互逻辑清单

### 全局

- 切换顶部模块：显示对应页面，更新 tab 选中态。
- 搜索按钮：打开全局搜索面板，支持搜索会话、面试记录、笔记。
- 通知按钮：打开通知列表。
- Toast：所有轻量操作统一通过 toast 反馈。

### 左侧列表通用交互

- 点击卡片：选中当前记录，并更新右侧内容区。
- 重命名：标题进入编辑态，Enter 保存，Escape 取消。
- 删除：弹出确认，确认后删除；如果删除的是当前选中项，自动选中下一条。
- 新建：创建对应模块的空白对象。
- 搜索：按标题、摘要、来源、标签过滤当前模块列表。

### 学习室

- 新建学习会话：生成空白会话，默认进入问答输入状态。
- 上传文件：打开文件选择，解析完成后生成重点提炼。
- 知识精讲：切换当前会话模式，AI 回复结构化讲解。
- 刷题模式：生成题目列表，记录答题结果。
- 发送问题：校验非空，追加用户消息，触发 AI 回复占位。
- 学习路径切换：更新当前学习步骤，不影响左侧会话列表。

### 面试间

- 新建模拟面试：创建一条面试记录，状态为进行中。
- 选择面试记录：加载当前问题、回答历史、评分面板。
- 简历优化：切换到简历建议模式。
- 模拟面试：切换到问答追问模式。
- 面试复盘：显示复盘报告和改进建议。
- 知识精讲：将面试暴露出的知识弱点跳转到学习讲解上下文。
- 输入回答：校验非空，提交后更新当前问题状态。
- 语音输入：进入录音状态，再转成文本填入回答框。
- 上传附件：关联简历、JD 或面试材料。
- 生成复盘：根据回答历史生成分数、亮点、问题和学习建议。

### 笔记本

- 新建笔记：创建空白笔记并进入编辑态。
- 笔记筛选：按全部、学习生成、面试复盘过滤。
- 选择笔记：右侧编辑器加载标题和内容。
- 编辑标题：失焦或 Enter 保存。
- 编辑正文：触发保存状态从已保存变为编辑中，再自动保存。
- 富文本按钮：加粗、斜体、列表、引用作用于当前选区。
- 同步学习计划：将笔记中的行动项写入学习计划。
- 删除笔记：确认后删除，右侧切换到下一篇或空状态。

## 6. Mock 数据建议

```text
src/mock/
├─ studySessions.ts
├─ interviewRecords.ts
├─ notes.ts
└─ index.ts
```

Mock 数据至少覆盖：

- 学习室：3 条学习会话，每条 2-4 条消息。
- 面试间：2 条面试记录，一条已复盘，一条待复盘。
- 笔记本：3 条笔记，覆盖学习生成、错题归档、面试复盘。
- 空状态：无搜索结果、无笔记、无面试记录。

## 7. 优先实现顺序

1. 全局布局和模块路由。
2. 三个页面的左侧列表占位。
3. 三个页面的右侧主内容占位。
4. Mock 数据渲染。
5. 列表选择、重命名、删除。
6. 学习室发送问题。
7. 面试间回答输入。
8. 笔记本编辑保存。
9. 搜索、筛选、空状态。
10. 文件上传、语音输入、AI 回复接入。
