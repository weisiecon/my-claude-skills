# Claude Code Skills 评估报告

- 日期：2026-10-24
- 范围：`~/.claude/skills/`（GitHub 仓库 `Sophieariel/my-claude-skills`）
- Windows 路径：`\\wsl.localhost\Ubuntu\home\weisi\.claude\skills\SKILLS_REVIEW.md`

## 1. 数据来源与局限

| 数据 | 来源 | 覆盖范围 |
|---|---|---|
| skill 调用记录 | `~/.claude/skill-usage.log`（settings.json 中的钩子在 Claude 每次调用 skill 时写入一行） | 2026-03-26 至 2026-10-24，共 288 次调用 |
| 输入记录 | `~/.claude/history.jsonl` | 2026-03-06 至 2026-10-24，共 6,086 条输入 |
| 会话记录 | `~/.claude/projects/` | 只保留最近 30 天 |

局限：

1. **只覆盖本机（WSL）。** PowerShell 那台电脑的使用情况没有记录。如果你在那台电脑上常用某个 skill，结论需要相应调整。
2. **手动调用不进日志。** 钩子只记录 Claude 自动调用的 skill，你输入 `/skill名` 时不会写入。不过输入记录显示，7 个月里你手动调用 skill 只有 5 次（`/context-status` 2 次、`/docx` 2 次、`/project-deck` 1 次），影响很小。
3. **"没用过"不等于"没用"。** 有些 skill 适用于低频但重要的场合，例如准备 replication package。下面的判断同时考虑四个因素：使用频率、与你工作的匹配程度、运行环境是否具备、与其他 skill 是否重复。

## 2. 主要发现

1. **使用高度集中。** 调用次数最多的 9 个 skill（docx、stata、pptx、split-pdf、latex-autofix、xlsx、proofread、avoid-ai-writing、pdf）占全部 288 次调用的 71%。
2. **一大半 skill 从未被调用。** 当前启用的 65 个 skill 中，40 个在 7 个月里一次也没有被调用。
3. **你最常用的是量身定制的 skill。** 项目文件夹中自建的 skill 比网上收集的通用 skill 用得更多：ECON1102 的 update-slides（9 次）和 generate-slides（5 次），Referees 文件夹的 reviewing-economics-articles（7 次）。
4. **很多 skill 来自别人的工作环境。** 约一半 skill 来自同一套模板。原作者使用 macOS、Notion、Zotero 或 Paperpile、Dropbox 里的 Overleaf 同步文件夹，以及一个 `.context/` 上下文库。你的电脑上没有 Notion 连接器，也没有 `.context/` 文件夹，这些 skill 无法按设计运行。
5. **skill 过多已经产生副作用。** 本次会话中，superpowers 和 claude-mem 插件里有 9 个 skill 只显示名称、不显示描述，而它们的 SKILL.md 文件里其实写了描述。官方文档证实了原因：skill 列表的篇幅上限是模型上下文窗口的 1%，超出时 Claude Code 会从最少使用的 skill 开始省略描述（https://code.claude.com/docs/en/skills ，"Skill descriptions are cut short" 一节）。描述缺失时，Claude 很难判断什么时候该用这些 skill。归档前，你的 64 个可见 skill 的描述合计约 18,500 个字符，其中 xlsx、docx、skill-deslop、pptx 四个就占了约 3,150 个字符。
6. **同名时，个人目录的 skill 优先于项目目录。** 官方文档原文是 "personal over project"（同一页 "Resolve skills that share a name" 一节）。因此你在 ECON1102 里定制的 pptx 和 theme-factory 一直被全局同名 skill 盖住，没有生效。全局 theme-factory 已归档，ECON1102 的版本现在会生效；pptx 的冲突仍在，见 5.4。
7. **Claude Code 自带的命令也被盖住过。** 你原来的 code-review（审查 R 和 Python 脚本）与 Claude Code 自带的 `/code-review` 同名。归档后，自带的代码审查命令重新出现在列表里。

## 3. 本次已完成的修复

这些修复不改变"哪些 skill 处于启用状态"，只清理重复和失效的部分。

