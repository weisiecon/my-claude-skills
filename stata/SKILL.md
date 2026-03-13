---
name: stata
description: "Working with Stata in this environment. Context on what Stata is, how to run it, create and execute do-files, and where documentation lives. Triggers: any task involving Stata, .do files, .dta files, or Stata commands."
allowed-tools: Bash(stata*), Bash(StataMP*), Bash(cat*), Bash(ls*)
---

# Stata Environment Skill

## What is Stata

Stata is a statistical software package used for data management, statistical analysis, and graphics. It is widely used in economics, political science, public health, and other social sciences. Stata uses its own scripting language executed via do-files (.do) and stores data in .dta format.

## Installation

Stata 16 MP (multi-processor) is installed on the Windows side of this WSL2 system.

| Item | Path |
|------|------|
| Installation directory | `/mnt/c/Program Files/Stata16/` |
| Executable | `/mnt/c/Program Files/Stata16/StataMP-64.exe` |
| Ado files | `/mnt/c/Program Files/Stata16/ado/` |
| License | `/mnt/c/Program Files/Stata16/STATA.LIC` |

## Running Stata

The `stata` alias is configured in `~/.bashrc`:

```bash
# Added to ~/.bashrc
export PATH="$PATH:/mnt/c/Program Files/Stata16"
alias stata='StataMP-64.exe'
```

- **Launch GUI:** Run `stata` from the terminal. This opens the Stata GUI on the Windows desktop.
- **Run a do-file in batch mode:** `StataMP-64.exe /e do "path/to/script.do"` (runs the do-file and exits).
- Stata is a Windows GUI application called from WSL. It cannot produce interactive terminal output in the WSL console. Use batch mode (`/e`) for scripted execution.

## Do-files

Do-files (.do) are Stata's script files. They contain a sequence of Stata commands.

### Creating do-files

When creating or editing .do files:

1. Use UTF-8 encoding (Stata 14+ supports Unicode).
2. Use Windows-style line endings (CRLF) since Stata runs on Windows. If writing from WSL, convert with `unix2dos` if needed.
3. Include a header block with project info, author, date, purpose, and input/output files.
4. Use `///` for line continuation in long commands.
5. Always `set more off` and open a log file near the top.

### Standard do-file structure

```stata
/*==============================================================================
    Project:    [Name]
    Author:     [Author]
    Date:       [Date]
    Purpose:    [Description]
    Input:      [Input files]
    Output:     [Output files]
==============================================================================*/

clear all
set more off
cap log close
log using "logfile.log", replace

* --- Your code here ---

log close
```

### Running do-files from WSL

```bash
# Open Stata GUI (interactive)
stata

# Run a do-file in batch mode (no GUI)
StataMP-64.exe /e do "/path/to/script.do"
```

Note: Paths passed to Stata should use Windows conventions when running via the Windows executable. WSL paths under `/mnt/` generally work, but for reliability use the Windows path format (e.g., `D:\Dropbox\project\script.do`).

## Documentation (PDF Manuals)

Stata 16 ships with full PDF documentation at `/mnt/c/Program Files/Stata16/docs/`. Key manuals:

| File | Manual |
|------|--------|
| `u.pdf` | User's Guide (start here for Stata basics) |
| `r.pdf` | Reference manual: core estimation and statistics commands |
| `d.pdf` | Data management commands |
| `g.pdf` | Graphics |
| `fn.pdf` | Functions |
| `i.pdf` | Glossary and index |
| `p.pdf` | Programming (ado-file development, Mata basics) |
| `m.pdf` | Mata (matrix programming language) |
| `st.pdf` | Survival analysis |
| `ts.pdf` | Time series |
| `xt.pdf` | Panel data / longitudinal |
| `svy.pdf` | Survey data |
| `me.pdf` | Multilevel mixed-effects models |
| `sem.pdf` | Structural equation modeling |
| `mi.pdf` | Multiple imputation |
| `te.pdf` | Treatment effects |
| `mv.pdf` | Multivariate statistics |
| `bayes.pdf` | Bayesian analysis |
| `erm.pdf` | Extended regression models |
| `lasso.pdf` | Lasso and elastic net |
| `meta.pdf` | Meta-analysis |
| `irt.pdf` | Item response theory |
| `fmm.pdf` | Finite mixture models |
| `dsge.pdf` | Dynamic stochastic general equilibrium models |
| `sp.pdf` | Spatial autoregressive models |
| `cm.pdf` | Choice models |
| `pss.pdf` | Power, precision, and sample size |
| `ig.pdf` | Import/export guide |
| `rpt.pdf` | Reporting |
| `gsw.pdf` | Getting Started with Stata for Windows |
| `gsu.pdf` | Getting Started with Stata for Unix |
| `gsm.pdf` | Getting Started with Stata for Mac |
| `stoc.pdf` | Stochastic frontier models |

To read a manual: `"/mnt/c/Program Files/Stata16/docs/u.pdf"` (open with a PDF reader or use the `/split-pdf` skill).

## Conventions (from user preferences)

- Always check compatibility between statistical commands and options like `cluster()` before generating code.
- For coefficient comparison tests, use `suest` rather than pooled regressions with interaction terms.
- After generating or modifying .do files, remind the user to check the Stata log file for errors.
- Include comments explaining each section of the code.
- Research projects live under `D:\Dropbox\PhD_Projects\` (accessible at `/mnt/d/Dropbox/PhD_Projects/` from WSL).

## Related Skills

- `stata-data-cleaning` — Reproducible data cleaning workflows
- `stata-regression` — Regression analysis with publication-ready tables
