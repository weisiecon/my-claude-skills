---
name: lit-review-verify
description: Use when the user wants to check whether the papers cited in a LaTeX or markdown manuscript actually support the claims they are attached to, and to find better references where they do not. Triggers on "check my citations", "verify references", "citation audit", "do my citations support what I wrote", "核查引用", "检查文献是否支持论断", or "/lit-review-verify". Not for checking citation keys or .bib metadata (use bib-validate).
argument-hint: "[path-to-tex-or-md] [--bib path-to-bib] [--section intro|litreview|all]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, WebSearch, WebFetch, Skill, mcp__mcpsemanticscholar__search-paper-title, mcp__mcpsemanticscholar__get-paper-abstract, mcp__mcpsemanticscholar__papers-search-basic
---

# Citation Verification

Read a manuscript (`.tex` or `.md`), extract every substantive claim that carries a citation, and check whether the cited work actually supports it. Where a citation is weak, suggest a better reference. The goal is to catch misattributions, overstated findings, and unsupported claims before a referee does.

## Input

- **Manuscript** (required): a `.tex` or `.md` file. For `.tex`, also read the files it pulls in with `\input{}` or `\include{}`.
- **`--bib`** (optional): the `.bib` file. If omitted for `.tex`, resolve `\bibliography{...}` or `\addbibresource{...}` relative to the manuscript. For `.md`, look for a `.bib` file with the same base name.
- **`--section`** (optional): `intro`, `litreview`, or `all` (default). Detect sections by `\section{...}` in `.tex` or `## ` headers in `.md`; match liberally.

If no arguments are given, list the `.tex` and `.md` files in the current directory and ask which one to check.

## Phase 1: Extract claim and citation pairs

1. **Find citations.** In `.tex`, every sentence containing `\cite`, `\citet`, `\citep`, `\citeauthor`, `\citeyear`, `\citealt`, `\citealp`, or a natbib or biblatex variant. In `.md`, author and year patterns such as "Author (Year)", "Author and Author (Year)", "Author et al. (Year)", and "(Author, Year)". Record the claim text, the citation key or keys, and the file and line.
2. **Skip non-substantive citations:** bare "see also" lists, self-citations, acknowledgments. When in doubt, include.
3. **Classify each pair:**

| Type | Meaning | Example |
|---|---|---|
| **FINDING** | Attributes a specific empirical result, direction, or magnitude to the cited work | "Doepke et al. (2023) document that across high-income countries the relationship between women's labor force participation and fertility is now positive" |
| **FACTUAL** | States a fact or statistic and cites a source | "The total fertility rate fell to X in year Y (Source, Year)" |
| **METHOD** | Cites a work for its method | "Following Abadie et al. (2023), we cluster at the level of treatment assignment" |
| **GENERAL** | Broad reference to a literature or idea | "A large literature studies the quantity and quality of children" |

Mark citations of statistical releases, government reports, and data portals (statistical yearbooks, NBS communiqués, World Bank indicators) as **DATA SOURCE**; they are FACTUAL claims that are checked against the source itself (Phase 2, step 4).

Do not stop for review after this phase; continue directly.

## Phase 2: Retrieve the cited works

**Step 1. Run the fetcher for the cited keys.** It reads the `.bib` file, uses the DOI when the entry has one, and otherwise searches Crossref by authors, title, and year. It accepts a match only when the titles are close (similarity of at least 0.85), then tries Crossref, OpenAlex, Semantic Scholar, and finally the publisher's landing page (Springer journals, for example, put the full abstract in the page's meta tags). Most of the user's `.bib` entries have no DOI, so the title search matters.

```bash
python3 ~/.claude/skills/lit-review-verify/scripts/fetch_abstract.py \
  --bib "<path/to/refs.bib>" --keys key1,key2,key3 > "<scratch>/citations.jsonl"
```