| 问题 | 处理 |
|---|---|
| 8 个 skill 放在分类子文件夹里（analysis/、communication/ 等），从未被加载 | 评估后均不建议启用，移入 `_archive/`（理由见 `_archive/README.md`） |
| 5 个子文件夹中的 skill 与顶层副本逐字节相同 | 删除子文件夹中的副本 |
| init-project-course、init-project-light 的文件名是小写 `skill.md`，在 Linux 上不被识别 | 改名为 `SKILL.md` 后移入 `_archive/`（两者都依赖 Notion） |
| `skills/skills` 是指向自身的循环链接 | 删除（只存在于本机，未同步到 GitHub） |
| diagram-design 与 diagram-design-real 内容完全相同 | 删除本机链接 `diagram-design`，把 `diagram-design-real` 改名为 `diagram-design` |
| bib-validate 与 validate-bib 描述相同 | 保留较新的 bib-validate（另有 10 个 skill 引用它），validate-bib 移入 `_archive/` |
| 你的 brainstorming 是 superpowers 插件中同名 skill 的旧版副本 | 移入 `_archive/`，插件里的新版本仍可使用 |
| 空的分类文件夹 | 删除 |

**注意：** PowerShell 那台电脑上的 Windows 文件系统不区分大小写，init-project-course 和 init-project-light 在那边可能原本是能用的。拉取更新后，它们在两台电脑上都会停用。

### 3.2 经你确认后完成的改动

| 改动 | 说明 |
|---|---|
| 归档 41 个 skill | 4.3 的 2 个、4.4 的 35 个、4.5 的 4 个，清单见 `_archive/README.md` |
| 改造 session-recap | 只做三件事：更新 `project_memory.md`、写 `log/` 下的 session log、询问后再 git 提交。不再启动子代理，不再写 `.context/` 或 Notion。原版备份在 `_archive/session-recap-original/` |
| 修改规则文件 | `latex-conventions.md` 中的 `/validate-bib` 改为 `/bib-validate` |
| 清理失效引用 | 保留的 9 个 skill 文件中，22 处指向已归档 skill 的引用被删除或改写。其中两处影响较大：beamer-deck 的描述原本让 Claude 去用 `/quarto-deck`；literature 原本把 `/session-log` 列为必须执行的第一步 |
| interview-me 的模板 | 它用到的 field-calibration 模板原本在已归档的 init-project-research 里，已复制到 `interview-me/references/` |

## 4. 逐项评估

### 4.1 核心保留（16 个）

| skill | 7 个月调用次数 | 说明 |
|---|---:|---|
| docx | 60 | Word 文档，你最常用的 skill |
| stata | 31 | 记录了本机 Stata 16 的路径和 do-file 约定，路径已核实有效 |
| pptx | 22 | PowerPoint |
| split-pdf | 22 | 分块精读论文 PDF |
| latex-autofix | 21 | LaTeX 编译与自动排错，你的规则文件推荐它 |
| xlsx | 14 | Excel |
| proofread | 14 | LaTeX 论文校对，你的规则文件引用了它的评分标准 |
| avoid-ai-writing | 12 | 去除 AI 写作痕迹 |
| pdf | 9 | PDF 处理 |
| devils-advocate | 7 | 对论证做压力测试，你的规则文件推荐它 |
| bib-validate | 6 | 核对引用（含已合并的 validate-bib 的 5 次） |
| session-recap | 6 | 会话收尾流程，建议改造（见 5.1） |
| respond-to-referees | 5 | 撰写审稿回复信 |
| pre-submission-report | 3 | 投稿前的综合检查，你的规则文件推荐它 |
| process-reviews | 2 | 整理审稿意见 |
| latex | 1 | 直接调用很少，但 latex-autofix、bib-validate、beamer-deck 都引用了它的编译约定 |

### 4.2 保留：低频但对口（8 个）

| skill | 调用次数 | 保留理由 |
|---|---:|---|
| diagram-design | 2 | 流程图、时间线等示意图 |
| beamer-deck | 1 | 学术报告用的 Beamer 幻灯片 |
| research-ideation | 1 | 面向经济学的选题 |
| python-env | 1 | 规定用 uv 管理 Python（本机已安装 uv）；docx、pdf 等 skill 运行 Python 脚本时会用到 |
| literature | 0 | 唯一面向经济学的文献 skill（覆盖 SSRN、NBER、OpenAlex、Crossref）；bib-validate、latex-autofix、beamer-deck 都会引用它 |
| pipeline-manifest | 0 | 梳理 do-file 与论文图表的对应关系，支持 Stata；论文接收后准备 replication package 时有用 |
| skill-creator | 0 | 你已经自建了十几个项目 skill，以后再建时可以用 |
| interview-me | 0 | 只能手动调用（`/interview-me`），不占用 skill 列表的篇幅 |

