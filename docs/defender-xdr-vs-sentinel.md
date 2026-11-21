# Defender XDR vs Sentinel: avoiding duplication

> Status: verified. Last verified: 21 Nov 2026.

Microsoft Defender XDR already collects, stores and lets you hunt across endpoint, email, identity and cloud app telemetry at no Sentinel ingestion cost. Streaming the same raw tables into a Sentinel workspace without a clear reason is one of the fastest ways to overspend. This guide explains what stays in Defender XDR, when to stream to Sentinel, how to prevent duplicate incidents, and when to choose unified custom detections over Sentinel analytic rules.

## What Defender XDR keeps by default

When you onboard Sentinel to the Microsoft Defender portal, you query Defender XDR tables and Sentinel workspace tables side by side in **Investigation & response > Advanced hunting** ([Microsoft Sentinel in the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal)).

- **Standard Defender XDR retention:** 30 days in the XDR default tier at no Sentinel ingestion or storage charge ([manage tables, tiers, and retention](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention)).
- **ISOC 90-day retention benefit:** Starting 15 November 2026, eligible customers using Integrated Security Operations Center (ISOC) with Microsoft Defender Suite, Microsoft 365 E5 or Microsoft 365 E7 receive up to 90 days of included retention for supported Defender XDR, Azure Activity and Office 365 Activity tables at no additional charge (`AgentsInfo` and `IdentityAccountInfo` remain 30 days) ([manage tables in ISOC](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention-isoc)).
- **Unsupported TVM tables:** Defender Vulnerability Management tables (`DeviceTvmSoftwareInventory`, `DeviceTvmSoftwareVulnerabilities`, `DeviceTvmSecureConfigurationAssessment` and related `*KB` tables) are visible in schema autocomplete but are not ingested into Sentinel workspaces. Query them in Defender XDR advanced hunting ([Defender XDR integration](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-365-defender-sentinel-integration)).

## When to stream raw Defender tables to Sentinel

Only stream raw Defender XDR tables into Sentinel (or extend their retention past the included XDR window in Table management) when you need one of four things:

1. **Retention beyond the included XDR window.** If compliance or incident response requires 180 days to 12 years of `DeviceProcessEvents` or `EmailEvents`, either extend Analytics retention or route directly to the Sentinel **Data lake tier** (cheaper ingestion and 6:1 compressed storage, while keeping the included 30-day or 90-day Analytics view in Defender XDR) ([manage tables, tiers, and retention](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention)).
2. **Legacy Sentinel-only workflows.** Workbooks, Logic Apps playbooks, UEBA or third-party exports that must query the Log Analytics workspace API directly rather than Defender advanced hunting.
3. **Cross-workspace or non-Defender data lake joins.** Running KQL jobs or Jupyter notebooks in the Sentinel data lake across historical Defender telemetry and third-party firewall, proxy or cloud logs.
4. **Workspace transformations or export.** Exporting filtered Defender tables out of Log Analytics to Event Hubs or Storage.

You do **not** need to stream raw Defender XDR tables into Sentinel just to correlate them with Sentinel tables in a detection rule. In the Defender portal, unified custom detections can join Defender XDR tables and Sentinel workspace tables directly.

## Decision table per Defender product

