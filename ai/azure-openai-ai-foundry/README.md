# Microsoft Foundry (formerly Azure AI Foundry) and Azure OpenAI

> Status: stub, candidate sources listed but not yet verified. Priority: P2. Last verified: not yet verified.

## What it is

Microsoft Foundry hosts models (including Azure OpenAI) and agents. Resource logs and Defender for AI alerts show key misuse, jailbreak attempts and abnormal usage.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Audit and request logs | `AzureDiagnostics` (Audit, `RequestResponse`, `AzureOpenAIRequestUsage`) | Diagnostic settings on the Foundry resource | To verify | To verify | To verify |
| Metrics | `AzureMetrics` | Diagnostic settings | To verify | To verify | To verify |
| Defender for AI services alerts | `SecurityAlert` | Defender for Cloud / Defender XDR | To verify | To verify | To verify |

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

- AI Services logs land in AzureDiagnostics, not resource-specific tables.
- Agent-level discovery and detection for Foundry agents needs Agent 365 from 1 Jul 2026.

## Official links

- [Enable diagnostic logging for Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/how-to/diagnostic-logging)
- [AI threat protection in Defender for Cloud](https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-threat-protection)
- [Connect Sentinel to Azure services using diagnostic settings](https://learn.microsoft.com/en-us/azure/sentinel/connect-services-diagnostic-setting-based)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