- Write the output to the session scratchpad directory if one is provided, otherwise to a temporary folder.
- It takes about 4 seconds per entry. For more than about 30 keys, run it in the background and tell the user it is running.
- Each output line has: `key`, `bib_title`, `bib_year`, `match` (for example "doi in .bib", "crossref title match 0.97", or "unresolved ..."), `doi`, `source`, `title`, `year`, `venue`, `abstract`, `cited_by_count`, and `tried` (what each source returned).
- The same title often exists as a working paper and as a published article. The fetcher picks the version whose year is closest to the `.bib` year and lists the others in `other_versions`. If it had to borrow the abstract from another version, `abstract_from` says which one. A working-paper abstract is usually adequate for verification, but say so in the report when a verdict rests on it, and check that the `.bib` entry cites the published version.
- On the Windows (PowerShell) machine, call `python` with the Windows path to the same script.

**Step 2. Fill gaps for academic works.** For entries that were matched but have no abstract, or were unresolved:

1. If Semantic Scholar was rate limited (`HTTP 429` in `tried`), retry with `mcp__mcpsemanticscholar__search-paper-title`, then `mcp__mcpsemanticscholar__get-paper-abstract` with the returned paper ID or `DOI:<doi>`.
2. For working papers and journal pages, find the landing page with WebSearch, then run `fetch_abstract.py --url <page>`. It returns abstract candidates from the page's meta tags. Check that the text is the paper's abstract: some sites (for example NBER) put a generic site description there. SSRN usually refuses scripted access.
3. As a last resort, use WebFetch on the landing page. WebFetch returns a short paraphrase rather than the full text, so use it only to rule out clear mismatches; do not mark a FINDING as SUPPORTED on WebFetch alone.
4. If the user keeps PDFs of the references (ask once, or look for a folder such as `Literature/` or `References/` in the project), use the `split-pdf` skill to read the abstract, introduction, and conclusion for any pair that is still UNCERTAIN or PARTIAL after the abstract check.

**Step 3. Unresolved entries.** If the title search fails, show the `.bib` title next to the nearest Crossref title. Never guess a DOI. Chinese-language publications are rarely covered by these sources; ask for the PDF or mark them UNVERIFIABLE.

**Step 4. DATA SOURCE citations.** Check the cited number on the official page when it is accessible (WebFetch), and report the exact figure, table, and year found. Do not search for academic alternatives to a data source.

## Phase 3: Verify

Compare each claim with the retrieved text. Apply strictness by claim type:

| Claim type | Strictness | What to check |
|---|---|---|
| **FINDING** | Strict | The source must report a result consistent with the claimed direction, mechanism, population, and setting. If the claim says "X causes Y", the source must support a causal relationship, not only a correlation or the reverse direction. |
| **FACTUAL** | Medium | The source should be consistent with the stated fact. Abstracts may not contain exact numbers; look for consistency rather than an exact match. |
| **METHOD** | Low | The source should describe or be consistent with the cited method. Flag only clear mismatches. |
| **GENERAL** | Lenient | Flag only if the work is clearly about a different topic. |

**Causal language.** Follow the user's rule that causal wording ("effect", "causes", "leads to") must match the strength of the identification. If the manuscript states a causal effect but the cited study reports associations, the verdict is PARTIAL, and the suggested fix softens the wording (for example "is associated with").

Assign one verdict to each pair:

| Verdict | Meaning |
|---|---|
| **SUPPORTED** | The source clearly supports the claim |
| **PARTIAL** | Related, but the claim overstates, understates, or slightly misrepresents the finding |
| **MISMATCH** | The source contradicts the claim or is clearly about something else |
| **UNCERTAIN** | Cannot be determined from the retrieved text |
| **UNVERIFIABLE** | No usable text could be retrieved |

**Be conservative with MISMATCH.** An abstract is a summary; the full paper may contain the supporting evidence. When in doubt, use UNCERTAIN.

## Phase 4: Better references

Search only for pairs rated PARTIAL, MISMATCH, UNCERTAIN, or UNVERIFIABLE, and never for GENERAL claims or DATA SOURCE citations.

- Search with `fetch_abstract.py --query "<keywords from the claim>"` (Crossref) and `mcp__mcpsemanticscholar__papers-search-basic`. Then retrieve each candidate's abstract with `fetch_abstract.py --doi <doi>`.
- Suggest an alternative only if its retrieved abstract supports the specific claim more directly, it is published in a peer-reviewed journal (prefer the published version to a working paper), and it is reasonably well cited (`cited_by_count`). A newer paper qualifies if it makes the same or a stronger point.
- Do not suggest marginal improvements, or the working-paper version of the same published paper.
- At most two alternatives per claim. Never propose a reference from memory: every alternative needs a DOI and a retrieved abstract.

