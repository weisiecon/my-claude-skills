# 已归档的 skills

这个文件夹里的 skill **不会被 Claude Code 加载**：Claude Code 只读取 `~/.claude/skills/<名称>/SKILL.md` 这一层，`_archive/` 下面的内容会被忽略。

之所以归档而不是删除，有两个原因：一是可以随时恢复；二是这个文件夹仍在 git 仓库里，会通过 GitHub 同步到两台电脑。

## 如何恢复某个 skill

在 WSL 终端运行（以 `stata-regression` 为例）：

```bash
cd ~/.claude/skills && git mv _archive/stata-regression stata-regression
```

然后重新启动 Claude Code。

## 归档清单

### 2026-10-24：结构清理（这些 skill 归档前本来就没有被加载，归档不改变任何行为）

| skill | 原位置 | 归档原因 |
|---|---|---|
| stata-regression | analysis/ | 通用回归流程；你的 `stata` skill 和 stata-conventions 规则已覆盖实际需要的约定 |
| beamer-presentation | communication/ | 与 `beamer-deck` 重复 |
| econ-visualization | communication/ | 基于 ggplot2 / matplotlib，而你主要用 Stata 作图 |
| api-data-fetcher | data/ | 用 Python 抓取 FRED、World Bank 等宏观数据，与你的研究方向关联较弱 |
| lit-review-assistant | literature/ | 与 `literature` 重复 |
| general-equilibrium-model-builder | theory/ | 用 Julia 求解瓦尔拉斯一般均衡模型，不属于你的研究领域 |
| latex-econ-model | theory/ | 通用 LaTeX 公式排版，不需要 skill 也能完成 |
| academic-paper-writer | writing/ | 通用论文写作模板；你的研究项目里已有 `writing-economic-analysis` |
| init-project-course | 顶层 | 文件名原为小写 `skill.md`，在 WSL 上从未被加载；依赖 Notion。已改名为 `SKILL.md`，恢复后即可使用 |
| init-project-light | 顶层 | 同上；依赖 Notion 和 Overleaf |

### 2026-10-24：合并重复项

| skill | 归档原因 |
|---|---|
| validate-bib | `bib-validate` 的旧版本（默认文件名为 paperpile.bib）。保留 `bib-validate`，其他 10 个 skill 引用的也是它 |
| brainstorming | superpowers 插件中 `brainstorming` 的旧版副本，描述完全相同；插件里的新版本仍可使用 |

### 2026-10-24：按评估报告归档（经你确认，共 41 个）

各 skill 的归档理由见仓库根目录的 `SKILLS_REVIEW.md` 第 4 节。

| 类别 | skill |
|---|---|
| 依赖本机没有的环境（Notion、`.context/` 上下文库、R、Quarto、NotebookLM 登录） | save-context, context-status, task-management, init-project, init-project-research, system-audit, latex-health-check, notebooklm, quarto-deck, r-econometrics, code-review |
| 面向其他学科或其他用途 | scientific-writing, literature-review, citation-management, scientific-critical-thinking, hypothesis-generation, venue-templates, latex-posters, scientific-slides, copy-editing, frontend-design, frontend-slides, python-panel-data |
| 内容过于通用或与其他 skill 重复 | stata-data-cleaning, latex-tables, multi-perspective, project-deck, theme-factory, code-archaeology, project-safety |
| 管理 Claude 本身的工具，从未使用 | learn, lessons-learned, creation-guard, consolidate-memory, insights-deck |
| 与保留的 skill 重复 | peer-review（Referees 项目里有 reviewing-economics-articles），skill-deslop（与 avoid-ai-writing 相同） |
| 原 session-recap 的配套 skill | update-focus, sync-notion, session-log, update-project-doc |

`session-recap-original/` 是改造前的 session-recap，仅作备份。它和现行版本同名，**不要**直接恢复到顶层；需要时可以对照参考。

注意：`code-review` 归档后，`/code-review` 对应的是 Claude Code 自带的代码审查命令。如果恢复这个归档版本，它会盖住自带命令。

### 2026-10-25：由官方插件取代

| skill | 原因 |
|---|---|
| skill-creator | 这是 55 行的精简版。现已安装 Anthropic 官方插件 `skill-creator@claude-plugins-official`（完整版，带评测脚本）。精简版和插件版同时启用会重复，所以归档精简版 |

另外删除了两个只存在于本机、没有同步到 GitHub 的链接：

- `skills/skills`：指向自身的循环链接，应为误建；
- `skills/diagram-design`：指向 `~/code/diagram-design` 的链接，内容与 `diagram-design-real` 完全相同。现在 `diagram-design-real` 已改名为 `diagram-design`。如果以后想从上游更新这个 skill，需要手动把 `~/code/diagram-design/skills/diagram-design/` 的内容复制过来。
