# Microsoft Purview Data Loss Prevention

> Status: stub, candidate sources listed but not yet verified. Priority: P2. Last verified: not yet verified.

## What it is

Purview DLP detects and blocks sensitive data leaving through email, SharePoint, endpoints, Teams and more.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| DLP alerts (only if the built-in tuning rule is off) | `AlertInfo`, `AlertEvidence` | Defender XDR | To verify | To verify | To verify |
| DLP signals as behaviours (default since Oct 2026) | `BehaviorInfo`, `BehaviorEntities` | Defender XDR | To verify | To verify | To verify |
| DLP rule matches in audit | `CloudAppEvents` / `OfficeActivity` | Defender XDR / Microsoft 365 | To verify | To verify | To verify |
| Endpoint DLP | `DeviceEvents` | Defender XDR | To verify | To verify | To verify |

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

- Since early October 2026 a built-in Defender XDR alert tuning rule turns DLP signals into behaviours (`BehaviorInfo`, `BehaviorEntities`) instead of alerts, so they no longer create incidents unless you turn the rule off. Document the choice.
- Confirm which DLP events are only in the audit log.

## Official links

- [Learn about data loss prevention](https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp)
- [Investigate data loss alerts with Microsoft Defender XDR](https://learn.microsoft.com/en-us/defender-xdr/dlp-investigate-alerts-defender)
- [Connect Microsoft Defender XDR to Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/connect-microsoft-365-defender)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
