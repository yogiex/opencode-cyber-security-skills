---
name: "Incident Communication Templates"
description: "Templates for breach notification, executive briefing, stakeholder update, and regulatory notification during incident response."
tags: [communication, templates, breach-notification, executive-briefing]
---

# Incident Communication Templates

## Executive Briefing Template

```
TO: [Executive Team]
FROM: [IR Lead]
SUBJECT: [SEVERITY] Security Incident — [INCIDENT NAME]
DATE: [TIMESTAMP]

### Situation Overview
[One paragraph — what happened, when, systems affected]

### Current Status
- Containment: [COMPLETED / IN PROGRESS / PENDING]
- Systems affected: [LIST]
- Data compromised: [TYPE / VOLUME]
- Attacker activity: [STOPPED / ONGOING / UNKNOWN]

### Actions Taken
[Bullet list of containment actions with timestamps]

### Recommended Next Steps
[3-5 bullet points]

### Communication Cadence
- Next update: [TIME]
- Channel: [EMAIL / SLACK / MEETING]
- Contact: [IR LEAD NAME / PHONE]
```

## Internal Incident Notification

```
INCIDENT NOTIFICATION — DO NOT FORWARD

Classification: [INTERNAL / CONFIDENTIAL]
Incident ID: IR-2026-[XXX]
Severity: [CRITICAL / HIGH / MEDIUM]
Reported: [DATE] [TIME] [TZ]
Detected via: [SIEM / EDR / USER REPORT]
IR Lead: [NAME]

### Affected Systems
[List of hostnames, IPs, services]

### Actions Required
- [TEAM A]: [ACTION]
- [TEAM B]: [ACTION]
- ALL: [ACTION, e.g., "Report any unusual activity"]

### Point of Contact
- IR Team Channel: [#incident-response]
- Escalation: [NAME / PHONE]
```

## Stakeholder Update Template

```
STATUS UPDATE #[N] — [INCIDENT NAME]

Date: [DATE]
Time: [TIME]
Prepared by: [NAME]

### What We Know
[Bullet points of confirmed facts]

### What We're Doing
[Actions in progress]

### What We Need
[Resources, decisions, approvals needed]

### Next Update
[SCHEDULED TIME or "Upon significant change"]
```

## Regulatory Notification Checklist

```
### GDPR Breach Notification (72h)
- [ ] Identify supervisory authority
- [ ] Describe nature of breach (categories + approx count of data subjects)
- [ ] Provide contact details of DPO
- [ ] Describe likely consequences
- [ ] Describe measures taken/proposed
- [ ] Document breach internally
- [ ] Submit via authority's designated channel

### HIPAA Breach Notification
- [ ] Notify affected individuals within 60 days
- [ ] Notify HHS (if 500+ individuals)
- [ ] Notify media (if 500+ individuals in state/jurisdiction)
- [ ] Document breach investigation
- [ ] Conduct risk assessment

### SEC Material Incident Notification (4 days)
- [ ] Assess materiality
- [ ] Prepare 8-K filing
- [ ] Coordinate with legal counsel
- [ ] Board notification
```
