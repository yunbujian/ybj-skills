# ybj-skills · 云不见技能合集

带着问题使用课程：定位哪一课讲过类似问题，联网读取原文，判断方法是否适合你的情况，再给出一个具体行动。不必从第一课重新学习。

本仓库包含 **7 个可安装 skill**（6 个课程技能 + 1 个费曼学习陪练），仅公开技能规则、课程标题和章节索引。**不包含课程全文。** 使用时需要 AI 工具具备联网读取网页的能力；安装并不授予课程网站的访问权限。

费曼学习陪练让你教 AI 一个概念，AI 通过每轮一个问题、复述和新例子，帮助发现解释中缺少的连接。它可以独立使用，无需访问课程网站。

## 安装

需要 Node.js 和 npm（提供 `npx`）。安装到当前项目的 Codex：

```bash
npx -y skills add yunbujian/ybj-skills --skill '*' --agent codex -y
```

全局安装到支持的 AI 工具：

```bash
npx -y skills add yunbujian/ybj-skills -g --all
```

[一次下载全部技能 ZIP](https://github.com/yunbujian/ybj-skills/archive/refs/heads/main.zip)。

只安装统一检索入口：

```bash
npx -y skills add yunbujian/ybj-skills -g --skill ybj-library
```

已有同名 skill 时，先检查本机是否有自定义内容，避免安装覆盖你的修改。

## 使用

在 Codex 中输入：

```text
$ybj-library 我每天写作都像重新开始。课程里讲过类似问题吗？有什么方法适合我？
```

也可以直接指定一门课：

```text
$ybj-speaktowrite 我一开口就想修改，课程里怎么处理这个问题？
```

费曼学习陪练示例：

```text
$ybj-feiman 今天我想教你什么是复利。请先听我解释，再从没听明白的地方问起。
```

其他 AI 工具可直接说“使用 ybj-library”，或使用该工具支持的 skill 调用方式。

| Skill | 作用 | 课程入口 |
|---|---|---|
| `ybj-feiman` | 你来教 AI，通过逐轮追问、复述和新例子发现理解漏洞 | 无需课程网站 |
| `ybj-library` | 跨课程定位方法，按需查找内容库文章；可以单独安装 | [课程总览](PAID_COURSE_URL_REMOVED) · [内容库](PAID_COURSE_URL_REMOVED) |
| `ybj-readaloud` | 朗读实践、自由输入与读后思考 | [朗读实践小组](PAID_COURSE_URL_REMOVED) |
| `ybj-speaktowrite` | 口喷写作、表达和自我研究 | [33 天口喷写作](PAID_COURSE_URL_REMOVED) |
| `ybj-tenweeks` | 持续写作、每周产出、编辑与反馈 | [十周写作实践](PAID_COURSE_URL_REMOVED) |
| `ybj-wtl` | 用写作学习陌生领域，保留启动、深化、发表陪练 | [写作高效学习任何领域](PAID_COURSE_URL_REMOVED) |
| `ybj-ebb` | 产品验证、内容更新与一人商业 | [极简一人商业](PAID_COURSE_URL_REMOVED) |

默认回答：**是否相关 → 具体课名与链接 → 适用条件 → 一个行动**。课程原意与 AI 应用建议会分开说明。只有你需要实践时，才进入陪练。

## 索引范围

索引日期：2026-09-19，共 156 个课程/材料入口：

- 朗读：37 个页面区块，含流程、答疑、复盘与附件目录；不含附件正文。
- 口喷：欢迎页与 Day 1–33，共 34 页。
- 十周：第 1–20 课；未将后五周规划作为已发布课文。
- WTL：网站第 1–10 课。skill 中的七天陪练安排不是网站课号。
- EBB：48 课与 7 项补充材料入口。
- Notion 内容库：尚未建立文章索引，按需访问，不承诺全文检索覆盖。

网页可能更新；这些是目录线索，不是正文证据。无法联网或访问课程时，skill 会说明原文未核实，并请你提供相关段落。不会假装已经读过。

统一入口自带合并索引，不依赖其他 skill 的安装位置。可选关键词搜索脚本只需 Python 3 标准库，不联网、不写文件；没有 Python 时 AI 可以直接读取 JSON 索引。

## 验证与内容边界

发布前检查技能结构、引用和本机路径，测试索引搜索的命中、空输入与无结果情况。完整问答行为与不同 AI 客户端的效果尚未完成独立评测。

本仓库不包含课程正文、书籍附件、个人笔记、测试答案或登录凭据。课程及其引用作品的权利归各自权利人；本仓库不改变原站访问规则或授予课程内容的再分发权。

## 来源

本合集整合 [ybj-course-skills](https://github.com/yunbujian/ybj-course-skills) 与 [ybj-feiman](https://github.com/yunbujian/ybj-feiman)，保留各技能名称和文件内容。
