---
name: audit-code
description: Use when the user asks to audit, review, or check Stata do-files for undefined macros, broken paths, internal consistency, estimation-option errors, or unused variables. Triggers on "audit code", "audit my do-files", "check my Stata code", "检查我的 Stata 代码", "审查 do 文件", or "/audit-code".
argument-hint: "[path-to-dofiles-directory or do-file]"
---

# audit-code

Systematic audit of Stata do-files in three modules: (1) paths and macros, (2) a per-file audit that separates critical problems from suggestions, (3) unused variables.

## Working principles

**Work modularly, one module at a time.** Stop after each module and wait for confirmation. Reason: code audits compound noise fast. If Module 1 surfaces 30 issues and the user catches a false positive, recalibrate before Module 2 generates 30 more in the same wrong direction.

**Flag unknowns explicitly instead of guessing.** Stata code is full of context-dependent behavior (locals versus globals, scoping inside `program`, version-specific defaults). A guess that sounds confident is worse than an unknown that prompts the user to clarify.

**Report only problems.** Do not list what you checked or what was already fine.

**Language.** Write the audit in the language the user writes in. Keep code, file names, and Stata output as they are.

## This machine

- Stata 16 MP, installed at `C:\Program Files\Stata16` (WSL path `/mnt/c/Program Files/Stata16`). See the `stata` skill for how to run do-files from WSL.
- Community-contributed packages live in `C:\ado\plus` (WSL path `/mnt/c/ado/plus/<first letter>/<command>.ado`). As of 2026-10-25, `gtools`, `ftools`, `reghdfe`, and `ppmlhdfe` are installed; `ivreghdfe` is **not** installed.
- When a do-file calls a community-contributed command, check that its `.ado` file exists under `/mnt/c/ado/plus`. If it does not, report a Critical issue and give the install line (for example `ssc install ivreghdfe`).

## Scope (before Module 1)

Projects can contain thousands of do-files, including old versions and backups. Before auditing:

1. List the do-files in the given path.
2. If there are more than about 15, ask which ones are in scope. Suggest starting from the master do-file (for example `00_master.do` or `main.do`) and the files it calls with `do` or `run`.
3. Skip files or folders whose names suggest old versions or backups (`old`, `backup`, `archive`, `bak`, `_v1`, dated copies) unless the user includes them.
4. Confirm the list and the order in which the files run.

## Workflow

Three modules, run strictly in order, each ending at a STOP checkpoint.

---

## Module 1: Paths and macros

