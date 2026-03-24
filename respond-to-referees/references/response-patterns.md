# Response Patterns

> Reference for Phase 2 of `/respond-to-referees`. Taxonomy of common response types with structure and examples from economics.

## Pattern 1: Agree and Change

**When to use:** The comment identifies a genuine issue that has been fixed in the revision.

**Structure:**
1. Acknowledge the validity of the comment
2. State what was changed
3. Reference the specific location in the revised manuscript

**Example:**
> Reviewer: "The standard errors should be clustered at the firm level."

Response: "We agree with the reviewer that clustering at the firm level is more appropriate given the panel structure of our data. All tables have been updated with firm-level clustered standard errors. The results are qualitatively unchanged (see Tables 2-5)."

**Danger:** Do not over-explain or justify why you did it differently before. Just fix it and move on.

---

## Pattern 2: Already Addressed

**When to use:** The revision already fixes this, either independently or because another reviewer raised the same point.

**Structure:**
1. Acknowledge the concern
2. State that it has been addressed
3. Point to the specific location

**Example:**
> Reviewer: "The paper would benefit from a discussion of external validity."

Response: "We agree with the reviewer. We have added a discussion of external validity in Section 5.3 (page 18, paragraphs 2-3), which considers [specific aspects]."

**Danger:** Do not sound dismissive ("We already did this"). Frame it as agreement.

---

## Pattern 3: Partially Agree

**When to use:** The comment has merit, but the full request is excessive, impractical, or misguided.

**Structure:**
1. Concede the valid part explicitly
2. Describe the change you made (the partial concession)
3. Explain why the remaining part is not adopted, with evidence
4. Make a visible change so the reviewer sees responsiveness

**Example:**
> Reviewer: "The authors should estimate a full structural model to quantify welfare effects."

Response: "The reviewer raises an important point about welfare implications. While a full structural model is beyond the scope of the current paper (which focuses on identifying the causal effect of X on Y), we have added a back-of-the-envelope welfare calculation in Section 6 (page 22) that provides a first approximation. We have also added this as a direction for future research in the conclusion."

**Key principle from Martin (2008):** Even when you do not fully adopt the suggestion, make a small visible change so you can say you responded.

---

## Pattern 4: Disagree with Evidence

**When to use:** The comment is based on a factual error, methodological misunderstanding, or literature the reviewer missed.

**Structure:**
1. Acknowledge the concern (never dismiss it outright)
2. Present counter-evidence (cite literature, show results, or provide a logical argument)
3. Optionally make a small concession or clarification to show good faith
4. Reference where the clarification appears in the revised manuscript

**Example:**
> Reviewer: "The difference-in-differences assumption is violated because pre-trends diverge."

Response: "We appreciate the reviewer's careful attention to the parallel trends assumption. We respectfully note that Figure 3 (page 14) presents the event-study estimates, which show no statistically significant pre-treatment differential trends (all coefficients are individually and jointly insignificant at the 5% level; F-test p-value = 0.42). Following Roth (2022), we have also conducted a sensitivity analysis for violations of parallel trends, reported in Appendix Table A3. The results suggest our estimates are robust to moderate departures from the parallel trends assumption. We have expanded the discussion of these tests in Section 4.2 (page 15)."

**Key principle from Williams (2004):** If you are confident you are right, argue back with referenced facts. The editor can adjudicate.

---

## Pattern 5: Clarification

**When to use:** The reviewer misunderstood something because the writing was unclear.

**Structure:**
1. Accept responsibility for the lack of clarity (never blame the reviewer)
2. Restate the correct interpretation
3. Reference the revised text that now makes the point explicit

**Example:**
> Reviewer: "The treatment is endogenous because individuals self-select into the program."

Response: "We apologize for the lack of clarity in the original manuscript. Our identification strategy does not rely on program participation; instead, we exploit the staggered rollout of the program across municipalities as an exogenous source of variation. We have rewritten Section 3 (pages 8-9) to make the identification strategy more explicit, with a clearer description of the instrument and the exclusion restriction."

