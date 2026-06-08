---
name: "Modern Infrastructure Adaptations — Cloud, K8s, APIs"
description: "PTES adaptations for cloud (AWS/Azure/GCP), containers/Kubernetes, and API/microservices environments covering phase-by-phase methodology adjustments, cloud-specific tools, attack primitives, and container escape paths."
tags: [ptes, cloud, kubernetes, containers, api, microservices, aws, azure, gcp]
---

# Modern Infrastructure Adaptations

## Cloud (AWS / Azure / GCP)

| Phase | Cloud Adaptation |
|-------|-----------------|
| Pre-engagement | Include CSP account IDs, subscriptions; confirm CSP pentest policy |
| Intelligence | Enumerate S3/Blob/GCS buckets, IAM roles, CloudFront, cert transparency |
| Threat Modeling | IAM trust relationships, cross-account access, federation attacks |
| Vulnerability | ScoutSuite, Prowler, CloudFox, CIS benchmarks |
| Exploitation | IAM privesc, SSRF → metadata service, role chaining |
| Post-Exploitation | Cross-account movement, managed identity abuse, vault secrets |

**Cloud-specific tools:** Pacu (AWS), AzureHound (Azure), Prowler (multi), ScoutSuite (multi), CloudFox.

**Key attack primitives:** IMDSv1 abuse via SSRF, AzureHound Contributor → Managed Identity → Key Vault, GCP default Compute Engine service account with Editor role, K8s exposed API server.

## Containers / Kubernetes

| Phase | K8s Focus |
|-------|-----------|
| Pre-engagement | Cluster API endpoint, pod security policies, network policies |
| Intelligence | Registry scanning, K8s dashboard exposure, kubeconfig leaks |
| Threat Modeling | Container escape paths, cluster-admin abuse, supply chain |
| Vulnerability | Trivy/Grype for images, kube-bench, kube-hunter |
| Exploitation | `kubectl exec` abuse, hostPath mount escape, runC escape |
| Post-Exploitation | Service account token harvesting, cluster-to-cloud pivot |
| Reporting | Image CVEs, RBAC misconfigurations, namespace isolation gaps |

## APIs / Microservices

| Phase | API Focus |
|-------|-----------|
| Pre-engagement | Endpoint inventory, auth mechanism (JWT, OAuth2, API keys) |
| Intelligence | API doc discovery (Swagger/Slate), GraphQL introspection |
| Threat Modeling | BOLA/IDOR, BFLA, mass assignment, JWT algorithm confusion |
| Vulnerability | 403 bypass, parameter pollution, rate limiting |
| Exploitation | OAuth token theft, JWT none algorithm, GraphQL depth abuse |
| Post-Exploitation | Internal API discovery, service mesh abuse, config server access |
| Reporting | OWASP API Top 10 mapping, rate-limiting gaps, authz failures |

## Best Practices

- CSP pentest policies: AWS allows most services without pre-approval, Azure/GCP similar
- For K8s: always check RBAC bindings and network policies first
- API testing: prioritize BOLA/IDOR — most common API vulnerability
- Cloud: identity is the new perimeter — focus on IAM trust relationships
