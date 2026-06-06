---
description: Research, synthesize, and write a security skill with 100+ references. Usage: /skill-research <topic description>
subtask: true
---

You are the skill-research workflow for the cyber-security Agent Skills repository.
Your task is to create or fine-tune a skill based on the user's request: $ARGUMENTS

Execute the following 4 phases **strictly in order**. Phase 3 requires user confirmation before proceeding to Phase 4.

---

## Phase 1: Scope Definition

1. Read `@manifest.json` and `@AGENTS.md` to understand the project structure and existing skills
2. Check `@skills/index.json` for all existing skills
3. Based on the user's request, determine:
   - **Skill name** (kebab-case, e.g. `mobile-security-testing`)
   - **Description** (one-line, max 160 chars)
   - **Category**: Red Team (pentesting/exploitation), Blue Team (defense/SOC/IR), or General (frameworks/processes)
   - **Target audience** (e.g. `penetration-testers`, `soc-analysts`, `developers`, `security-engineers`)
   - **Metadata tags** (approach, source, standard, workflow)
4. Check for duplicate/overlapping skills with existing ones. If a similar skill exists, propose to **extend** it instead of creating a new one
5. Present the proposed scope to the user and ask for confirmation before proceeding

---

## Phase 2: Deep Research (100+ References)

Conduct **extensive** web research using `websearch`. Run **15-25 parallel searches** targeting different categories. Use `type: "deep"` for comprehensive results.

### Required Research Categories (adapt to the skill domain):

| # | Category | Example search patterns |
|---|----------|------------------------|
| 1 | Official Standards/Frameworks | "<topic> standard framework guidelines", "NIST <topic>", "OWASP <topic>" |
| 2 | Official Documentation | "official documentation <topic>" |
| 3 | Books | "best books <topic> 2024 2025 2026" |
| 4 | Tools — SAST | "<topic> SAST static analysis tools" |
| 5 | Tools — DAST/Scanner | "<topic> DAST dynamic analysis tools" |
| 6 | Tools — SCA/Dependency | "<topic> software composition analysis tools" |
| 7 | Tools — Infrastructure | "<topic> infrastructure security IaC tools" |
| 8 | Tools — CI/CD Security | "<topic> CI/CD pipeline security tools" |
| 9 | Certifications | "<topic> certifications 2025 2026" |
| 10 | Training & Courses | "<topic> training courses hands-on" |
| 11 | GitHub Awesome Lists | "awesome <topic> github" |
| 12 | Communities | "<topic> community forums" |
| 13 | Whitepapers & Research | "<topic> whitepaper research paper" |
| 14 | Cloud-specific guidance | "AWS/Azure/GCP <topic> security best practices" |
| 15 | Kubernetes/Container (if relevant) | "Kubernetes <topic> security" |
| 16 | Threat Modeling (if relevant) | "<topic> threat modeling" |
| 17 | Compliance/Regulatory (if relevant) | "<topic> compliance regulatory requirements" |
| 18 | Methodology & Mindset | "<topic> methodology approach mindset" |
| 19 | Books & Publications | "<topic> must read books 2024 2025 2026" |
| 20 | Podcasts/Video/Conferences | "<topic> conference talks podcasts" |

### Research Guidelines:
- Collect **URLs**, **author/organization names**, and **brief descriptions** for each reference
- Prioritize official sources (NIST, OWASP, ISO, CIS) over blog posts
- For tools: note language, open-source status, and GitHub stars when available
- For certifications: note cost, exam format, and prerequisite requirements
- For courses: note provider, cost, hands-on lab count
- For books: note author, year, and primary focus
- Organize raw findings into categories as you collect them

---

## Phase 3: Synthesis & Confirmation

After collecting 100+ references:

1. Organize findings into a proposed **SKILL.md structure** with sections:
   - Frontmatter (YAML)
   - Introduction / Filosofi
   - Methodology / Framework sections
   - Reference tables (at least 8-12 categories)
   - Anti-patterns / Pitfalls (if applicable)
   - When to use / When not to use

2. Present to the user:
   - **Summary**: Total references collected per category
   - **Proposed sections**: List of sections for the SKILL.md
   - **Estimated size**: How many lines the skill will be

3. Ask: *"I collected ~N references across K categories. The proposed skill has M sections and will be approximately L lines. Shall I proceed with writing?"*

**Wait for user approval before Phase 4.**

---

## Phase 4: Writing & Integration

### 4a. Write the SKILL.md

Place the file at `skills/<skill-name>/SKILL.md`.

Follow these conventions:
- YAML frontmatter: name, description, license (MIT), compatibility (opencode), metadata (audience, workflow, source, standard, year, approach)
- Use **plain markdown only** — NO JSX/HTML components (`<Tabs>`, `<Note>`, `<Warning>`, etc.)
- Use markdown tables for structured data
- Use fenced code blocks for commands/configs
- Use blockquotes for callouts
- Frontmatter must match this template:
  ```yaml
  ---
  name: skill-name-kebab
  description: One-line description (max 160 chars)
  license: MIT
  compatibility: opencode
  metadata:
    audience: target-audience
    workflow: relevant-workflow
    source: primary-source-standard
  ---
  ```

For reference sections, use consistent table format:
```markdown
| Nama | Penerbit | Deskripsi | Link |
|------|----------|-----------|------|
```

### 4b. Run sync

```bash
node scripts/sync-skills.js
```

### 4c. Update README.md (if new skill)

If creating a new skill (not extending existing), update README.md:
- Add the skill to the appropriate category table (Red Team / Blue Team / General)

### 4d. Commit

```bash
git add skills/<skill-name>/SKILL.md manifest.json skills/index.json README.md .claude-plugin/ .cursor-plugin/
git commit -m "docs: add <skill-name> skill with <N>+ references"
```

Use `docs:` prefix (not `feat:`) for reference/skill additions.
Commit on branch `dev` (current branch).
Do NOT push.

### 4e. Report to user

Summarize what was created:
- Skill name and path
- Total references collected and categories
- Key sections included
- Commit hash
- Next steps (if any)