### 4.3 需要你决定（2 个）

| skill | 调用次数 | 情况 | 我的建议 |
|---|---:|---|---|
| peer-review | 2 | 偏生物医学，内置 CONSORT 等医学报告规范。你在 Dropbox/Referees 里已有专门的 reviewing-economics-articles（7 次） | 归档 |
| skill-deslop | 3 | 与 avoid-ai-writing（12 次）功能相同，描述长达 732 个字符 | 归档，保留 avoid-ai-writing |

### 4.4 建议归档（35 个）

**(a) 依赖你电脑上没有的环境（11 个）**

| skill | 调用次数 | 原因 |
|---|---:|---|
| save-context | 0 | 写入 `.context/` 上下文库，你的电脑上没有 |
| context-status | 1 | 读取 Notion 和 `.context/`；内置的 `/context` 命令可以直接查看上下文用量 |
| task-management | 1 | 依赖 Notion 和 `.context/` |
| init-project | 0 | 会把新项目登记到你没有的 `.context/` 上下文库，目录结构按原作者的习惯设计。需要的话，可以按你现有项目的结构另写一个 |
| init-project-research | 0 | 依赖 Notion、`.context/`、macOS 路径和上述 Overleaf 链接方式 |
| system-audit | 0 | 检查的是原作者的 Notion、Overleaf、Task Management 目录 |
| latex-health-check | 0 | 面向原作者的多项目 Overleaf 目录（macOS 路径） |
| notebooklm | 0 | 装好了运行环境（`.venv/`），但从未完成 Google 登录（登录信息应保存在 `data/`，该目录不存在） |
| quarto-deck | 0 | 本机未安装 Quarto |
| r-econometrics | 0 | 本机未安装 R |
| code-review | 0 | 只支持 R 和 Python，你主要写 Stata |

**(b) 面向其他学科或其他用途（12 个）**

| skill | 调用次数 | 原因 |
|---|---:|---|
| scientific-writing | 0 | IMRAD 结构，CONSORT、STROBE 等医学报告规范 |
| literature-review | 0 | PubMed、bioRxiv 等医学数据库 |
| citation-management | 1 | Google Scholar 加 PubMed；literature 已经覆盖用 DOI 生成 BibTeX |
| scientific-critical-thinking | 0 | GRADE、Cochrane 偏倚评估等医学证据框架，与 devils-advocate 重叠 |
| hypothesis-generation | 0 | 自然科学的实验设计，与 research-ideation 重叠 |
| venue-templates | 0 | Nature、IEEE、NeurIPS、NIH 等模板，不含经济学期刊 |
| latex-posters | 0 | 学术海报，经济学很少用 |
| scientific-slides | 0 | 用 AI 生成整页图片式幻灯片，不适合需要反复修改的课件 |
| copy-editing | 0 | 营销文案编辑 |
| frontend-design | 0 | 网页界面设计 |
| frontend-slides | 0 | 网页动画幻灯片，你用 PowerPoint 和 Beamer |
| python-panel-data | 0 | Python 面板数据分析，你用 Stata |

**(c) 内容过于通用，或与其他 skill 重复（7 个）**

| skill | 调用次数 | 原因 |
|---|---:|---|
| stata-data-cleaning | 0 | 7 个月里 Stata 任务都触发了 stata，这个从未被触发；内容是通用建议 |
| latex-tables | 0 | 通用的 booktabs 建议；你的表格由 Stata 的 esttab 生成 |
| multi-perspective | 0 | 与 devils-advocate 重叠，而且会同时启动多个子代理，比较耗费额度 |
| project-deck | 0 | 向导师或合作者汇报项目进展的幻灯片，与 beamer-deck 重叠 |
| theme-factory | 0 | 全局版本从未使用；ECON1102 文件夹里有你定制过的版本 |
| code-archaeology | 0 | 用于重新理解搁置已久或从别人那里接手的代码；你的两个 R&R 项目一直在推进，代码是熟悉的 |
| project-safety | 0 | 一次性的设置工具，从未使用 |

**(d) 管理 Claude 本身的工具，从未使用（5 个）**

learn、lessons-learned、creation-guard、consolidate-memory、insights-deck。这些工具服务于原作者那套复杂的配置体系。

