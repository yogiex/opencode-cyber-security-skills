# cyber-security Agent Skills

This repository contains a collection of agent skills for cyber-security. These skills are designed to enhance the capabilities of agents by providing them with specialized functionalities.

## What are Agent Skills?

Agent Skills are folders of instructions, scripts, and resources that agents can discover and use to do things more accurately and efficiently. They work across any AI agent that supports the [open Agent Skills standard](https://agentskills.io).

## Available Skills

<!-- START:Available-Skills -->

| Skill                                                           | Description                                                                                                                                                                                                                                              |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [incident-response-plan](./skills/incident-response-plan)       | Panduan incident response non-teknis untuk organisasi: persiapan, deteksi, analisis, containment, eradikasi, recovery, dan pembelajaran. Cocok untuk tim manajemen, legal, PR, dan koordinator insiden.                                                  |
| [owasp-top10-2025](./skills/owasp-top10-2025)                   | Complete reference for OWASP Top 10 2025 web application security risks. Use when discussing web app security, vulnerability assessments, or when user asks about OWASP, A01-A10, or specific risks like broken access control or supply chain failures. |
| [ptes-standard](./skills/ptes-standard)                         | Penetration Testing Execution Standard (PTES) - comprehensive guide for conducting penetration tests, from pre-engagement to reporting.                                                                                                                  |
| [risk-management-framework](./skills/risk-management-framework) | Panduan NIST Risk Management Framework (SP 800-37) untuk mengelola risiko keamanan dan privasi secara terstruktur, fleksibel, dan berkelanjutan di seluruh siklus hidup sistem.                                                                          |
| [threat-modeling](./skills/threat-modeling)                     | Identifikasi ancaman pada desain sistem menggunakan STRIDE, DFD, dan prioritisasi risiko. Cocok untuk arsitek keamanan, developer lead, dan product manager.                                                                                             |
| [web-reconnaissance](./skills/web-reconnaissance)               | Reconnaissance pada web app: chunk file, network tab, API endpoint mapping, localstorage/token/session, identifikasi teknologi. Cocok untuk security analyst dan penetration tester.                                                                     |

<!-- END:Available-Skills -->

## Installation

### Skills

Use [skills](https://skills.sh/) to install skills directly:

```bash
# Install all skills
npx skills add cyber-security/agent-skills

# Install specific skills
npx skills add cyber-security/agent-skills --skill owasp-top10-2025

# List available skills
npx skills add cyber-security/agent-skills --list
```

### Claude Code Plugin

Install via Claude Code's plugin system:

```bash
# Add the plugin (includes all skills)
/plugin add cyber-security/agent-skills
```

> Claude Code plugins are also supported in Factory's [Droid](https://docs.factory.ai/cli/configuration/plugins#claude-code-compatibility).

### Other Installation Methods

Agent skills can also be installed by using the below commands from [Playbooks](https://playbooks.com/skills) or [Context7](https://context7.com/docs/skills):

```bash
# Playbooks
npx playbooks add skill cyber-security/agent-skills

# Context7
npx ctx7 skills install /cyber-security/agent-skills
```

## Adding New Skills

Use the included script to add new skills:

```bash
node scripts/add-skill.js <skill-name> "<description>"
```

Example:

```bash
node scripts/add-skill.js owasp-top10-2025 "OWASP Top 10 2025 vulnerability knowledge and guidance. Use when discussing web app security, vulnerability assessments, or when user asks about OWASP, A01-A10, or specific risks like broken access control or supply chain failures."
```

This will create the skill structure and automatically update manifest.json, platform plugin files, skills/index.json, and this README.

## Scripts

| Script                        | Description                                                                                    |
| ----------------------------- | ---------------------------------------------------------------------------------------------- |
| `node scripts/add-skill.js`   | Add a new skill to the repository                                                              |
| `node scripts/sync-skills.js` | Sync manifest.json, platform plugin files, skills/index.json, and README with skills directory |

## Resources

- [Agent Skills Specification](https://agentskills.io/specification)
- [npx skills](https://skills.sh/)
- [Validate Agent Skill](https://github.com/marketplace/actions/validate-skill)
- [Playbooks](https://playbooks.com/skills)
- [Context7 Skills](https://context7.com/docs/skills)

## Contributing

Contributions are welcome! Please read our [Contributing Guide](.github/CONTRIBUTING.md) for more information.

## License

MIT
