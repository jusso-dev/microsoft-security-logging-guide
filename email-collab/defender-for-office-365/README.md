# Microsoft Defender for Office 365

> Status: stub, candidate sources listed but not yet verified. Priority: P1 (start here). Last verified: not yet verified.

## What it is

Defender for Office 365 adds email threat protection, Safe Links and Safe Attachments, and the email tables in advanced hunting.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Email delivery | `EmailEvents` | Defender XDR | To verify | To verify | To verify |
| Attachments | `EmailAttachmentInfo` | Defender XDR | To verify | To verify | To verify |
| URLs in email | `EmailUrlInfo` | Defender XDR | To verify | To verify | To verify |
| Post-delivery actions (ZAP etc.) | `EmailPostDeliveryEvents` | Defender XDR | To verify | To verify | To verify |
| Safe Links clicks | `UrlClickEvents` | Defender XDR | To verify | To verify | To verify |
| Alerts | `AlertInfo`, `AlertEvidence` | Defender XDR | To verify | To verify | To verify |

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

- Email tables can be large in big tenants. Consider data lake tier for EmailUrlInfo and EmailAttachmentInfo if only used for hunting.

## Official links

- [Connect Microsoft Defender XDR to Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/connect-microsoft-365-defender)
- [EmailEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-emailevents-table)
- [Advanced hunting schema tables](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-schema-tables)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