| Product | Free in Defender XDR | Free in Sentinel | Paid raw tables if streamed to Sentinel | Recommendation |
|---|---|---|---|---|
| **Microsoft Defender for Endpoint** | `Device*` tables (30 days default, 90 days ISOC) plus TVM tables | `SecurityAlert`, `SecurityIncident` via Defender XDR connector | `DeviceProcessEvents`, `DeviceNetworkEvents`, `DeviceFileEvents`, `DeviceEvents`, `DeviceLogonEvents`, `DeviceRegistryEvents`, `DeviceImageLoadEvents`, `DeviceInfo`, `DeviceNetworkInfo`, `DeviceFileCertificateInfo` | Leave in Defender XDR by default; `DeviceNetworkEvents` and `DeviceProcessEvents` are huge. Stream to the Sentinel Data lake tier only if you need longer than 30/90 days retention. |
| **Microsoft Defender for Office 365** | `Email*`, `UrlClickEvents`, `Message*`, `CampaignInfo` (30 days default, 90 days ISOC) | `SecurityAlert`, `SecurityIncident` via Defender XDR connector | `EmailEvents`, `EmailUrlInfo`, `EmailAttachmentInfo`, `EmailPostDeliveryEvents`, `UrlClickEvents` | Leave in Defender XDR for alerting via custom detections. Stream `EmailEvents` and `UrlClickEvents` only if Sentinel analytic rules or >30/90 day retention require them. |
| **Microsoft Defender for Identity** | `IdentityLogonEvents`, `IdentityQueryEvents`, `IdentityDirectoryEvents`, `IdentityEvents` | `SecurityAlert`, `SecurityIncident` via Defender XDR connector | `IdentityLogonEvents`, `IdentityQueryEvents`, `IdentityDirectoryEvents` | Medium volume. Leave in Defender XDR unless you need >30/90 day AD investigation history in Sentinel or Sentinel-only workbooks. |
| **Microsoft Defender for Cloud Apps** | `CloudAppEvents`, `OAuthAppInfo` | `SecurityAlert`, `SecurityIncident` via Defender XDR connector | `CloudAppEvents`, `McasShadowItReporting` (classic discovery logs) | Leave `CloudAppEvents` in Defender XDR unless Sentinel analytic rules or long retention need it. Stream `McasShadowItReporting` to Data lake tier only if you track shadow IT long term. |
| **Microsoft Defender for Cloud** | Alerts sync into Defender XDR incidents; supported cloud hunting tables (`CloudAuditEvents`, `CloudStorageEvents`, etc.) in ISOC | `SecurityAlert` via Defender for Cloud connector | `SecurityRecommendation`, `SecureScores`, `SecurityRegulatoryCompliance` (continuous export) | **Enable both** Defender XDR integration and the tenant-based Defender for Cloud connector so Defender for Cloud incidents carry alerts and entities (see below). |
| **Microsoft Entra ID and ID Protection** | `EntraIdSignInEvents`, `EntraIdSpnSignInEvents`, `EntraIdDirectoryAuditEvents`, `GraphAPIAuditEvents` (Entra ID P2 for sign-ins) | `SecurityAlert` (Entra ID Protection) | `SigninLogs`, `AADNonInteractiveUserSignInLogs`, `AADServicePrincipalSignInLogs`, `AuditLogs`, `AADUserRiskEvents`, `AADRiskyUsers`, `MicrosoftGraphActivityLogs` | Keep `SigninLogs`, `AuditLogs` and `AADServicePrincipalSignInLogs` in Sentinel Analytics for UEBA and Content Hub rules; consider Data lake tier for `MicrosoftGraphActivityLogs` and review `AADNonInteractiveUserSignInLogs` after 7 days. |
| **Microsoft Purview DLP** | Alerts in Defender XDR, `CloudAppEvents` and `DeviceEvents` (Endpoint DLP) | `SecurityAlert`, `SecurityIncident` via Defender XDR connector; `OfficeActivity` (free) | Raw `CloudAppEvents` / `DeviceEvents` if streamed | Rely on Defender XDR incident sync plus free `OfficeActivity` audit events. |
| **Microsoft Purview Insider Risk Management** | Alerts in Defender XDR (`AlertInfo`, `AlertEvidence`) | `SecurityAlert`, `SecurityIncident` | No high-volume raw table needed in Sentinel | Sync alerts via Defender XDR (or Purview Insider Risk connector if not yet unified). Watch RBAC and anonymisation settings before exposing alerts to the wider SOC. |
| **Defender Vulnerability Management (TVM)** | `DeviceTvm*` tables in advanced hunting | Not supported in Sentinel | Cannot be streamed via the standard connector | Query in Defender XDR advanced hunting only. |

## Cost implications

