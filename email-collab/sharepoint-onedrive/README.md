# SharePoint Online and OneDrive

> Status: stub, candidate sources listed but not yet verified. Priority: P2. Last verified: not yet verified.

## What it is

File access, sharing and download activity in SharePoint and OneDrive, the main places data leaves a Microsoft 365 tenant.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| File and sharing activity | `OfficeActivity` (`OfficeWorkload` in ("`SharePoint`","`OneDrive`")) | Microsoft 365 (Office 365) | To verify | To verify | To verify |
| Cloud app view | `CloudAppEvents` | Defender XDR | To verify | To verify | To verify |

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

- FileAccessed is very high volume. Keep sharing and anonymous link events in the Analytics tier and consider filtering the rest.

## Official links

- [Microsoft 365 (Office 365) connector](https://learn.microsoft.com/en-us/azure/sentinel/data-connectors/microsoft-365)
- [OfficeActivity table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/officeactivity)
- [Microsoft Purview auditing solutions](https://learn.microsoft.com/en-us/purview/audit-solutions-overview)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
