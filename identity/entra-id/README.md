# Microsoft Entra ID (sign-in, audit and Graph activity logs)

> Status: stub, candidate sources listed but not yet verified. Priority: P1 (start here). Last verified: not yet verified.

## What it is

Microsoft Entra ID is the identity provider for Microsoft 365, Azure and most SaaS. Its sign-in and audit logs are the backbone of almost every identity detection.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Interactive user sign-ins | `SigninLogs` | Microsoft Entra ID | To verify | To verify | To verify |
| Non-interactive user sign-ins | `AADNonInteractiveUserSignInLogs` | Microsoft Entra ID | To verify | To verify | To verify |
| Service principal sign-ins | `AADServicePrincipalSignInLogs` | Microsoft Entra ID | To verify | To verify | To verify |
| Managed identity sign-ins | `AADManagedIdentitySignInLogs` | Microsoft Entra ID | To verify | To verify | To verify |
| Directory audit | `AuditLogs` | Microsoft Entra ID | To verify | To verify | To verify |
| Provisioning | `AADProvisioningLogs` | Microsoft Entra ID | To verify | To verify | To verify |
| Microsoft Graph activity | `MicrosoftGraphActivityLogs` | Microsoft Entra ID (diagnostic settings) | To verify | To verify | To verify |
| Defender XDR sign-in view | `EntraIdSignInEvents`, `EntraIdSpnSignInEvents` | Defender XDR (advanced hunting) | To verify | To verify | To verify |

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

- `AADSignInEventsBeta` and `AADSpnSignInEventsBeta` were replaced by `EntraIdSignInEvents` and `EntraIdSpnSignInEvents` in Defender XDR. Update any queries stored outside Defender.
- Non-interactive and service principal sign-ins are high volume but carry token replay and app abuse signal. Decide their tier deliberately rather than leaving them out.
- Some tables need Entra ID P1 or P2. Record which.

## Official links

- [Connect Microsoft Entra ID to Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/connect-azure-active-directory)
- [Integrate Entra activity logs with Azure Monitor logs](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-integrate-activity-logs-with-azure-monitor-logs)
- [Zero Trust workshop: integrate all Entra logs into SIEM](https://microsoft.github.io/zerotrustassessment/docs/workshop-guidance/identity/RMI_074)
- [Microsoft Graph activity logs](https://learn.microsoft.com/en-us/graph/microsoft-graph-activity-logs-overview)
- [EntraIdSignInEvents table (Defender XDR)](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-entraidsigninevents-table)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
