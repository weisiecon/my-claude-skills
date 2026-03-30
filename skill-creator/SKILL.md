---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

The process:
1. Understand what the user wants the skill to do
2. Write a draft SKILL.md
3. Create test prompts and run them
4. Evaluate results with the user (qualitatively and quantitatively)
5. Rewrite based on feedback
6. Repeat until satisfied

## Skill Structure

Every skill lives in a folder:
- SKILL.md (required): YAML frontmatter with name and description, plus markdown instructions
- scripts/ (optional): executable code for deterministic tasks
- references/ (optional): docs loaded into context as needed
- assets/ (optional): templates, icons, fonts

## SKILL.md Frontmatter

- name: skill identifier
- description: when to trigger and what it does. Make it slightly "pushy" to avoid undertriggering.

## Writing Guidelines

- Keep SKILL.md under 500 lines
- Description is the primary trigger mechanism
- Put all "when to use" info in the description, not the body
- Be specific about input/output formats
- Reference bundled files clearly with guidance on when to read them

## Creating a New Skill

1. Ask: what should this skill do, when should it trigger, what is the expected output?
2. Interview the user about edge cases and success criteria
3. Write the SKILL.md draft
4. Test with representative prompts
5. Iterate based on feedback

## Improving an Existing Skill

1. Read the current SKILL.md
2. Identify weaknesses: does it trigger correctly, are instructions clear, are outputs good?
3. Propose specific edits
4. Test the changes
5. Repeat

Always be flexible. If the user says "just vibe with me", skip formal testing and iterate conversationally.
