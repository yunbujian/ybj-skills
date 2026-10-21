# ybj-skills · 云不见技能合集

用于课程检索、写作修改、学习陪练、语言复盘、公众号排版和 YouTube 中文策展。

本仓库包含 **11 个可安装 Skill**：6 个课程技能，以及费曼学习陪练、写作反差、语言转化、公众号 HTML 排版和 YouTube 策展。

课程技能仅提供规则、课程标题和章节索引，**不包含课程全文**。使用课程技能需要联网读取原文；安装不授予课程网站访问权限。其他技能的依赖见下方说明。

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

| Skill | 作用 | 课程入口或输入 |
|---|---|---|
| `ybj-contrast` | 保留作者口吻，优化开头、结尾和指定段落的反差与衔接 | 用户提供的文稿 |
| `ybj-language-shift` | 从日记、口喷中区分情绪与限制性判决，找到资源和下一步 | 用户提供的文字 |
| `ybj-wechat-html` | Markdown 转公众号 HTML，含云不见风格及其他 15 种风格，支持图片 | Markdown 与可选图片 |
| `ybj-youtube-trans` | YouTube 中文策展、说话人翻译、原文金句核验和人物研究 | 视频链接、文稿或音频 |
| `ybj-feiman` | 你来教 AI，通过逐轮追问、复述和新例子发现理解漏洞 | 无需课程网站 |
| `ybj-library` | 跨课程定位方法，按需查找内容库文章；可以单独安装 | [课程总览](PAID_COURSE_URL_REMOVED) · [内容库](PAID_COURSE_URL_REMOVED) |
| `ybj-readaloud` | 朗读实践、自由输入与读后思考 | [朗读实践小组](PAID_COURSE_URL_REMOVED) |
| `ybj-speaktowrite` | 口喷写作、表达和自我研究 | [33 天口喷写作](PAID_COURSE_URL_REMOVED) |
| `ybj-tenweeks` | 持续写作、每周产出、编辑与反馈 | [十周写作实践](PAID_COURSE_URL_REMOVED) |
| `ybj-wtl` | 用写作学习陌生领域，保留启动、深化、发表陪练 | [写作高效学习任何领域](PAID_COURSE_URL_REMOVED) |
| `ybj-ebb` | 产品验证、内容更新与一人商业 | [极简一人商业](PAID_COURSE_URL_REMOVED) |

课程技能默认回答：**是否相关 → 具体课名与链接 → 适用条件 → 一个行动**。课程原意与 AI 应用建议会分开说明。只有你需要实践时，才进入陪练。

## 新增技能使用示例

```text
$ybj-contrast 保留我的口吻，帮我改这篇文章的开头：……
$ybj-language-shift 帮我分析这段口喷中的限制性语言：……
$ybj-wechat-html 把这份 Markdown 排成云不见风格的公众号 HTML。
$ybj-youtube-trans 策展这个 YouTube 视频：https://www.youtube.com/watch?v=视频ID
```

## 工具与环境

- 反差写作、语言转化、费曼陪练：无需额外脚本依赖。
- 公众号排版：随包提供 `templates/styles.md`，需要 AI 工具能够保存 HTML 文件；不自动上传或发布到公众号。
- YouTube 策展：需要网页读取和文件保存能力；随包脚本需要 Python 3.10+。获取视频元数据与字幕还需要在同一 Python 环境安装 `yt-dlp`（`python3 -m pip install yt-dlp`）。音频转写需另备转写工具，本包不自带模型。字幕获取可能受视频可用性和网络条件影响。
- YouTube 策展优先使用用户指定的保存目录；未指定时保存到当前工作目录的 `策展内容库/<中文标题>/`。仅有链接时，全文翻译和引文范围遵守宿主工具的规则。

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

本合集整合 [ybj-course-skills](https://github.com/yunbujian/ybj-course-skills) 与 [ybj-feiman](https://github.com/yunbujian/ybj-feiman)，并收录云不见的写作、语言复盘、排版与策展技能。YouTube 策展的发布版使用通用输出目录。
