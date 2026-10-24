---
name: session-recap
description: "End-of-session wrap-up: update project_memory.md (completed work, key decisions, next steps), write a session log in log/, then offer a git commit. Triggers: 'wrap up', 'end session', 'what did we do today', '收尾', '今天先到这里'."
allowed-tools: Bash(git*), Bash(wc*), Bash(date*), Bash(mkdir*), Read, Write, Edit, Glob, Grep, AskUserQuestion
argument-hint: (no arguments)
---

# Session Recap: End-of-Session Wrap-Up

Run when the user is finished for the day or is switching projects. It produces three things, in this order:

1. An updated `project_memory.md` (the user's convention, stated in the global CLAUDE.md and in most project CLAUDE.md files)
2. A session log at `log/YYYY-MM-DD-HHMM.md`
3. A git commit, only after the user chooses one

Rules:

- Write only inside the project root. Never write to `.context/`, Notion, or any other external location.
- Do not launch subagents. Everything runs in the main conversation, which already holds the session context.
- Never push to a remote without an explicit choice by the user.

## Step 1: Locate the project (silent)

- Project root: `git rev-parse --show-toplevel` if inside a repo, otherwise the current working directory.
- A valid project root contains `project_memory.md` or `CLAUDE.md`. If neither exists (for example, the CWD is `PhD_Projects/` or the home folder), ask which project the session belongs to before writing anything.
- Print one line: `Session closing for: <project name> (<path>)`.
- If the project's own `CLAUDE.md` or `AGENTS.md` defines how `project_memory.md` is kept, or defines a commit and push procedure (for example, an Overleaf mirror workflow), the project rules take precedence over this skill.

## Step 2: Read the memory file efficiently

`project_memory.md` can be very large (some projects exceed 1 MB). Do not read the whole file.

- Run `wc -l project_memory.md`.
- Read only the first 150 lines, to see the latest entries and the format in use.
- Use Grep with the pattern `^## ` on the file to see its section structure.
- Decide which format the file uses:
  - **Status document:** fixed sections such as `Last Updated`, `Completed Work`, `Key Decisions`, `Next Steps`.
  - **Dated log:** newest-first entries such as `## YYYY-MM-DD HH:MM: ...` directly below the title.

If the file does not exist, it will be created from the template in Step 4.

## Step 3: Draft and confirm (one interaction)

Draft from the conversation:

- **Completed:** what was actually done this session (files changed, results obtained, edits applied). Be concrete; give file paths where useful.
- **Key decisions:** choices made and the reason for each (for example, "Switched to `suest` for gender tests").
- **Next steps:** a short numbered list for the next session. Carry forward items from the previous entry that are still open; drop items finished this session.

Show the draft, then ask one `AskUserQuestion` with `multiSelect: true`:

- **Update project_memory.md (Recommended)**
- **Write session log (Recommended)**

The user may correct the draft in their answer.

## Step 4: Write

### project_memory.md

Follow the format the file already uses.

- **Status document:** update `Last Updated`, add the session's work under `Completed Work` with the date, update `Key Decisions`, and replace `Next Steps` with the new list.
- **Dated log:** insert one new entry directly below the title, matching the style of the existing entries:

```markdown
## YYYY-MM-DD HH:MM: <one-line summary>

- **Completed:** ...
- **Key decisions:** ...
- **Next steps:**
  1. ...
```

- **New file:** use this template:

```markdown
# Project Memory: <Project Name>

## Last Updated: YYYY-MM-DD

## Current Status
<two or three sentences>

## Completed Work
### YYYY-MM-DD
- ...

## Key Decisions
- ...

## Next Steps
1. ...
```

Keep each session's entry short (aim for fewer than 40 lines). Detail belongs in the session log; the memory entry can point to it.

**Size check:** if `project_memory.md` has more than about 500 lines, tell the user once, in one sentence, that the file is long for something read at the start of every session, and offer to move older entries into `project_memory_archive.md`. Never move or delete entries without explicit approval.

### Session log

Create `log/YYYY-MM-DD-HHMM.md` (create `log/` if needed):

```markdown
# Session Log: YYYY-MM-DD HH:MM

## Project: <name>

## What We Did
- ...

## Key Decisions
- ...

## Open Issues and Next Steps
1. ...

## Files Changed
- `path/to/file`: what changed
```

Write both files in the language that the existing `project_memory.md` uses. In English prose, follow the user's writing rules: no dashes as punctuation, no contractions.

### Auto memory

If the session revealed a durable fact about how the user wants to work (a preference or a correction, not project content), save it to auto memory as the memory instructions describe. Do not copy `project_memory.md` content into auto memory.

## Step 5: Git (always last)

- If the project root is not a git repo, skip this step silently.
- Run `git status --short` and `git diff --stat`.
- If there are changes, list the files that would be committed. If some changes are unrelated to this session, point them out.
- Ask with `AskUserQuestion`: **Commit only (Recommended)**, **Commit and push**, or **Skip**.
- Stage only the files the user agreed to. Do not push unless the user chose **Commit and push**.

## Step 6: Summary

Print:

```
Session closed: <project>
  project_memory.md: updated / skipped
  Session log:       log/YYYY-MM-DD-HHMM.md / skipped
  Git:               committed (abc1234) / committed and pushed (abc1234) / skipped / not a repo
```
