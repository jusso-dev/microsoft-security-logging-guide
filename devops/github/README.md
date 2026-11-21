# GitHub (Enterprise Cloud)

> Status: stub, candidate sources listed but not yet verified. Priority: P2. Last verified: not yet verified.

## What it is

GitHub audit logs show repository visibility changes, secret scanning bypasses, PAT and app grants, and branch protection changes.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Enterprise audit log | Verify current table (`GitHub` solution, CCF) | GitHub (Sentinel solution) | To verify | To verify | To verify |
| Advanced Security alerts | Verify | GitHub / Defender for Cloud DevOps security | To verify | To verify | To verify |

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

- Several GitHub connectors exist (webhook, audit log polling, streaming). Recommend one and say why.

## Official links

- [Stream the audit log for your enterprise](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/streaming-the-audit-log-for-your-enterprise)
- [GitHub solution for Microsoft Sentinel](https://github.com/Azure/Azure-Sentinel/tree/master/Solutions/GitHub)
- [Defender for Cloud DevOps security](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-devops-introduction)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