- **Alerts and incidents are free.** `SecurityAlert` and `SecurityIncident` synced through the Defender XDR connector incur no Sentinel ingestion charge ([free data sources](https://learn.microsoft.com/en-us/azure/sentinel/billing#free-data-sources)).
- **Raw advanced hunting tables are billable.** Turning on event streaming in the Defender XDR connector or extending an XDR table's Analytics retention beyond the included 30-day (or 90-day ISOC) window charges full Sentinel Analytics ingestion per GB ([Sentinel pricing](https://azure.microsoft.com/en-us/pricing/details/microsoft-sentinel/)).
- **Direct-to-lake option.** If you only need long-term retention (for example 1 to 7 years) on raw XDR tables, set the table to the **Data lake tier** in **Table management**. You keep the included 30-day (or 90-day ISOC) Analytics view in Defender XDR while paying only the much lower data lake ingestion, processing and 6:1 compressed storage rates ([manage tables, tiers, and retention](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention)).
- **Microsoft 365 E5 data grant.** Check your Microsoft 365 E5, A5, F5 or G5 data grant benefit (5 MB/user/day toward eligible Entra, Defender for Cloud Apps, Defender for Endpoint and Information Protection ingestion) in Azure Cost Management before sizing a commitment tier ([Sentinel billing](https://learn.microsoft.com/en-us/azure/sentinel/billing)).

## Avoiding duplicate alerts and incidents

Duplicate incidents happen when both the Defender XDR connector and legacy standalone product connectors are active at the same time.

1. **Use the Defender portal onboarding.** When you onboard Microsoft Sentinel to the Defender portal and hold Defender XDR licences, the Defender XDR connector is enabled automatically and legacy alert connectors for Defender for Endpoint, Office 365, Identity, Cloud Apps (alerts) and Entra ID Protection are disconnected automatically ([Defender XDR integration](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-365-defender-sentinel-integration)).
2. **Turn off Microsoft incident creation rules for XDR products.** Microsoft incident creation rules aren't supported in the Defender portal because Defender's correlation engine creates and groups incidents natively. Replace alert filtering with Defender portal **alert tuning** or Sentinel **automation rules** using tags rather than incident titles (Defender automatically renames correlated incidents).
3. **Keep the Defender for Cloud connector enabled.** Defender XDR brings in Defender for Cloud incidents, but you **must** also enable the tenant-based Microsoft Defender for Cloud connector in Sentinel so alerts and entities populate. Without it, Defender for Cloud incidents appear empty ([Defender XDR integration](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-365-defender-sentinel-integration), [connect Defender for Cloud](https://learn.microsoft.com/en-us/azure/sentinel/connect-defender-for-cloud)).
4. **Watch the 150-alert Sentinel cap.** Bi-directional sync keeps status, owner, tags, comments and classifications aligned in near real time. If a Defender XDR incident grows beyond 150 alerts, the synced Sentinel copy displays `150+` and links back to the full Defender XDR incident.
5. **Resetting XDR retention stops streaming.** In Table management, resetting an XDR table's Analytics and total retention back to the default 30 days stops Sentinel ingestion for that table.

## Unified custom detections vs Sentinel analytic rules

Microsoft recommends **custom detection rules** in the Defender portal as the primary format for new rules across both Defender XDR and Sentinel data ([Defender XDR integration](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-365-defender-sentinel-integration), [custom detection rules](https://learn.microsoft.com/en-us/defender-xdr/custom-detection-rules)). Many Content Hub solutions (such as Microsoft Entra ID and Microsoft Business Applications) now ship the same detection in both formats.

| Capability | Defender XDR custom detections | Sentinel scheduled / NRT analytic rules |
|---|---|---|
| **Tables supported** | Both Defender XDR tables (without Sentinel ingestion) and Sentinel Analytics tables, including cross-joins | Sentinel workspace Analytics tables only |
| **Near real time (NRT)** | Continuous (NRT) on single-table supported queries, no per-workspace NRT quota friction | Separate NRT rule limit per workspace |
| **Automated response** | Built-in Defender actions (isolate device, revoke sessions, mark user compromised, quarantine file) plus Sentinel automation rules | Sentinel automation rules and Logic Apps playbooks |
| **Alert cap per run** | 150 alerts per run | Configurable event grouping and alert limits |
| **Permissions needed** | Both Defender XDR role (for Defender tables) and Microsoft Sentinel Contributor (for Sentinel tables) | Microsoft Sentinel Contributor on the workspace |
| **Rule to avoid duplicates** | **Pick one format per Content Hub template.** Never enable both the Sentinel analytic rule and the Defender XDR custom detection copy of the same rule. | Same: disable the duplicate format when migrating to custom detections. |

## Official links

- [Microsoft Defender XDR integration with Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-365-defender-sentinel-integration)
- [Stream data from Microsoft Defender XDR to Microsoft Sentinel in the Azure portal](https://learn.microsoft.com/en-us/azure/sentinel/connect-microsoft-365-defender)
- [Microsoft Sentinel in the Microsoft Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal)
- [Manage tables, tiers, and retention in Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention)
- [Manage tables, tiers, and retention in ISOC](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention-isoc)
- [Create custom detection rules in Microsoft Defender XDR](https://learn.microsoft.com/en-us/defender-xdr/custom-detection-rules)
- [Plan costs and understand pricing and billing](https://learn.microsoft.com/en-us/azure/sentinel/billing)
- [Microsoft Sentinel pricing](https://azure.microsoft.com/en-us/pricing/details/microsoft-sentinel/)
- [Ingest Microsoft Defender for Cloud alerts into Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/connect-defender-for-cloud)

## Last verified

21 Nov 2026, against Microsoft Learn.
