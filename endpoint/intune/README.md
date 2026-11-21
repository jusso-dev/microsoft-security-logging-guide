# Microsoft Intune

> Status: stub, candidate sources listed but not yet verified. Priority: P2. Last verified: not yet verified.

## What it is

Intune manages device configuration and compliance. Its audit logs show who changed policies, wiped devices or pushed scripts, which attackers use for lateral movement.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Audit | `IntuneAuditLogs` | Intune diagnostic settings | To verify | To verify | To verify |
| Operational | `IntuneOperationalLogs` | Intune diagnostic settings | To verify | To verify | To verify |
| Device inventory | `IntuneDevices` | Intune diagnostic settings | To verify | To verify | To verify |
| Compliance | `IntuneDeviceComplianceOrg` | Intune diagnostic settings | To verify | To verify | To verify |

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

- Script deployment and remote wipe actions are the high-value events. Write detections for those first.

## Official links

- [Send Intune log data to Azure Monitor](https://learn.microsoft.com/en-us/intune/intune-service/fundamentals/review-logs-using-azure-monitor)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
