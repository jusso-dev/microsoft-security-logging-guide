# Azure Activity (control plane)

> Status: stub, candidate sources listed but not yet verified. Priority: P1 (start here). Last verified: not yet verified.

## What it is

The Azure Activity log records every control plane write in a subscription: role assignments, resource deletes, policy changes and key operations.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Subscription activity | `AzureActivity` | Azure Activity (Azure Policy based) | To verify | To verify | To verify |

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

- AzureActivity is a free data source in Sentinel. There is no reason not to collect it from every subscription. Use Azure Policy to enforce it at management group scope.

## Official links

- [Azure Activity connector](https://learn.microsoft.com/en-us/azure/sentinel/data-connectors/azure-activity)
- [AzureActivity table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/azureactivity)
- [Connect Sentinel to Azure services using diagnostic settings](https://learn.microsoft.com/en-us/azure/sentinel/connect-services-diagnostic-setting-based)

## Last verified

Not yet verified. Set this to the date you checked every table name and link.
