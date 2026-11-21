# Active Directory Federation Services (AD FS)

> Status: stub, candidate sources listed but not yet verified. Priority: P1 (start here). Last verified: not yet verified.

## What it is

AD FS issues tokens for federated apps. Token-signing abuse (for example Golden SAML) is high impact and only visible if AD FS auditing is on.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| AD FS sign-ins via Connect Health | ADFSSignInLogs | Microsoft Entra ID (diagnostic settings) | To verify | To verify | To verify |
| AD FS auditing on the servers | `SecurityEvent` | Windows Security Events via AMA | To verify | To verify | To verify |
| Defender for Identity on AD FS | `IdentityLogonEvents` | Defender XDR | To verify | To verify | To verify |

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

- Requires AD FS auditing enabled (Basic or Verbose) plus object access auditing.
- Plan for organisations migrating off AD FS to Entra ID; keep logging until the farm is gone.

## Official links

- [ADFSSignInLogs table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/adfssigninlogs)
- [AD FS troubleshooting: auditing and logging](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/troubleshooting/ad-fs-tshoot-logging)
- [Windows Security Events via AMA connector](https://learn.microsoft.com/en-us/azure/sentinel/data-connectors/windows-security-events-via-ama)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
