# Microsoft Copilot Studio

> Status: stub, candidate sources listed but not yet verified. Priority: P2. Last verified: not yet verified.

## What it is

Copilot Studio is where makers build agents. Agent creation, authentication changes, publishing and sharing are the events security teams need.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Copilot and agent interactions | `CopilotActivity` | Microsoft Copilot solution | To verify | To verify | To verify |
| Agent definitions via Dataverse bot table | `DataverseActivity` | Microsoft Dataverse | To verify | To verify | To verify |
| Agent inventory and risk (Agent 365) | `AgentsInfo` | Defender XDR | To verify | To verify | To verify |

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

- Copilot Studio maker admin events (BotCreate, BotUpdateOperation-*) are documented in Purview but not in a documented Sentinel table. Re-check each review.
- Defender agent inventory and runtime protection need a Microsoft Agent 365 licence from 1 Jul 2026.

## Official links

- [Configure data policies for Copilot Studio agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention)
- [Audit logs for Copilot and AI applications](https://learn.microsoft.com/en-us/purview/audit-copilot)
- [CopilotActivity table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/copilotactivity)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
