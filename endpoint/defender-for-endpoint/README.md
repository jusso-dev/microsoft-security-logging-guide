# Microsoft Defender for Endpoint

> Status: stub, candidate sources listed but not yet verified. Priority: P1 (start here). Last verified: not yet verified.

## What it is

Defender for Endpoint is the EDR for Windows, macOS, Linux, iOS and Android. Its device tables are the richest endpoint telemetry available.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Process creation | `DeviceProcessEvents` | Defender XDR | To verify | To verify | To verify |
| Network connections | `DeviceNetworkEvents` | Defender XDR | To verify | To verify | To verify |
| File events | `DeviceFileEvents` | Defender XDR | To verify | To verify | To verify |
| Registry | `DeviceRegistryEvents` | Defender XDR | To verify | To verify | To verify |
| Logons | `DeviceLogonEvents` | Defender XDR | To verify | To verify | To verify |
| Image loads | `DeviceImageLoadEvents` | Defender XDR | To verify | To verify | To verify |
| Miscellaneous events (ASR, exploit protection, etc.) | `DeviceEvents` | Defender XDR | To verify | To verify | To verify |
| Device inventory | `DeviceInfo`, `DeviceNetworkInfo` | Defender XDR | To verify | To verify | To verify |
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

- Device tables are free to query in advanced hunting for 30 days. Streaming them into Sentinel analytics is the biggest single cost decision. Document the trade-off and point to docs/defender-xdr-vs-sentinel.md.

## Official links

- [Connect Microsoft Defender XDR to Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/connect-microsoft-365-defender)
- [Advanced hunting schema tables](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-schema-tables)
- [Microsoft Defender for Endpoint documentation](https://learn.microsoft.com/en-us/defender-endpoint/)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
