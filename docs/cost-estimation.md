# Cost estimation and ingestion monitoring

> Status: verified. Last verified: 21 Nov 2026.

Microsoft Sentinel bills mainly on the GB ingested into the **Analytics tier** (pay-as-you-go or commitment tier), plus lower-cost meters for **Data lake tier** ingestion, processing, 6:1 compressed storage and queries ([Sentinel billing](https://learn.microsoft.com/en-us/azure/sentinel/billing)). Before you turn on noisy tables or commit to a daily tier, measure actual GB/day with the KQL pack in [queries/cost/](../queries/cost/README.md).

## Where to run these queries

- **Microsoft Defender portal (recommended):** Go to **Investigation & response > Advanced hunting**, open the query editor and confirm your Sentinel workspace is selected in the scope bar. Queries 1 to 6 run against the Sentinel `Usage` table and workspace tables; query 7 runs directly against Defender XDR tables without streaming them to Sentinel.
- **Azure portal (retiring 31 March 2027):** Go to your Log Analytics workspace > **Logs**, paste the query and set the time range to match the query window (usually 30 days) ([monitor costs](https://learn.microsoft.com/en-us/azure/sentinel/billing-monitor-costs)).
- **Data lake costs:** Analytics `Usage` queries do not show data lake query or notebook compute charges. Review those in the Defender portal under **Microsoft Sentinel > Cost management** (needs Security Reader to view, Billing Administrator or Security Administrator to set alerts) and in Azure **Cost Management + Billing** ([monitor costs](https://learn.microsoft.com/en-us/azure/sentinel/billing-monitor-costs)).

## Query pack

All seven queries live as standalone `.kql` files in [queries/cost/](../queries/cost/README.md):

| File | What it answers |
|---|---|
| [01-gb-per-table.kql](../queries/cost/01-gb-per-table.kql) | Billable vs free GB per table (daily average, 30-day total and % share of billable volume) |
| [02-gb-per-solution.kql](../queries/cost/02-gb-per-solution.kql) | Billable GB grouped by Sentinel solution and data type |
| [03-gb-per-dcr.kql](../queries/cost/03-gb-per-dcr.kql) | Estimated GB per resource and Data Collection Rule (`_BilledSize`) for AMA and diagnostic tables |
| [04-daily-trend-and-anomalies.kql](../queries/cost/04-daily-trend-and-anomalies.kql) | 30-day daily billable GB trend with automatic spike detection (`series_decompose_anomalies`) |
| [05-top-noisy-events-and-hosts.kql](../queries/cost/05-top-noisy-events-and-hosts.kql) | Top noisy Windows Event IDs, `AzureDiagnostics` categories and source hosts driving ingestion cost |
| [06-commitment-tier-sizing.kql](../queries/cost/06-commitment-tier-sizing.kql) | Daily billable GB percentiles (p50, p90, p95, max) to decide between pay-as-you-go and commitment tiers |
| [07-xdr-streaming-cost-preview.kql](../queries/cost/07-xdr-streaming-cost-preview.kql) | Pre-streaming GB/day estimate for Defender XDR tables run directly in advanced hunting |

### Starter query: billable GB per table over 30 days

Note that Azure billing measures GB in decimal (`10^9` bytes, so `Usage.Quantity` in MB divides by `1000` for billing GB, or `1024` for GiB) ([Sentinel billing](https://learn.microsoft.com/en-us/azure/sentinel/billing), [monitor costs](https://learn.microsoft.com/en-us/azure/sentinel/billing-monitor-costs)).

```kql
// Billable and free GB per table over the last 30 complete days
Usage
| where StartTime >= startofday(ago(31d)) and EndTime < startofday(now())
| summarize
    BillableGB = round(sumif(Quantity, IsBillable == true) / 1000.0, 2),
    FreeGB = round(sumif(Quantity, IsBillable == false) / 1000.0, 2)
    by DataType
| extend DailyAvgBillableGB = round(BillableGB / 30.0, 2)
| order by BillableGB desc
```

## Pre-onboarding estimation using a trial workspace

Every new Microsoft Sentinel workspace includes a **31-day free trial** covering the first **10 GB/day** of Analytics tier ingestion (both Log Analytics ingestion and Sentinel analysis charges are waived up to 10 GB/day; limit of 20 trial workspaces per tenant; automation, BYOML and data lake meters still apply) ([free trial](https://learn.microsoft.com/en-us/azure/sentinel/billing#free-trial)).

Use a staging trial workspace to measure real volume before enabling noisy connectors in production:

1. **Create a separate non-production Log Analytics workspace** and enable Microsoft Sentinel (automatically starts the 31-day, 10 GB/day free trial).
2. **Connect a representative sample** for 7 days:
   - For Entra ID and Purview, connect a pilot tenant or estimate directly from Defender XDR advanced hunting with [07-xdr-streaming-cost-preview.kql](../queries/cost/07-xdr-streaming-cost-preview.kql).
   - For Windows Server, AD DS or Linux fleets, attach a DCR to 5 to 10 representative hosts (one domain controller, one busy web server, one workstation, one Syslog forwarder) and multiply the per-host GB/day by fleet size.
   - For Azure PaaS (Key Vault, Storage, Firewall, AKS), point diagnostic settings from one representative production resource per tier at the trial workspace for 72 hours.
3. **Measure with queries 1, 3 and 5.** Identify the top noisy event IDs or categories before building your production DCR transformations.
4. **Apply free data sources and grants.** Subtract free tables (`AzureActivity`, `SentinelHealth`, `OfficeActivity` for Exchange/SharePoint/Teams, and `SecurityAlert` / `SecurityIncident` from Defender XDR and Defender for Cloud) and any Microsoft 365 E5 (5 MB/user/day) or Defender for Servers Plan 2 (500 MB/server/day) data grants ([free data sources](https://learn.microsoft.com/en-us/azure/sentinel/billing#free-data-sources)).
5. **Size the pricing model** with query 6 and cross-check against the [Microsoft Sentinel pricing page](https://azure.microsoft.com/en-us/pricing/details/microsoft-sentinel/).
6. **Delete or disconnect the trial workspace before day 31** so it doesn't silently roll over into pay-as-you-go billing.

## Main levers to cut Sentinel spend

- **Separate non-security logs.** Sentinel analyses every billable table in a Sentinel-enabled workspace. Keep pure operational APM and infrastructure metrics in a separate Log Analytics workspace ([reduce costs](https://learn.microsoft.com/en-us/azure/sentinel/billing-reduce-costs)).
- **Route hunt-only tables to the Data lake tier.** Firewall traffic, VNet flow logs, Storage reads, DNS and Graph activity logs belong in the Data lake tier unless an analytic rule reads them. See [data-lake-tiering.md](data-lake-tiering.md).
- **Filter at source with AMA and DCRs.** Use `Common` or targeted XPath filters for Windows Security Events and DCR KQL transformations to drop noisy operational events before ingestion.
- **Avoid streaming Defender XDR tables twice.** Leave `Device*`, `Email*` and `Identity*` in Defender XDR advanced hunting unless you need retention beyond 30 days (or 90 days on ISOC). See [defender-xdr-vs-sentinel.md](defender-xdr-vs-sentinel.md).
- **Use simplified commitment tiers and pre-purchase plans.** Once daily billable volume regularly exceeds roughly 60 to 70 GB/day (check current regional rates), a 100 GB/day simplified commitment tier or a 1-year Microsoft Sentinel pre-purchase plan (commit units) cuts per-GB cost materially ([reduce costs](https://learn.microsoft.com/en-us/azure/sentinel/billing-reduce-costs)). You can step up a commitment tier at any time; stepping down requires 31 days.
- **Set Azure Cost Management budgets and alerts.** Configure subscription or resource-group budgets filtered to `Sentinel`, `Log Analytics` and `Azure Monitor`, and deploy the built-in **Workspace Usage Report** workbook ([monitor costs](https://learn.microsoft.com/en-us/azure/sentinel/billing-monitor-costs)).

## Official links

- [Plan costs and understand pricing and billing](https://learn.microsoft.com/en-us/azure/sentinel/billing)
- [Manage and monitor costs for Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/billing-monitor-costs)
- [Reduce costs for Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/billing-reduce-costs)
- [Microsoft Sentinel pricing](https://azure.microsoft.com/en-us/pricing/details/microsoft-sentinel/)
- [Manage tables, tiers, and retention in Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention)
- [Transformations in Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/data-collection-transformations)

## Last verified

21 Nov 2026, against Microsoft Learn.
