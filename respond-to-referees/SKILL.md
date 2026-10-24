---
name: respond-to-referees
description: "Compose professional response letters to referee and editor comments for academic journal R&R cycles. Produces a LaTeX response letter with cover letter to editor and point-by-point replies to each reviewer. Triggers: 'write response to referees', 'draft rebuttal letter', 'respond to reviewer comments', 'R&R response letter'. Not for extracting/organising comments (use /process-reviews). Not for proofreading (use /proofread)."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash(mkdir*), Bash(ls*), Bash(latexmk*), AskUserQuestion, Task]
argument-hint: "[path-to-comment-tracker or path-to-reviews-pdf or no arguments for guided setup]"
---

# Respond to Referees

Compose professional response letters to referee and editor comments. Implements the Three Golden Rules from Williams (2004): answer completely, answer politely, answer with evidence.

## When to Use

- After receiving an R&R decision and needing to write the response letter
- After `/process-reviews` has organized comments into `comment-tracker.md`
- When resubmitting a revised manuscript and need a cover letter to the editor
- When working from raw referee comments (PDF or text) without having run `/process-reviews`

## When NOT to Use

- Extracting and organizing referee comments from a PDF (use `/process-reviews`)
- Proofreading the response letter before submission (use `/proofread`)
- Reviewing someone else's manuscript (use the `reviewing-economics-articles` skill in the Dropbox/Referees project)
- Challenging your own arguments before responding (use `/devils-advocate`)

## Inputs

Gather via interview if not provided:

1. **Comment source** (one of):
   - `comment-tracker.md` from `/process-reviews` (preferred)
   - Individual `reviews/reviewer-{n}.md` files from `/process-reviews`
   - Raw reviews PDF or pasted text of referee comments
2. **Revised manuscript path** (`.tex` file, so responses can reference specific locations)
3. **Project path** (auto-detect from cwd)
4. **Venue and round** (auto-detect from correspondence directory if `/process-reviews` was run)
5. **Response language** (English or Chinese; default English)
6. **User's response notes** (optional: partial responses, preferred strategies for specific comments)

### Defaults

| Setting | Default | Override |
|---------|---------|---------|
| Output format | LaTeX | N/A |
| Output location | `correspondence/referee-reviews/{venue}-round{n}/` | User provides path |
| Cover letter | Included | User says "skip cover letter" |
| Tone | Formal, diplomatic | User says "more assertive" or "more conciliatory" |

## Output Location

Follow the directory structure established by `/process-reviews`:

```
correspondence/referee-reviews/{venue}-round{n}/
├── response-letter.tex          (primary output)
└── rebuttal.md                  (populated, if empty stub exists from /process-reviews)
```

If the round directory does not exist, create it. If `response-letter.tex` already exists, version it (`response-letter-v2.tex`).

## The Three Golden Rules

1. **Answer completely.** Respond to every comment. Number responses to match the reviewer's numbering or the R{n}-C{m} IDs from `/process-reviews`. Repeat or paraphrase each comment before responding. Split compound paragraphs into sub-comments (R1-C1.1, R1-C1.2). Never skip or merge comments. Even compliments get acknowledged.

2. **Answer politely.** Assume good faith. Thank the referee for specific insights. Use diplomatic language from `references/diplomatic-phrases.md`. Never be dismissive or arrogant. When the referee is wrong, state the correction gently with evidence.

3. **Answer with evidence.** Every disagreement must be supported by a reference, a result, or a logical argument. "We disagree" alone is never acceptable. Cite specific page numbers, section numbers, table numbers, or figure numbers in the revised manuscript.

## Protocol

### Phase 1: Gather and Organize

1. Confirm inputs (comment source, revised manuscript, venue, round)
2. If `/process-reviews` has been run, read `comment-tracker.md` and `review-analysis.md` for strategic context
3. If working from raw comments, extract and number them following the R{n}-C{m} convention; suggest running `/process-reviews` for better results
4. Read the revised manuscript to understand what changes have already been made
5. If the user has response notes, incorporate them

### Phase 2: Strategic Planning

1. Read `references/response-patterns.md` for the response taxonomy
2. Classify each comment by response type:
   - **Agree and change**: Comment is valid; describe what was changed
   - **Already addressed**: The revision already addresses this
   - **Partially agree**: Accept part, explain why the rest is not adopted
   - **Disagree with evidence**: Provide counter-argument backed by references or results
   - **Clarification**: The reviewer misunderstood; clarify without blame
   - **Question**: Answer directly
   - **Scope limitation**: Acknowledge, explain why it is beyond the current scope
   - **Conflicting reviewers**: Note the disagreement, explain which position is adopted
