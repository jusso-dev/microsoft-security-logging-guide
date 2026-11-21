# Microsoft Dataverse and Dynamics 365

> Status: stub, candidate sources listed but not yet verified. Priority: P2. Last verified: not yet verified.

## What it is

Dataverse stores data for Power Apps and Dynamics 365 Customer Engagement. Its audit stream shows exports, mass reads, role changes and audit tampering.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Dataverse audit | `DataverseActivity` | Microsoft Dataverse (Business Applications solution) | To verify | To verify | To verify |
| Legacy (migrate away) | `Dynamics365Activity` | Dynamics 365 (legacy) | To verify | To verify | To verify |
| Finance and Operations | `FinanceOperationsActivity_CL` (verify) | Dynamics 365 Finance and Operations | To verify | To verify | To verify |

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

- Detailed content currently sits in business-apps/power-platform. Split it out here.
- DataverseActivity replaces Dynamics365Activity. Don't run both.

## Official links

- [Microsoft Sentinel solution for Microsoft Business Apps](https://learn.microsoft.com/en-us/azure/sentinel/business-applications/solution-overview)
- [Manage Dataverse auditing](https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing)
- [DataverseActivity table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/dataverseactivity)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
