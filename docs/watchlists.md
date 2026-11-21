# Watchlists and enrichment

Several detections in this repo only work with context from outside Microsoft: who just left the company, whose account matters enough to page someone at 3am, which subnets are corporate, which assets are crown jewels. Sentinel watchlists are the standard place for that context, and UEBA's `IdentityInfo` table covers the user half of it automatically. This page catalogues the watchlists the guides use and how to keep them current.

> Status: verified. Last verified: 21 Nov 2026.

## How watchlists work

Watchlists hold reference data in the workspace `Watchlist` table, cached for query speed, and are read in KQL with the `_GetWatchlist('alias')` function or listed with `_GetWatchlistAlias` ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/watchlists#watchlists-in-queries-for-searches-and-detection-rules)). Each watchlist defines one **SearchKey** column, which is the column rules join on, so pick the column your detections actually filter ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/watchlists-create)).

```kql
// Typical join shape: events plus a watchlist
SigninLogs
| where TimeGenerated > ago(1d)
| lookup kind=inner _GetWatchlist('vipusers') on $left.UserPrincipalName == $right.SearchKey
```

Limits that shape what belongs in a watchlist ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/watchlists#watchlist-limitations)):

| Limit | Value |
|---|---|
| Name and alias length | 3 to 64 characters |
| Total active items | 10 million per workspace |
| Local file upload | 3.8 MB |
| Azure Storage upload | 500 MB via a SAS URL (preview) |
| Underlying table retention | 28 days, refreshed roughly every 12 days |
| Use | Reference data only. Not for event-volume data |
| Azure Lighthouse | Cross-workspace watchlist management not supported |

Watchlists are reference data, not a log: if your list changes every few minutes, use a custom log table instead ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/watchlists#watchlist-limitations)).

## The built-in watchlist templates

Sentinel ships six watchlist templates with fixed schemas ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/watchlist-schemas)). Start from these rather than inventing your own shapes, because Content Hub content and this repo's guides expect them.

| Watchlist | Purpose | Key columns (mandatory) | Used by |
|---|---|---|---|
| Terminated Employees | Leavers, flagged before and after termination | `User Principal Name`, `UserState` (Notified or Terminated), `Termination date` | Power Platform departing-employee rules; Exchange and SharePoint exfil detections |
| VIP Users | High-impact accounts | `User Principal Name` | Dataverse privileged-login rules; generic VIP logon alerting |
| Network Addresses | Subnets with organisational context | `IP Subnet` | Geo and allow or block list rules; GSA traffic context |
| High Value Assets | Devices, subscriptions and resources with critical value | `Asset Type`, `Asset Id`, `Asset FQDN` | Prioritising alerts touching crown jewels |
| Identity Correlation | Maps a user to their privileged accounts | `User Principal Name`, `Associated Privileged Account` | Linking admin activity back to a person |
| Service Accounts | Service accounts and their owners | `Service Principal Name`, `Owner User Principal Name` | Anomalous service account activity triage |

The schemas, including the optional fields and the exact Tags quoting, are in Microsoft's [watchlist template schemas reference](https://learn.microsoft.com/en-us/azure/sentinel/watchlist-schemas).

The Business Applications solution adds its own: `TerminatedEmployees`, `VIPUsers`, `NetworkAddresses` and `MSBizApps-Configuration`, plus the `DataverseSharePointSites` watchlist. Microsoft's rules query them through the bundled parsers, `MSBizAppsTerminatedEmployees`, `MSBizAppsVIPUsers`, `MSBizAppsNetworkAddresses`, `MSBizAppsOrgSettings` and `DataverseSharePointSites`, rather than raw watchlist lookups. Use the parsers in your own rules too: they stay stable if Microsoft renames a watchlist ([Power Platform guide](../business-apps/power-platform/README.md)).

## UEBA IdentityInfo: the user enrichment you get for free

Before hand-maintaining user lists, enable [UEBA](https://learn.microsoft.com/en-us/azure/sentinel/enable-entity-behavior-analytics). UEBA synchronises user data from Microsoft Entra ID, and from on-premises Active Directory if you run Microsoft Defender for Identity, into the `IdentityInfo` table ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/ueba-reference)):

- Full resync every 14 days; profile, group and role changes land within 15 to 30 minutes, billed at normal ingestion rates.
- Default retention 30 days. `GroupMembership` covers up to 500 groups per user. Deleted users stay visible until a later purge, so filter with `| where isempty(deletedDateTime)` ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/ueba-reference#limitations)).

```kql
// Instead of a hand-built privileged users list, use IdentityInfo
SigninLogs
| where TimeGenerated > ago(1d)
| join kind=inner (IdentityInfo | where AssignedRoles != "[]") on $left.UserPrincipalName == $right.AccountUPN
```

In Defender portal onboarded workspaces with UEBA enabled, the unified `IdentityInfo` table exists in advanced hunting as well, and some fields are renamed there, like `AccountUPN` to `AccountUpn`: check queries if you hunt in both places ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/ueba-reference)).

