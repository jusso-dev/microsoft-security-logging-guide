# Active Directory Domain Services (on-premises)

> Status: stub, candidate sources listed but not yet verified. Priority: P1 (start here). Last verified: not yet verified.

## What it is

Domain controller security events are still the primary record of on-premises identity attacks such as Kerberoasting, DCSync and privileged group changes.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Domain controller security events | `SecurityEvent` | Windows Security Events via AMA | To verify | To verify | To verify |
| Event set selection | `SecurityEvent` (Common or All) | Data collection rule | To verify | To verify | To verify |
| Defender for Identity view | `IdentityDirectoryEvents`, `IdentityLogonEvents` | Defender XDR | To verify | To verify | To verify |

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

- Map to the ASD priority list event IDs (for example 4624, 4625, 4662, 4720, 4728, 4732, 4756, 4768, 4769, 4771, 4776, 5136, 1102) and say which DCR event set or XPath gets them.
- Advanced audit policy must be configured by GPO or the events never exist.

## Official links

- [Windows Security Events via AMA connector](https://learn.microsoft.com/en-us/azure/sentinel/data-connectors/windows-security-events-via-ama)
- [Windows security event sets that can be sent to Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/windows-security-event-id-reference)
- [Audit policy recommendations for AD DS](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/audit-policy-recommendations)
- [Azure Monitor Agent overview](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-overview)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
