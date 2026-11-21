# DevOps

Source control, CI/CD pipelines, PATs and supply-chain security for GitHub Enterprise Cloud and Azure DevOps.

## What are you trying to do?

| I'm trying to... | Do this |
|---|---|
| **Catch private-to-public repo flips, PAT/SSH key additions, branch protection bypasses or secret-scanning alerts in GitHub** | Open [GitHub (Enterprise Cloud)](github/README.md) (`GitHubAuditLogsV3_CL` or `GitHubAuditLogsV2_CL`, `GitHubAdvancedSecurityAlerts_CL`). |
| **Catch PAT misuse, rogue build agents, service connection hijacking or audit tampering in Azure DevOps** | Open [Azure DevOps](azure-devops/README.md) (`ADOAuditLogs_CL` or `AzureDevOpsAuditing`). |
| **Check if all DevOps tables are landing** | Run [devops.kql](../queries/validation/devops.kql). |

## Guides in this group

| Guide | Priority | Primary tables | Default tier | Status |
|---|---|---|---|---|
| [GitHub (Enterprise Cloud)](github/README.md) | P2 | `GitHubAuditLogsV3_CL` (or `GitHubAuditLogsV2_CL`), `GitHubAdvancedSecurityAlerts_CL`, `SecurityAlert` (free) | Analytics (filter/lake noisy `git.*` events) | Verified |
| [Azure DevOps](azure-devops/README.md) | P3 | `ADOAuditLogs_CL` (or `AzureDevOpsAuditing`), `SecurityAlert` (free) | Analytics | Verified |
