# Windows security event logs (clients)

> Status: stub, candidate sources listed but not yet verified. Priority: P1 (start here). Last verified: not yet verified.

## What it is

Native Windows event logs, collected with the Azure Monitor Agent or Windows Event Forwarding, for devices where you need events that Defender for Endpoint doesn't record.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Security log | `SecurityEvent` | Windows Security Events via AMA | To verify | To verify | To verify |
| Forwarded events | `WindowsEvent` | Windows Forwarded Events | To verify | To verify | To verify |
| Other channels (PowerShell, Sysmon, AppLocker) | Event / `WindowsEvent` | AMA with custom DCR XPath | To verify | To verify | To verify |

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

- Overlaps heavily with Defender for Endpoint. Be explicit about which events are worth paying for twice.
- Include sample DCR XPath queries for PowerShell 4104, Sysmon and AppLocker.

## Official links

- [Windows Security Events via AMA connector](https://learn.microsoft.com/en-us/azure/sentinel/data-connectors/windows-security-events-via-ama)
- [Windows security event sets that can be sent to Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/windows-security-event-id-reference)
- [Windows Forwarded Events connector](https://learn.microsoft.com/en-us/azure/sentinel/data-connectors/windows-forwarded-events)
- [Azure Monitor Agent overview](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-overview)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
