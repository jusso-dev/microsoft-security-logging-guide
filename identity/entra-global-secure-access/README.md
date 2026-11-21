# Microsoft Entra Internet Access and Private Access (Global Secure Access)

> Status: stub, candidate sources listed but not yet verified. Priority: P3. Last verified: not yet verified.

## What it is

Global Secure Access is Microsoft's security service edge. Its traffic logs show web and private app access through the Entra client and remote networks.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Traffic logs | `NetworkAccessTraffic` | Microsoft Entra ID (diagnostic settings) | To verify | To verify | To verify |
| Remote network health | `RemoteNetworkHealthLogs` | Microsoft Entra ID (diagnostic settings) | To verify | To verify | To verify |

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

- Traffic logs are high volume. Assess data lake tier.

## Official links

- [View Global Secure Access traffic logs](https://learn.microsoft.com/en-us/entra/global-secure-access/how-to-view-traffic-logs)
- [Connect Microsoft Entra ID to Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/connect-azure-active-directory)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