Check that every macro used in a later do-file is defined somewhere earlier in the run order, and that every path is correctly specified (exists, uses the project's global path macros consistently, and does not mix `\` and `/` in a way that breaks on the other machine).

**Present for review:**

1. Every instance where a macro is used but not defined (file, line, macro name)
2. Macros that are defined but never used, with the do-file where each is defined
3. Paths that do not exist or are hard-coded to one machine

**STOP and wait for approval to proceed to Module 2.**

---

## Module 2: Audit each do-file separately

### Structure of the audit

For each do-file, separate **critical** problems from **suggestions**.

- List all Critical issues in order of line number, then all Suggestions in order of line number. Never jump backwards within a category.
- For each item report: (1) the line, (2) the actual code, (3) a solution with corrected code.
- Label items "Critical 1, Critical 2, ..." and "Suggestion 1, Suggestion 2, ..." so the user can refer to them.

### What counts as critical

Critical means the code will fail, or will run but produce wrong results. In addition to ordinary bugs (wrong variable, wrong merge key, wrong sample restriction, overwritten data), check these:

**Stata 16 compatibility.** Commands and syntax introduced in Stata 17 or later will not run here. Examples: `collect`, `etable`, the redesigned `table` syntax of Stata 17, `didregress`, and `xtdidregress`. Flag any use as Critical.

**`suest` requirements** (Stata 16 [R] manual, `suest`, pp. 2595 to 2597):

1. Each model must come from an estimation command whose `predict` can generate equation-level scores with the `score` (or `scores`) option. If you are not sure that a command supports this, say so and point the user to `help <command> postestimation`; do not assert it.
2. The component models must be estimated **without** `vce(robust)` or `vce(cluster clustvar)`. `suest` always computes the robust variance and takes clustering through its own option: `suest m1 m2, vce(cluster clustvar)`.
3. The estimation results must be stored with `estimates store` before calling `suest`.

**Estimation options.** Check that each command accepts the options it is given (for example `vce(cluster ...)`, `absorb()`, weights). Report an incompatibility as Critical only when you can name it precisely; otherwise list it as an unknown for the user to check.

**Missing packages.** A call to a community-contributed command that is not installed (see "This machine") is Critical.

**Not a problem in Stata:** referring to a tempfile outside the loop in which it was created. As long as the do-file runs, tempfiles persist for the session.

### Valid community-contributed commands

Do not flag these as errors (all are installed on this machine except where noted):

- **gtools:** `gcollapse`, `gcontract`, `gegen`, `gduplicates`, `gisid`, `glevelsof`, `greshape`, `gquantiles`, `gstats`, `gtoplevelsof` (`gtop`), `gunique`, `gdistinct`, `hashsort`
- **ftools:** `fcollapse`, `fegen`, `fisid`, `flevelsof`, `fmerge`, `fsort`, `join`
- **Packages built on ftools:** `reghdfe`, `ppmlhdfe` (installed) and `ivreghdfe` (**not installed**)

Note that `gsort` is a base Stata command, not part of gtools.

### Suggestions to include

- **Coefficient comparisons.** The user's convention is to test whether a coefficient differs across models with `suest`, not with a pooled regression and interaction terms. Where the code compares coefficients across groups with a pooled interaction model, suggest the `suest` version (and respect the three requirements above).
- Code that can be made clearly more compact or clear without changing results.

### Never include as suggestions

- Replacing base commands with gtools or ftools equivalents (`egen` to `gegen`, `collapse` to `gcollapse`, and so on). The user's code uses base Stata consistently; do not raise speed unless the user asks about performance.
- Replacing `merge` with `fmerge`.
- Missing `compress` before `save`, or missing `quietly`.
- Adding comments, header blocks, or log commands to existing code. These are the user's conventions for new code (see the stata-conventions rule); check them only if the user asks for a conventions review.

### How to write the audit

- **Think first, write second.** Before writing any item, verify that it is an actual problem requiring a change.
- **Each item you write is final.** If you are unsure whether something is a problem, do not include it as an item; mention it as an unknown instead. Never write "I withdraw this" or "actually this is fine."
- **Every numbered item must contain a code change.** If you cannot write "Solution:" followed by different code, do not create the item.
- Before presenting, delete any item whose solution is identical to the original or that merely confirms the code is correct. If a do-file has no issues, write only "No critical issues" and "No suggestions."

### Mandatory stop after each do-file

After auditing one do-file:

1. Present the findings (critical issues, then suggestions, then unknowns).
2. **Stop completely** and wait. The user may have questions or corrections.
3. Do not move to the next do-file until the user explicitly says **"next"** (or "下一个"). Any other reply, including "ok", "thanks", corrections, or questions, is not permission to proceed.

End each stop with:

```
STOPPED - AWAITING YOUR INPUT
To move to the next do-file, say "next"
```

### Consistency based on user feedback

If the user corrects or clarifies the audit approach at any stop (a classification change, "don't flag X", an approved pattern, a threshold, an intentionally unused variable, a style preference), apply that correction to every remaining do-file. Before auditing each new do-file, review all earlier feedback. Never flag an issue type again after the user has said it should not be flagged.

---

## Module 3: Unused variables

Go through all in-scope code again and identify variables that are created but never used later (in a later command, a saved dataset that a later do-file uses, or an output table).

**Present for review:**

1. Variables created but never used
2. The do-file and line where each is created

**STOP and wait for final approval.**

---

## Implementing fixes

Edit do-files only when the user explicitly asks (for example "implement Critical 2 and Suggestion 1").

- Show the full corrected lines with file name and line number.
- Save do-files with Windows (CRLF) line endings, because Stata runs on the Windows side: run `unix2dos <file>` after editing.
- After any edit, remind the user to run the do-file and check the Stata log for errors.

---

## Source and license

Adapted from `audit-code` in [amatray/claude-skills-public](https://github.com/amatray/claude-skills-public) by Adrien Matray, released under the MIT License (see `LICENSE.txt`). Changes made on 2026-10-25: removed the rule that always suggested gtools replacements; corrected the gtools and ftools command lists; added a scope step, Stata 16 compatibility checks, the documented `suest` requirements, a missing-package check, the user's coefficient-comparison convention, and CRLF handling.
