# Exchange Online

> Status: stub, candidate sources listed but not yet verified. Priority: P1 (start here). Last verified: not yet verified.

## What it is

Exchange Online audit covers mailbox access, inbox rules, forwarding and admin changes, which are core to business email compromise detection.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Admin and mailbox audit | `OfficeActivity` (`OfficeWorkload` == "Exchange") | Microsoft 365 (Office 365) | To verify | To verify | To verify |
| Cloud app view | `CloudAppEvents` | Defender XDR | To verify | To verify | To verify |
| Mail flow | `EmailEvents` | Defender XDR (needs Defender for Office 365) | To verify | To verify | To verify |

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

- MailItemsAccessed needs Audit (Premium) or the expanded logging Microsoft rolled out to more licences. Record the current licence position.
- Inbox rule creation and forwarding changes are must-have detections.

## Official links

- [Microsoft 365 (Office 365) connector](https://learn.microsoft.com/en-us/azure/sentinel/data-connectors/microsoft-365)
- [OfficeActivity table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/officeactivity)
- [Microsoft Purview auditing solutions](https://learn.microsoft.com/en-us/purview/audit-solutions-overview)
- [Manage mailbox auditing](https://learn.microsoft.com/en-us/purview/audit-mailboxes)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
