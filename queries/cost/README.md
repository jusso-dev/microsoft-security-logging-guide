# Cost estimation query pack

KQL queries for measuring Microsoft Sentinel ingestion volume, finding noisy sources, sizing commitment tiers, and previewing Defender XDR streaming costs. See [docs/cost-estimation.md](../../docs/cost-estimation.md) for instructions on running these in the Defender portal and sizing a trial workspace.

| Query | Purpose | Where to run |
|---|---|---|
| [01-gb-per-table.kql](01-gb-per-table.kql) | Billable vs free GB per table over 30 days, with daily average and % share | Sentinel workspace |
| [02-gb-per-solution.kql](02-gb-per-solution.kql) | Billable GB grouped by Sentinel solution and table | Sentinel workspace |
| [03-gb-per-dcr.kql](03-gb-per-dcr.kql) | Ingestion GB by Azure resource and Data Collection Rule (`_BilledSize`) | Sentinel workspace |
| [04-daily-trend-and-anomalies.kql](04-daily-trend-and-anomalies.kql) | 30-day daily billable GB trend and spike detection | Sentinel workspace |
| [05-top-noisy-events-and-hosts.kql](05-top-noisy-events-and-hosts.kql) | Top noisy Windows Event IDs, `AzureDiagnostics` categories and hosts | Sentinel workspace |
| [06-commitment-tier-sizing.kql](06-commitment-tier-sizing.kql) | Daily billable GB percentiles for commitment tier selection | Sentinel workspace |
| [07-xdr-streaming-cost-preview.kql](07-xdr-streaming-cost-preview.kql) | Estimate GB/day of Defender XDR tables before enabling Sentinel streaming | Defender XDR advanced hunting |

## One-click Sentinel workbook deployment

Queries 1 to 6 are packaged as the **Cost Estimation and Volume Monitoring** workbook inside the [Microsoft Sentinel solution package](../../solution/README.md) (query 7 is also included in [defender-xdr/](../../defender-xdr/README.md)):

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fjusso-dev%2Fmicrosoft-security-logging-guide%2Fmain%2Fsolution%2FSolutions%2FMicrosoftSecurityLoggingGuide%2FPackage%2FmainTemplate.json)
