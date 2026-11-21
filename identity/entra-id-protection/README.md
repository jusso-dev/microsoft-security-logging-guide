# Microsoft Entra ID Protection (risk detections)

> Status: stub, candidate sources listed but not yet verified. Priority: P1 (start here). Last verified: not yet verified.

## What it is

Entra ID Protection scores user and workload identity risk. Its risk events feed Conditional Access and are high-signal alerts in their own right.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Risky users | `AADRiskyUsers` | Microsoft Entra ID | To verify | To verify | To verify |
| User risk events | `AADUserRiskEvents` | Microsoft Entra ID | To verify | To verify | To verify |
| Risky service principals | `AADRiskyServicePrincipals` | Microsoft Entra ID | To verify | To verify | To verify |
| Service principal risk events | `AADServicePrincipalRiskEvents` | Microsoft Entra ID | To verify | To verify | To verify |
| Alerts | `SecurityAlert`, `AlertInfo`, `AlertEvidence` | Defender XDR | To verify | To verify | To verify |

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

- Needs Entra ID P2 for full risk detail.
- Alerts arrive through the Defender XDR connector. Avoid also enabling the standalone alert connector and creating duplicate incidents.

## Official links

- [Export risk data](https://learn.microsoft.com/en-us/entra/id-protection/howto-export-risk-data)
- [Connect Microsoft Entra ID to Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/connect-azure-active-directory)
- [Connect Microsoft Defender XDR to Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/connect-microsoft-365-defender)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