Keep watchlists for what UEBA cannot know: leaver dates before the account is disabled, organisational value judgements like VIP, and non-user context like subnets and assets.

## Keeping them current

A stale watchlist fails silently: rules keep running, they just stop matching. Feed each list from its system of record rather than editing by hand.

| Watchlist | Feed from | How |
|---|---|---|
| Terminated Employees | HR, via Entra ID | Preferred: [HR-driven provisioning](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/what-is-hr-driven-provisioning) brings Workday, SuccessFactors and similar into Entra ID, so leaver state shows up in `IdentityInfo` and `AuditLogs` automatically. For the pre-termination window, run a scheduled Logic App that adds a watchlist item when HR notifies, using the Sentinel connector's Watchlists actions ([Microsoft Learn](https://learn.microsoft.com/en-us/connectors/azuresentinel/)). |
| VIP Users | Business owners | Small list, reviewed quarterly. An Entra group membership export can generate the CSV, but the value judgement stays human. |
| Network Addresses | Network team | CSV export from IPAM or firewall config review, then bulk update. Tag subnets by role, like DMZ or corporate VPN. |
| High Value Assets | CMDB and cloud inventory | Azure assets: query [Azure Resource Graph](https://learn.microsoft.com/en-us/azure/governance/resource-graph/overview) on a schedule and generate the CSV. Everything else: export from the CMDB. |
| Identity Correlation | Identity team | Manual, or generated from a privileged access process. Review when admins change roles. |
| Service Accounts | Entra ID | Service principal inventory export, with owners mapped from your request process. |

Automation notes for the Logic App path:

- The Microsoft Sentinel connector has full watchlist actions: create or update with raw content, add item, update item, delete item ([Microsoft Learn](https://learn.microsoft.com/en-us/connectors/azuresentinel/#actions)). Write actions need Microsoft Sentinel Contributor on the workspace.
- **Bulk update appends, it never deletes.** Removing leavers from a Terminated Employees list after a retention window means deleting items one by one, or deleting and recreating the watchlist. If you recreate, expect duplicate rows in Log Analytics for about five minutes after the swap ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/watchlists-manage)).
- Prefer editing items over delete-and-recreate: the recreate window shows both old and new entries to rules ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/watchlists-manage)).
- A watchlist that returns zero rows right after creation is usually the workspace daily cap blocking ingestion, not a broken watchlist ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/watchlists#troubleshoot-watchlists-that-show-zero-rows-after-creation)).
- Don't apply narrow time scopes to watchlist queries: the function returns current state refreshed on a cycle, and a tight time range can return empty results even when the list exists ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/watchlists#troubleshoot-empty-or-partial-query-results)).

## Watch the watchlists

Alert on staleness the same way you alert on log sources ([Sentinel health guide](sentinel-health.md)). The `Watchlist` table records when each item last changed:

```kql
// Which watchlists have not been touched in 30 days?
// ASSUMPTION: lists expected to change more often, like leavers, deserve a shorter window.
Watchlist
| where TimeGenerated > ago(60d)
| summarize Items = count(), LastUpdate = max(LastUpdatedTimeUTC) by WatchlistAlias
| where LastUpdate < ago(30d)
```

And a completeness check for the lists rules depend on: if a rule expects a watchlist and the alias is missing entirely, it silently returns nothing.

```kql
// Are the watchlists the guides rely on present and populated?
let expected = dynamic(["TerminatedEmployees", "VIPUsers", "NetworkAddresses", "HighValueAssets", "ServiceAccounts"]);
let present = _GetWatchlistAlias | project WatchlistAlias;
expected
| where WatchlistAlias !in (present)
| extend Problem = "watchlist missing"
```

`_GetWatchlistAlias` lists aliases ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/watchlists#watchlists-in-queries-for-searches-and-detection-rules)); match the aliases to your own names, because some templates create aliases without spaces, like `VIPUsers` rather than "VIP Users".

## Official links

- [Use watchlists to correlate and enrich event data](https://learn.microsoft.com/en-us/azure/sentinel/watchlists)
- [Create watchlists](https://learn.microsoft.com/en-us/azure/sentinel/watchlists-create)
- [Edit watchlists](https://learn.microsoft.com/en-us/azure/sentinel/watchlists-manage)
- [Built-in watchlist schemas](https://learn.microsoft.com/en-us/azure/sentinel/watchlist-schemas)
- [Watchlist table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/watchlist)
- [UEBA reference, including the IdentityInfo table](https://learn.microsoft.com/en-us/azure/sentinel/ueba-reference)
- [Enable UEBA](https://learn.microsoft.com/en-us/azure/sentinel/enable-entity-behavior-analytics)
- [What is HR-driven provisioning with Microsoft Entra ID?](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/what-is-hr-driven-provisioning)
- [Plan cloud HR application to Microsoft Entra user provisioning](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/plan-cloud-hr-provision)
- [Microsoft Sentinel connector for Logic Apps, watchlist actions](https://learn.microsoft.com/en-us/connectors/azuresentinel/)
- [Azure Resource Graph overview](https://learn.microsoft.com/en-us/azure/governance/resource-graph/overview)