其中 consolidate-memory 值得多说一句：你的 ECON1102（76 行）和 Higher Education & Fertility（75 行）两个项目的记忆索引 MEMORY.md 已经不短了。不过这个 skill 要到 100 条以上才建议整理，而且是按原作者的两层记忆结构（另有 `.claude/state/personal-memory.md`）写的。以后需要整理时，直接让 Claude "整理这个项目的记忆" 即可，不需要这个 skill。

### 4.5 与 session-recap 改造一起处理（4 个）

update-focus、sync-notion、session-log、update-project-doc。session-recap 在收尾时会调用这 4 个 skill。其中 update-focus 和 sync-notion 依赖你没有的 `.context/` 和 Notion。如果先归档它们而不改 session-recap，收尾流程可能出错，所以建议和 5.1 一起处理。

## 5. 建议的后续改进

### 5.1 改造 session-recap（已完成）

改造前，它会在收尾时启动最多 5 个并行子代理，分别更新 `.context/current-focus.md`、同步 Notion、写 session log 等。其中大部分步骤在你的电脑上无效。昨晚它在 Higher Education & Fertility 项目里写的 session log 质量不错，说明写 log 这一步是有用的。

现在只做你实际需要的三件事：

1. 按你在 CLAUDE.md 中的约定更新 `project_memory.md`：已完成的工作、关键决定、下一步；
2. 在 `log/` 下写一份 session log；
3. 检查 git 状态，询问后再提交。

4.5 中的 4 个配套 skill 已一并归档。

### 5.2 更新规则文件中的引用（已完成）

`/mnt/d/Dropbox/claude-config/rules/latex-conventions.md` 原来写的是 `/validate-bib`，已改为 `/bib-validate`。

### 5.3 可选：插件与 agents

- **superpowers 插件**的 14 个 skill 主要面向软件开发（测试驱动开发、git worktree、代码审查等）。它每次会话开始时都会注入一段很长的指令，要求 Claude 只要有 1% 的可能就调用 skill。7 个月里日志记录到它的 skill 被调用 7 次，另有 1 次是你手动输入的。是否保留由你决定，可以用 `/plugin` 管理。
- **11 个 "Academic ..." agents**（翻译、润色、审稿模拟等）最近 30 天都没有被调用过，而且大多是为计算机会议论文（NeurIPS、ICLR）设计的。如果要用于经济学论文，需要先改写。

### 5.4 ECON1102 的 pptx 被全局 pptx 盖住（待你决定）

ECON1102 的 `.claude/skills/pptx/` 是你定制的版本（基于 python-pptx），全局 `pptx` 是 Anthropic 官方版本（7 个月调用 22 次）。两者同名，按官方规则，在 ECON1102 里实际用的是全局版本。解决办法是把 ECON1102 里的版本改一个名字（例如 `econ1102-pptx`），两个版本就能同时可用。这需要修改 ECON1102 文件夹，所以留给你决定。

### 5.5 项目记忆文件过大（待你决定）

| 项目 | project_memory.md 行数 | 大小 |
|---|---:|---:|
| Higher Education & Fertility | 3,230 | 1.36 MB |
| Diverse Expertise | 5,053 | 0.88 MB |
| Gender Experiment | 850 | 0.23 MB |
| Referees | 264 | 0.06 MB |
| ECON1102 | 130 | 0.01 MB |

按你的约定，每次会话开始都要读这个文件。前两个文件太大，无法一次读完，每次也会占用大量上下文。建议把较早的条目移到 `project_memory_archive.md`，只在主文件里保留当前状态、未完成事项和最近几次会话的记录。新版 session-recap 在文件超过 500 行时会提醒你，但不会自己移动内容。

## 6. 汇总

| 类别 | 数量 |
|---|---:|
| 核心保留 | 16 |
| 低频但对口，保留 | 8 |
| 需要你决定 | 2 |
| 建议归档 | 35 |
| 与 session-recap 改造一起处理 | 4 |
| **当前启用合计** | **65** |

经你确认，以上建议已全部执行：启用的 skill 从 68 个（结构修复前）降到 24 个。

现在启用的 24 个：avoid-ai-writing, beamer-deck, bib-validate, devils-advocate, diagram-design, docx, interview-me, latex, latex-autofix, literature, pdf, pipeline-manifest, pptx, pre-submission-report, process-reviews, proofread, python-env, research-ideation, respond-to-referees, session-recap, skill-creator, split-pdf, stata, xlsx。
