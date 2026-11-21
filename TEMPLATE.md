# Product name

> Status: stub | draft | verified. Priority: P1 | P2 | P3. Last verified: DD Mon YYYY.

## What it is

One or two plain sentences: what the product does and why its logs matter to a SOC.

## High-value log sources

| Source | Table name | Connector | Tier | Cost / volume | Value |
|---|---|---|---|---|---|
| Plain name of the log | `ExactTableName` | Connector name as shown in Content Hub | Analytics or data lake | Low, medium or high, with a GB/day hint if known | Why a SOC wants it |

Keep only sources with real detection or investigation value. Say if a table is free in Sentinel or already in Defender XDR advanced hunting.

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

- Retired tables, renamed tables, licence changes and anything that silently stops logging.

## Official links

- [Exact Microsoft Learn page title](https://learn.microsoft.com/...)

## Last verified

DD Mon YYYY, by @github-handle, against the links above.
