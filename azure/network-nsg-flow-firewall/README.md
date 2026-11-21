# Azure networking (VNet flow logs, Azure Firewall, WAF, DNS)

> Status: stub, candidate sources listed but not yet verified. Priority: P2. Last verified: not yet verified.

## What it is

Network telemetry for Azure: flow logs, Azure Firewall rule and threat intel hits, WAF logs and DNS queries.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| VNet flow logs (traffic analytics) | `NTANetAnalytics` | Network Watcher | To verify | To verify | To verify |
| Azure Firewall | `AZFWNetworkRule`, `AZFWApplicationRule`, `AZFWThreatIntel`, `AZFWIdpsSignature`, `AZFWDnsQuery` | Azure Firewall (diagnostic settings) | To verify | To verify | To verify |
| Application Gateway WAF | `AGWFirewallLogs`, `AGWAccessLogs` | Application Gateway (diagnostic settings) | To verify | To verify | To verify |
| DNS security policy | `DNSQueryLogs` | DNS security policy (diagnostic settings) | To verify | To verify | To verify |

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

- NSG flow logs are being retired in favour of VNet flow logs. Document dates and migration.
- Flow and firewall logs are the classic data lake tier candidates. Keep threat intel and IDPS hits in analytics.

## Official links

- [VNet flow logs overview](https://learn.microsoft.com/en-us/azure/network-watcher/vnet-flow-logs-overview)
- [NSG flow logs overview and retirement](https://learn.microsoft.com/en-us/azure/network-watcher/nsg-flow-logs-overview)
- [Monitor Azure Firewall](https://learn.microsoft.com/en-us/azure/firewall/monitor-firewall)
- [Connect Sentinel to Azure services using diagnostic settings](https://learn.microsoft.com/en-us/azure/sentinel/connect-services-diagnostic-setting-based)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
