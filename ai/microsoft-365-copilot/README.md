# Microsoft 365 Copilot

> Status: stub, candidate sources listed but not yet verified. Priority: P2. Last verified: not yet verified.

## What it is

Microsoft 365 Copilot interactions, plugin changes and settings, including prompts that reference sensitive files.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Copilot interactions | `CopilotActivity` | Microsoft Copilot solution | To verify | To verify | To verify |
| Audit view | `CloudAppEvents` | Defender XDR | To verify | To verify | To verify |

The rows above are a starting list for contributors. Table names, connectors and tiers must be checked against Microsoft Learn before this guide is marked verified.

## Prerequisites and licensing

To do. Licences, audit settings that must be on, and roles needed to connect.

## Step-by-step setup

To do. Numbered steps from a clean tenant to data landing, using current Defender portal navigation.

## Architecture diagram

To do. A Mermaid `flowchart` from the product to its tables, showing the connector or agent and the tier.

## Validation KQL

To do. Queries that prove each table is landing, how fresh it is, and how many GB a day it costs.

## Out-of-box analytic rules

To do. Rule name, what it detects, tables used, MITRE tactics and whether to enable on day 1. Link the Content Hub solution.

## Custom detections

To do. Gaps the out-of-box content misses, as KQL with assumptions marked.

## Playbooks

To do. Included and suggested response playbooks, with connectors and permissions.

## Workbooks and hunting

To do.

## Gotchas and deprecations

- `LLMActivity` was renamed `CopilotActivity` in December 2025.

## Official links

- [Audit logs for Copilot and AI applications](https://learn.microsoft.com/en-us/purview/audit-copilot)
- [CopilotActivity table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/copilotactivity)
- [Microsoft Copilot solution (GitHub)](https://github.com/Azure/Azure-Sentinel/tree/master/Solutions/Microsoft%20Copilot)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
