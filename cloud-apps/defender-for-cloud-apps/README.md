# Microsoft Defender for Cloud Apps

> Status: stub, candidate sources listed but not yet verified. Priority: P2. Last verified: not yet verified.

## What it is

Defender for Cloud Apps is the CASB. It normalises activity from Microsoft 365 and connected SaaS apps and reports shadow IT from discovery logs.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| SaaS activity | `CloudAppEvents` | Defender XDR | To verify | To verify | To verify |
| Shadow IT discovery | `McasShadowItReporting` | Microsoft Defender for Cloud Apps | To verify | To verify | To verify |
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

- CloudAppEvents overlaps with OfficeActivity. Document which to use for which workload.

## Official links

- [Integrate Defender for Cloud Apps with Microsoft Sentinel](https://learn.microsoft.com/en-us/defender-cloud-apps/siem-sentinel)
- [CloudAppEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-cloudappevents-table)
- [Connect Microsoft Defender XDR to Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/connect-microsoft-365-defender)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
