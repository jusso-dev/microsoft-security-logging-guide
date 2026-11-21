# Windows Server

> Status: stub, candidate sources listed but not yet verified. Priority: P2. Last verified: not yet verified.

## What it is

Member servers outside the domain controller tier: security events, PowerShell, Sysmon and Defender for Servers telemetry.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Security log | `SecurityEvent` | Windows Security Events via AMA | To verify | To verify | To verify |
| Other channels | Event / `WindowsEvent` | AMA custom DCR | To verify | To verify | To verify |
| Defender for Servers | Device* tables | Defender XDR | To verify | To verify | To verify |

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

- Cover Azure Arc for on-premises and other-cloud servers.

## Official links

- [Windows Security Events via AMA connector](https://learn.microsoft.com/en-us/azure/sentinel/data-connectors/windows-security-events-via-ama)
- [Windows security event sets that can be sent to Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/windows-security-event-id-reference)
- [Azure Monitor Agent overview](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-overview)
- [Defender for Servers overview](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-servers-overview)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