## Phase 5: Report

**Where to save.** Save `citation_verification_YYYY-MM-DD.md` in the project folder (for example under `PhD_Projects/<project>/`). Do **not** save it inside an Overleaf-synced folder (`Dropbox/Apps/Overleaf/...`), because Overleaf would publish it to all collaborators. If the location is unclear, ask.

**Language.** Write the report in the language the user writes in. Keep quotations and suggested manuscript text in English.

**Structure:**

```markdown
# Citation Verification: <manuscript file>

- Date: YYYY-MM-DD
- Files checked: ...
- Sections: ...
- Bibliography: ...
- Retrieval: N abstracts (Crossref n1, OpenAlex n2, Semantic Scholar n3, landing pages n4, PDFs n5); N unresolved

## Summary

| Verdict | Count |
|---|---:|
| SUPPORTED | |
| PARTIAL | |
| MISMATCH | |
| UNCERTAIN | |
| UNVERIFIABLE | |

## Issues

### Suggestion 1: <key> (<file>, line <n>), <VERDICT>, <TYPE>

**Claim:** <exact text from the manuscript>

**Evidence:** "<quotation from the retrieved text>" (<source>)

**Assessment:** <why the verdict>

**Suggested fix:** <drop-in replacement for the claim text>

**Alternative reference (optional):** <Authors (Year), Title, Journal, DOI>: <why it fits better>

## Could not be verified

| Key | Reason |
|---|---|
```

Number only PARTIAL and MISMATCH items as "Suggestion N". List UNCERTAIN and UNVERIFIABLE items under "Could not be verified" with the reason. Never list SUPPORTED pairs. Present the summary and the issues in the conversation as well.

## Implementing suggestions

When the user says "implement suggestion N" (or "accept N", "apply 1 and 3"):

1. Read the current file and locate the exact claim text.
2. Apply the fix with Edit, preserving the sentence structure and all LaTeX commands. Change only what is necessary; for an overstated finding, soften the wording rather than delete the citation.
3. If the fix adds a new citation key, add a BibTeX entry generated from the DOI, never written from memory:
   `curl -sL -H "Accept: application/x-bibtex" https://doi.org/<doi>`
   Rename the key to match the style of the existing `.bib` keys.
4. Report the file and line changed.

If the project defines its own procedure for editing manuscript files (for example, edit a local copy and then push it to an Overleaf mirror), follow that procedure instead of editing the synced file directly.

## Rules

- Never fabricate abstracts or paper content. Every verdict must rest on retrieved text, and the report must quote it.
- Be conservative with MISMATCH; prefer UNCERTAIN when in doubt.
- In suggested English text, follow the user's writing rules: no dashes as punctuation, no contractions.
- If a source fails or is unavailable, say which citations could not be verified and why; never skip them silently.
- The user works in applied microeconomics (labor, health, population, economics of science). Read designs such as DiD, event studies, IV, RDD, and shift-share instruments correctly when classifying and verifying claims.
- Run the whole pipeline (extract, retrieve, verify, search alternatives, report) in one pass. Stop only to ask for the PDF folder or the report location when needed.

## Source and license

Rewritten from `lit-review-verify` in [amatray/claude-skills-public](https://github.com/amatray/claude-skills-public) by Adrien Matray, released under the MIT License (see `LICENSE.txt`). Kept from the original: claim types, strictness levels, verdict categories, the criteria for alternative references, and the implementation procedure. Changed on 2026-10-25: the private bib-cleaner MCP server, the Zotero database, and the original author's file paths were replaced by `scripts/fetch_abstract.py` (Crossref, OpenAlex, Semantic Scholar, and page metadata), the Semantic Scholar MCP tools, and local PDFs read with split-pdf. Also added: title matching for `.bib` entries without a DOI, handling of data-source citations, the causal-language check, the Overleaf-folder safeguard, and a report template.