**Danger:** Never write "The reviewer failed to read..." or "As clearly stated in the paper..."

---

## Pattern 6: Answer a Question

**When to use:** The reviewer asks a specific factual question (data source, robustness check, sample size, etc.).

**Structure:**
1. Answer directly and concisely
2. Provide the requested information
3. Reference where it appears in the revision (if added to the manuscript)

**Example:**
> Reviewer: "What is the response rate for the survey?"

Response: "The response rate was 67.3%. We have added this information to Section 2.1 (page 5) along with a comparison to response rates in similar surveys in the literature."

---

## Pattern 7: Scope Limitation

**When to use:** The suggested analysis or extension is interesting but beyond the paper's scope. Use sparingly: more than 2-3 across the entire letter signals avoidance.

**Structure:**
1. Acknowledge the importance and interest of the suggestion
2. Explain concretely why it cannot be done (data limitations, methodological complexity, paper length, different research question)
3. Add it as a future research direction in the manuscript

**Example:**
> Reviewer: "The authors should extend the analysis to other countries to assess generalizability."

Response: "We agree that cross-country comparison would be valuable. Unfortunately, the administrative data we use are only available for [country], and comparable data structures do not exist in other settings to our knowledge. We have added a discussion of this limitation and its implications for external validity in Section 5.3 (page 19), and we note cross-country comparison as a direction for future research in the conclusion."

**Danger:** Overuse signals avoidance. If 4+ comments receive this response, reconsider whether some can be partially addressed.

---

## Pattern 8: Conflicting Reviewers

**When to use:** Two reviewers give contradictory advice.

**Structure:**
1. Transparently note the disagreement (do not hide it)
2. Explain which position you adopt and why
3. Cite one reviewer's reasoning to defend against the other

**Example:**
> Reviewer 1: "The paper is too long and should drop the heterogeneity analysis."
> Reviewer 2: "The heterogeneity analysis is the most interesting part and should be expanded."

Response to Reviewer 1: "We note that Reviewer 2 identifies the heterogeneity analysis as a key contribution of the paper. Given this, we have retained the analysis but condensed it by moving supporting tables to the appendix, reducing the main text by approximately one page."

Response to Reviewer 2: "We have expanded the discussion of the heterogeneity results in Section 5 (page 16), with additional interpretation of the mechanisms."

**Key principle from Williams (2004):** Conflicting reviewers are a gift. You get to choose which advice to follow.

---

## Pattern 9: Reducing Manuscript Length

**When to use:** The editor or reviewer asks to shorten the paper.

**Structure:**
1. State what was removed or moved to appendix
2. Briefly justify why those sections were chosen for removal
3. Note the net change in page count

**Key principle from Williams (2004):** Drop entire sections rather than trimming everywhere. Discussion sections are the best target for excisions.

**Example:**
> Editor: "Please reduce the manuscript by approximately 20%."

Response: "We have reduced the manuscript from 42 to 34 pages. The main changes are: (1) we moved the supplementary robustness checks (former Section 5.2) to Appendix B; (2) we condensed the literature review from 4 pages to 2 pages, focusing on the most directly relevant studies; and (3) we streamlined the discussion section by removing the speculative paragraphs on long-run implications. All core results, methods, and the heterogeneity analysis remain in the main text."

---

## Pattern 10: Adding New Analysis

**When to use:** The reviewer requests additional empirical work (robustness checks, placebo tests, subsample analysis, alternative specifications).

**Structure:**
1. Acknowledge the suggestion
2. Describe the new analysis briefly
3. Present the key result
4. Reference the new table, figure, or appendix section

**Example:**
> Reviewer: "Can the authors provide a placebo test using outcomes that should not be affected by the treatment?"

Response: "This is a helpful suggestion. We have conducted a placebo test using [outcome] as the dependent variable. As expected, we find no statistically significant effect (coefficient = 0.003, SE = 0.012; see Table A4 in the appendix). This supports the validity of our identification strategy. We have added a brief discussion of this test in Section 4.3 (page 16)."
