# Sentinel health and audit monitoring

A SIEM that quietly stops ingesting is worse than no SIEM: rules keep running, they just match nothing. Microsoft Sentinel writes its own health and audit data, but you have to turn it on, and it only covers some connector types. This page covers the three tables, what they see, the gaps, and the alerts that tell you when a high-value source goes quiet.

> Status: verified. Last verified: 21 Nov 2026.

## The three tables

| Table | What it holds | How it is turned on | Tier |
|---|---|---|---|
| `SentinelHealth` | Health events for supported resources: data connectors, analytics rules, automation rules and playbooks | Sentinel settings, **Auditing and health monitoring** ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/enable-monitoring)) | Analytics. Tiny volume. |
| `SentinelAudit` | Audit of changes made to Sentinel resources: analytics rule create, update, delete | Same setting as `SentinelHealth` ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/enable-monitoring)) | Analytics. Tiny volume. |
| `LAQueryLogs` | Every query run against the workspace: who ran it, from which tool, the full query text, response code and duration | A diagnostic setting on the Log Analytics workspace ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/query-audit)) | Analytics. Low volume, scales with SOC activity. |

`SentinelHealth` and `SentinelAudit` support the Auxiliary or data lake table plans and DCR workspace transformations, but not the Basic plan. They are small enough that tier rarely matters ([SentinelHealth reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/sentinelhealth), [SentinelAudit reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/sentinelaudit)). Enabling query auditing is free, but the ingested `LAQueryLogs` data is billed ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/query-audit#query-audit-data-ingestion-costs)).

## Turn on auditing and health monitoring

1. In the Defender portal, select **System** > **Settings** > **Microsoft Sentinel**. In the Azure portal it is **Configuration** > **Settings**.
2. Select **Auditing and health monitoring**, then **Enable**. This adds the right diagnostic settings for all supported resource types and sends the data to the Sentinel workspace.
3. For granular control, select **Configure diagnostic settings** instead, add a diagnostic setting, choose categories such as **Data Collection - Connectors**, or **allLogs** to cover analytics rules, and send them to your Log Analytics workspace ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/enable-monitoring)).
4. The tables are created when the first event for a selected resource occurs.
5. Turn on query auditing with a diagnostic setting on the workspace itself ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/query-audit)).

Verify data is flowing with the functions Microsoft documents for the purpose ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/enable-monitoring#verify-that-the-tables-are-receiving-data)):

```kql
_SentinelHealth()
| take 20
```

```kql
_SentinelAudit()
| take 20
```

## What SentinelHealth does and does not cover

Data connector health events exist only for connectors that fetch data from somewhere else. Microsoft supports ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/monitor-data-connector-health#supported-data-connectors)):

- Amazon Web Services, CloudTrail and S3
- Dynamics 365
- Office 365
- Microsoft Defender for Endpoint
- Threat Intelligence, TAXII and platforms
- Any connector built on the Codeless Connector Framework

Everything that arrives through Azure diagnostic settings, such as Microsoft Entra ID, Azure Activity, Key Vault, Storage and Intune, has no fetch step, so it never appears in `SentinelHealth`. For those sources, watch table freshness directly. The repo's validation pack runs that check across every documented table: [queries/validation/health-all-tables.kql](../queries/validation/health-all-tables.kql).

Health events are batched, not instant ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/monitor-data-connector-health#understanding-sentinelhealth-table-events)):

- **Data fetch status change** is logged once an hour while a connector's status is stable, and immediately when status changes. Transient errors, like source throttling, are logged only after 60 minutes, so brief hiccups stay invisible by design.
- **Failure summary** is logged hourly, per connector, but only when the connector actually had polling errors.

## Detect health drift

Microsoft's documented drift queries, from [Monitor the health of your data connectors](https://learn.microsoft.com/en-us/azure/sentinel/monitor-data-connector-health#run-queries-to-detect-health-drifts):

```kql
// Latest status per connector, failures only
SentinelHealth
| where TimeGenerated > ago(3d)
| where OperationName == 'Data fetch status change'
| where Status in ('Success', 'Failure')
| summarize TimeGenerated = arg_max(TimeGenerated, *) by SentinelResourceName, SentinelResourceId
| where Status == 'Failure'
```

```kql
// Connector health at a glance over a week
SentinelHealth
| where TimeGenerated > ago(7d)
| where SentinelResourceType == 'DataConnector'
| summarize Events = count(),
            Failures = countif(Status == 'Failure'),
            Latest = arg_max(TimeGenerated, Status)
    by Connector = SentinelResourceName
| order by Failures desc
```

## Alert when a source goes quiet

Microsoft recommends [Azure Monitor log alert rules](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-log) for connector health rather than Sentinel analytics rules: the health monitor should not depend on the thing it monitors ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/monitor-data-connector-health#configure-alerts-and-automated-actions-for-health-drifts)). Scope the alert rule to the Sentinel workspace, use **Custom log search**, and attach an action group.

**Alert 1: a supported connector is failing.** Run hourly over a 1-hour lookback:

```kql
// ALERT - a supported data connector stopped fetching successfully
SentinelHealth
| where TimeGenerated > ago(1h)
| where OperationName == 'Data fetch status change'
| where Status == 'Failure'
| project TimeGenerated, Connector = SentinelResourceName, Status, Reason, ExtendedProperties
```

**Alert 2: a critical table went quiet.** This catches the sources `SentinelHealth` cannot see, and tables that keep landing but stale. Edit the list to match what you actually ingest, and pair each table with how long it can safely be silent:

