# Microsoft Teams

> Status: stub, candidate sources listed but not yet verified. Priority: P2. Last verified: not yet verified.

## What it is

Teams activity covers external access, guest access, app installs and meeting events. Teams is now a phishing channel in its own right.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Teams activity | `OfficeActivity` (`OfficeWorkload` == "`MicrosoftTeams`") | Microsoft 365 (Office 365) | To verify | To verify | To verify |
| Cloud app view | `CloudAppEvents` | Defender XDR | To verify | To verify | To verify |
| Teams message security (if licensed) | `MessageEvents`, `MessagePostDeliveryEvents`, `MessageUrlInfo` | Defender XDR | To verify | To verify | To verify |

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

- Verify the current state of the Teams message tables in Defender XDR before documenting them.

## Official links

- [Microsoft 365 (Office 365) connector](https://learn.microsoft.com/en-us/azure/sentinel/data-connectors/microsoft-365)
- [OfficeActivity table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/officeactivity)
- [Advanced hunting schema tables](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-schema-tables)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