3. Draft a one-line strategy per comment
4. Identify cross-cutting themes that can be addressed once in the cover letter

### REVIEW GATE: Strategy Approval

Present to the user and STOP:
- Summary table: comment count by reviewer and by response type
- One-line proposed strategy for each comment
- Items where user input is essential (especially disagreements and scope limitations)
- Cross-cutting themes identified

Do NOT proceed until the user explicitly approves the strategy.

### Phase 3: Draft Response Letter

1. Read `references/diplomatic-phrases.md` for polite language
2. Read `templates/response-letter.tex` for the LaTeX template structure
3. **Cover letter to editor** (~1 page):
   - Thank the editor and reviewers for their time and constructive feedback
   - Summarize the major changes made to the manuscript
   - Highlight how cross-cutting themes were addressed
   - State that all comments have been addressed point by point below
4. **Point-by-point responses** (one section per reviewer):
   - Section header: "Response to Reviewer {N}"
   - For each comment:
     - Reproduce the original comment in the `refcomment` environment (sans-serif, grey background)
     - Write the response in the `response` environment (serif, regular text)
     - Include manuscript reference using `\manuscriptref{}` when a change was made
   - Vary diplomatic phrasing across responses (do not repeat the same opener)
   - Back every disagreement with a reference, data point, or logical argument
5. Pay special attention to the editor's suggestions (Martin 2008): they carry the most weight

### Phase 4: Quality Review

1. Read `references/quality-rubric.md` and apply quality scoring
2. Check against the Three Golden Rules:
   - **Completeness**: every comment has a response
   - **Politeness**: no dismissive or arrogant language detected
   - **Evidence**: every disagreement backed by a reference, result, or argument
3. Check writing conventions: no dashes in English prose, no contractions, no exclamation marks
4. Check causal language: do not escalate "association" to "effect" unless the identification strategy supports it
5. Run critic-fixer loop if score is below 90 (up to 3 rounds, per global rule)

### Phase 5: Compile and Finalize

1. Write `response-letter.tex` to the output directory
2. Compile with `latexmk -pdf` to verify it builds cleanly
3. If an empty `rebuttal.md` exists from `/process-reviews`, populate it with a plain-text summary
4. If `comment-tracker.md` exists, update the Status column to "Responded" for all comments
5. Present the final letter to the user with the quality score

## Critical Rules

1. **Never skip a comment.** Every referee comment gets a numbered response, no matter how minor.
2. **Never fabricate references.** If a reference is needed to support a claim, flag it for the user to provide.
3. **Never blame the referee.** Even when factually wrong, the response must be respectful.
4. **Quote verbatim.** When reproducing the referee's comment, use the exact text from the source.
5. **No dashes in prose.** Follow the user's global writing convention.
6. **Match causal language.** Do not escalate "association" to "effect" in the response.
7. **New results go in the manuscript.** Never introduce results only in the response letter.

## Anti-Patterns

- "We disagree" without providing evidence or reasoning
- "As we clearly stated..." or "The reviewer failed to read..." (blame the writing, not the reader)
- Copy-paste responses for overlapping comments (tailor each response)
- Using "obviously" or "clearly" (implies the reviewer should have known)
- Padding responses with irrelevant detail to appear thorough
- Overusing "beyond scope" for more than 2-3 comments (signals avoidance)
- Escalating causal language beyond what the identification strategy supports
- Using dashes (em, en, or hyphen) in English prose

## References

| File | When to read | Purpose |
|------|-------------|---------|
| `references/diplomatic-phrases.md` | Phase 3 | Polite response language by scenario |
| `references/response-patterns.md` | Phase 2 | Taxonomy of response types with examples |
| `references/quality-rubric.md` | Phase 4 | Skill-specific quality scoring deductions |
| `templates/response-letter.tex` | Phase 3 | LaTeX template with two-font design |

## Cross-References

| Skill | Relationship |
|-------|-------------|
| `/process-reviews` | **Upstream:** extract and organize comments before writing the response |
| `/proofread` | **Downstream:** proofread the response letter before submission |
| `/devils-advocate` | Stress-test responses to difficult comments |
| `/pre-submission-report` | Full quality check of the revised paper before resubmission |
| `/bib-validate` | Validate bibliography after adding new references in revision |
| `/latex-autofix` | Compile the response letter with autonomous error resolution |