```kql
// ALERT - critical tables are stale or empty
// ASSUMPTION: the table list and staleness budget match your environment.
// OfficeActivity is polled, so give it a longer budget than push-based logs.
let expected = datatable(Table: string, MaxStaleMinutes: long)
    ["SigninLogs", 120,
     "AuditLogs", 120,
     "AzureActivity", 120,
     "OfficeActivity", 720,
     "SecurityEvent", 120,
     "CommonSecurityLog", 120];
let seen = union withsource=TableName isfuzzy=true
        SigninLogs, AuditLogs, AzureActivity, OfficeActivity, SecurityEvent, CommonSecurityLog
    | where TimeGenerated > ago(14d)
    | summarize Latest = max(TimeGenerated) by TableName;
expected
| join kind=leftouter seen on $left.Table == $right.TableName
| extend StaleMinutes = round((now() - coalesce(Latest, ago(14d))) / 1m)
| where StaleMinutes > MaxStaleMinutes
| project Table, Latest, StaleMinutes, MaxStaleMinutes
```

An empty table and a stale table both alert, so tune `MaxStaleMinutes` per source after a week of real data.

## Workbook and portal views

Two views cover connector health without writing rules:

- **Data & connectors, Overview tab (preview)** in the Defender portal under **Setup & configuration** > **Data & connectors**. It shows connector counts, ingestion volume by tier, connectors that need attention from `SentinelHealth`, table ingestion fluctuations and per-table latency, in one workspace view ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/monitor-data-connector-health#monitor-connector-health-and-ingestion-in-the-defender-portal-preview)).
- **Data collection health monitoring workbook**, installed from Content Hub. The Overview tab shows volume, events per second and time since the last log received, per table. The Data collection anomalies tab runs `series_decompose_anomalies()` over ingestion volume so you can spot drops and spikes, and the Agent info tab shows Azure Monitor Agent health: heartbeat, latency, memory and disk ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/monitor-data-connector-health#use-the-health-monitoring-workbook)).

## SentinelAudit: who changed the rules

`SentinelAudit` currently covers analytics rules only ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/enable-monitoring)). Record who disabled, deleted or weakened a rule, which is a quiet way to kill coverage:

```kql
// Analytics rules disabled or deleted
SentinelAudit
| where TimeGenerated > ago(14d)
| where SentinelResourceType == 'AlertRule'
| where OperationName has_any ('Delete', 'Disable', 'Update')
| project TimeGenerated, Rule = SentinelResourceName, OperationName, Description, ExtendedProperties
```

Changes to Sentinel itself, like who edited a connector, are also in the Azure Activity Log, which covers all Sentinel resource operations at the subscription level ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/audit-sentinel-data)).

## LAQueryLogs: query audit

Each query run in a user context produces a record with the caller, the tool, the full query text and performance statistics ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/query-audit#audit-data)). The `RequestClientApp` field tells you where the query came from: `ASI_Portal` is Sentinel, `M365D_AdvancedHunting` is Defender advanced hunting, and `AppAnalytics` is the Log Analytics blade ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/query-audit#request-client-app)).

Two useful checks for a SOC that stores its detection IP in KQL:

```kql
// Who queried the most sensitive tables this week
LAQueryLogs
| where TimeGenerated > ago(7d)
| where QueryText has_any ('SigninLogs', 'SecurityEvent', 'SentinelAudit')
| summarize Queries = count(), LastRun = max(TimeGenerated) by AADEmail, RequestClientApp
| order by Queries desc
```

```kql
// Failed or extremely slow queries
LAQueryLogs
| where TimeGenerated > ago(7d)
| where ResponseCode != 200 or ResponseDurationMs > 300000
| project TimeGenerated, AADEmail, ResponseCode, ResponseDurationMs, RequestClientApp, QueryText
```

Note the limits: service-to-service queries, billing calculations and scheduled alert executions are not logged, and performance statistics are missing for queries routed through the Azure Data Explorer proxy ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/query-audit#query-audit-logging-considerations)).

## Gotchas

- The supported connector list is narrow. Diagnostic-settings sources never produce fetch events, so an all-clear in `SentinelHealth` proves nothing about Entra ID or Azure Activity. Run the stale-table alert as well.
- Transient errors are suppressed for 60 minutes and stable status is logged hourly, so a connector can be broken for up to an hour before a status change event appears.
- `SentinelAudit` covers analytics rules only today. Use Azure Activity Log for connector and other resource changes ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/audit-sentinel-data)).
- Playbook health needs Logic Apps diagnostics as well; Sentinel sees the Sentinel side, Logic Apps sees the workflow runs ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/monitor-automation-health)).
- Sentinel in the Azure portal retires on 31 March 2027. Build these monitors in the Defender portal ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal)).

## Official links

- [Turn on auditing and health monitoring in Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/enable-monitoring)
- [Monitor the health of your Microsoft Sentinel data connectors](https://learn.microsoft.com/en-us/azure/sentinel/monitor-data-connector-health)
- [Monitor the health of your automation rules and playbooks](https://learn.microsoft.com/en-us/azure/sentinel/monitor-automation-health)
- [Audit and monitor the health of analytics rules](https://learn.microsoft.com/en-us/azure/sentinel/monitor-analytics-rule-integrity)
- [Audit Microsoft Sentinel with Azure Activity Logs](https://learn.microsoft.com/en-us/azure/sentinel/audit-sentinel-data)
- [Auditing and health monitoring in Microsoft Sentinel (overview)](https://learn.microsoft.com/en-us/azure/sentinel/health-audit)
- [SentinelHealth table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/sentinelhealth)
- [SentinelAudit table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/sentinelaudit)
- [LAQueryLogs table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/laquerylogs)
- [Audit queries in Azure Monitor log queries](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/query-audit)
- [Azure Monitor log alerts](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-log)
- [Sentinel in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal)
