# Data lake tiering guidance

> Status: verified. Last verified: 26 Nov 2026.

Microsoft Sentinel runs on two storage tiers: the **Analytics tier** (indexed hot storage for near-real-time analytic rules, custom detections, live hunting and workbooks) and the **Data lake tier** (open-format Parquet storage for low-cost ingestion, up to 12 years of retention, KQL jobs, summary rules and Jupyter notebooks) ([data lake overview](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-overview), [direct ingestion guidance](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-log-ingestion-guidance)).

## What changed in September 2026 (Table management, Basic and Auxiliary logs)

- **Integrated onboarding via Table management (September 2026):** Starting 23 September 2026, Microsoft integrated the Sentinel data lake directly into Sentinel SIEM onboarding. You no longer run a separate data lake onboarding and billing setup. Instead, open **Setup & configuration > Data management > Data & connectors > Tables** (or **Microsoft Sentinel > Configuration > Tables**) in the Defender portal, select a table, and select **Manage table** to mirror Analytics data to the data lake or switch a table to **Data lake tier** only ([What's new in Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/whats-new), [manage tables, tiers, and retention](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention)).
- **What happens to Basic and Auxiliary logs:** Once a workspace uses the Microsoft Sentinel data lake, low-cost long-term retention, search and auxiliary ingestion bill through the data lake meters rather than legacy Archive, search or Auxiliary logs meters ([Sentinel billing](https://learn.microsoft.com/en-us/azure/sentinel/billing)). Existing **Basic Logs** tables are visible in the Defender portal, but you still manage them in Log Analytics unless you switch their plan to Analytics first so Table management can control them ([manage tables](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention)). New deployments should use the **Analytics** and **Data lake** tiers rather than introducing legacy Basic or Auxiliary configurations.
- **Switching tiers live:** You can move supported tables between Analytics and Data lake at any time. Switching a table from Analytics to Data lake immediately stops real-time analytic rules, custom detections and live workspace hunting queries on that table. Shortening total retention has a 30-day safety grace period before deletion ([manage tables](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention)).

## Retention defaults and cost model

| Tier | Default retention | Maximum retention | Billing meters |
|---|---|---|---|
| **Defender XDR default** | 30 days (90 days included from 15 Nov 2026 for eligible ISOC E5/E7/Defender Suite tables, except `AgentsInfo` and `IdentityAccountInfo`) | 30 days (or 90 days ISOC) without Sentinel ingestion | Included in Defender XDR / ISOC licence ([ISOC retention](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention-isoc)) |
| **Sentinel Analytics tier** | 90 days interactive retention included free on Sentinel-enabled workspaces (30 days on non-Sentinel Log Analytics) | Up to 2 years interactive retention; up to 12 years total retention via mirrored data lake | Pay-as-you-go or Commitment tier ingestion (100 GB/day+) + prorated interactive retention beyond 90 days. Mirroring to the data lake for the same retention period costs nothing extra ([Sentinel billing](https://learn.microsoft.com/en-us/azure/sentinel/billing)) |
| **Sentinel Data lake tier (direct)** | Configurable (minimum 30 days) | Up to 12 years | Lower per-GB data lake ingestion + data processing + 6:1 compressed monthly storage (600 GB raw bills as 100 GB compressed) + per-GB uncompressed KQL query scan + notebook vCore compute ([Sentinel billing](https://learn.microsoft.com/en-us/azure/sentinel/billing), [pricing](https://azure.microsoft.com/en-us/pricing/details/microsoft-sentinel/)) |

## Promoting insights from the Data lake tier to Analytics

Analytic rules and custom detections cannot run directly on Data lake tier tables ([direct ingestion guidance](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-log-ingestion-guidance)). Use two built-in mechanisms to promote high-signal slices back into the Analytics tier:

1. **Summary rules:** Scheduled background KQL aggregations that write compact, pre-aggregated outputs into a custom `_CL` table on the Analytics plan (for example, hourly firewall deny counts per source IP or rare external DNS domains) ([summary rules](https://learn.microsoft.com/en-us/azure/sentinel/summary-rules)). Enable `SummaryLogs` diagnostic settings if you want run-failure telemetry.
2. **KQL jobs and Jupyter notebook jobs:** One-time or scheduled queries over data lake tables (including joins across workspaces and federated Entra/M365/Resource Graph tables) that promote matching rows to a new `_KQL_CL` table or existing Analytics table ([KQL jobs](https://learn.microsoft.com/en-us/azure/sentinel/datalake/kql-jobs), [notebook examples](https://learn.microsoft.com/en-us/azure/sentinel/datalake/notebook-examples)). Filter and project only needed columns to keep Analytics promotion volume small, and expect up to 15 minutes of ingestion latency in the lake.

## Per-table tier recommendations

Every active table documented across the 38 product guides in this repository is listed below. Retired or legacy tables (`Dynamics365Activity`, `LLMActivity`, `AIAgentsInfo`, `PowerAppsActivity`, `PowerPlatformConnectorActivity`, `PowerPlatformDlpActivity`, `AzureNetworkAnalytics_CL`, `DDoSMitigationReports`, `ContainerLog`, `GitHub_CL`, `GitHubAuditLogPolling_CL`, `InformationProtectionLogs_CL`, `AADSignInEventsBeta`, `AADSpnSignInEventsBeta`) are omitted because new deployments should not ingest them.

### Identity

| Table | Guide | Recommended tier | Why |
|---|---|---|---|
| `SigninLogs` | [Entra ID](../identity/entra-id/README.md) | **Analytics** (mirror to lake for 1+ yr) | Core identity detection and UEBA input; low to medium volume. |
| `AuditLogs` | [Entra ID](../identity/entra-id/README.md) | **Analytics** (mirror to lake for 1+ yr) | Role, consent, app and Conditional Access changes; low volume. |
| `AADServicePrincipalSignInLogs` | [Entra ID](../identity/entra-id/README.md) | **Analytics** | Workload identity abuse rules and UEBA baselines. |
| `AADManagedIdentitySignInLogs` | [Entra ID](../identity/entra-id/README.md) | **Analytics** | Low volume in most tenants; cheap to keep alertable. |
| `AADNonInteractiveUserSignInLogs` | [Entra ID](../identity/entra-id/README.md) | **Analytics** (review after 7 days; DCR-trim or move hunt-only slices to **Data lake**) | Often the largest Entra table, but password spray and CA bypass rules read it. |
| `AADProvisioningLogs` | [Entra ID](../identity/entra-id/README.md) | **Data lake** | Primarily investigation and SaaS lifecycle audit context. |
| `MicrosoftGraphActivityLogs` | [Entra ID](../identity/entra-id/README.md) | **Data lake** | Very high volume (~15 GiB/month per 1,000 users); hunt and promote via KQL jobs. |
| `ADFSSignInLogs` | [AD FS](../identity/adfs/README.md), [Entra ID](../identity/entra-id/README.md) | **Analytics** | Low volume for federated tenants; skip if cloud-only. |
| `AADUserRiskEvents`, `AADRiskyUsers`, `AADServicePrincipalRiskEvents`, `AADRiskyServicePrincipals`, `AADRiskyAgents`, `AADAgentRiskEvents` | [Entra ID Protection](../identity/entra-id-protection/README.md) | **Analytics** | Very low volume, high-severity identity risk signals. |
| `IdentityLogonEvents`, `IdentityQueryEvents`, `IdentityDirectoryEvents`, `IdentityEvents` | [Defender for Identity](../identity/defender-for-identity/README.md) | **Defender XDR default** (or **Data lake** if >30/90d retention needed) | Already free in Defender XDR; avoid paying twice unless long retention or Sentinel rules require them. |
| `IdentityInfo` | [Watchlists and enrichment](watchlists.md) | **Analytics** (managed by UEBA) | Required for UEBA user enrichment and VIP/leaver joins. |
| `NetworkAccessTraffic`, `NetworkAccessConnectionEvents`, `NetworkAccessGenerativeAIInsights` | [Global Secure Access](../identity/entra-global-secure-access/README.md) | **Data lake** | High-volume web proxy and private access flow telemetry; summarise to Analytics. |
| `NetworkAccessAlerts`, `RemoteNetworkHealthLogs` | [Global Secure Access](../identity/entra-global-secure-access/README.md) | **Analytics** | Low-volume alerts and remote network tunnel health. |
| `EntraIdSignInEvents`, `EntraIdSpnSignInEvents`, `EntraIdDirectoryAuditEvents`, `GraphAPIAuditEvents` | [Entra ID](../identity/entra-id/README.md) | **Defender XDR default** | Native Defender XDR views (P2/ISOC); no Sentinel streaming needed by default. |

### Endpoint and servers

| Table | Guide | Recommended tier | Why |
|---|---|---|---|
| `DeviceProcessEvents`, `DeviceNetworkEvents`, `DeviceFileEvents`, `DeviceEvents`, `DeviceLogonEvents`, `DeviceRegistryEvents`, `DeviceImageLoadEvents`, `DeviceInfo`, `DeviceNetworkInfo`, `DeviceFileCertificateInfo` | [Defender for Endpoint](../endpoint/defender-for-endpoint/README.md), [Windows Server](../servers/windows-server/README.md), [Linux](../servers/linux-syslog/README.md) | **Defender XDR default** (or **Data lake** if >30/90d retention needed) | Very high volume; free in Defender XDR for 30 days (90 days ISOC). Never stream blindly to Sentinel Analytics. |
| `DeviceTvmSoftwareInventory`, `DeviceTvmSoftwareVulnerabilities` | [Defender for Endpoint](../endpoint/defender-for-endpoint/README.md) | **Defender XDR only** | Unsupported for Sentinel ingestion; query in Defender XDR advanced hunting. |
| `SecurityEvent` | [AD DS](../identity/active-directory-on-prem/README.md), [AD FS](../identity/adfs/README.md), [Windows clients](../endpoint/windows-security-events/README.md), [Windows Server](../servers/windows-server/README.md), [SQL Server](../servers/sql-server/README.md) | **Analytics** (DCR-filtered with `Common` + targeted XPath) | Core Windows, DC and SQL Audit (ID 33205) detection table; covered by Defender for Servers P2 500 MB/node/day grant. |
| `WindowsEvent` | [Windows clients](../endpoint/windows-security-events/README.md), [Windows Server](../servers/windows-server/README.md) | **Analytics** (targeted WEF/XPath) or **Data lake** | Windows Forwarded Events via AMA; filter strictly at the collector. |
| `Event` | [Windows clients](../endpoint/windows-security-events/README.md), [Windows Server](../servers/windows-server/README.md), [SQL Server](../servers/sql-server/README.md) | **Analytics** (Analytics-only table) | PowerShell 4104, System, Application and Sysmon fallback; `Event` does not support Data lake tier. |
| `ASimDnsActivityLogs` | [Windows Server](../servers/windows-server/README.md) | **Data lake** (or DCR-filtered **Analytics**) | Windows DNS Server events via AMA; very high volume on busy DNS servers. |
| `W3CIISLog` | [Windows Server](../servers/windows-server/README.md) | **Data lake** | Verbose IIS web access logs; use summary rules or KQL jobs for web-attack hunts. |
| `MDCFileIntegrityMonitoringEvents` | [Windows Server](../servers/windows-server/README.md) | **Analytics** | Low volume, high signal; covered by Defender for Servers P2 500 MB/day grant. |
| `IntuneAuditLogs`, `IntuneOperationalLogs` | [Intune](../endpoint/intune/README.md) | **Analytics** | Low volume; detects wipe/retire, script deployment and compliance policy changes. |
| `IntuneDevices`, `IntuneDeviceComplianceOrg` | [Intune](../endpoint/intune/README.md) | **Data lake** | Daily snapshot inventory tables used mainly for enrichment and reporting. |
| `Syslog` | [Linux](../servers/linux-syslog/README.md) | **Analytics** (`auth`, `authpriv`, `auditd`) or **Data lake** (verbose daemons) | Keep auth/sudo/SSH in Analytics; drop or route noisy daemon facilities to the lake. |
| `CommonSecurityLog` | [Linux](../servers/linux-syslog/README.md) | **Data lake** (firewall/proxy traffic) or **Analytics** (IDS/IPS/threat alerts) | Classic high-volume CEF table; split or summarise allow-traffic in the lake. |

### Email, collaboration, cloud apps and data security

| Table | Guide | Recommended tier | Why |
|---|---|---|---|
| `OfficeActivity` | [Exchange](../email-collab/exchange-online/README.md), [SharePoint/OneDrive](../email-collab/sharepoint-onedrive/README.md), [Teams](../email-collab/teams/README.md), [Purview Audit](../email-collab/purview-unified-audit/README.md), [Purview DLP](../data-security/purview-dlp/README.md) | **Analytics** (free ingestion) | Exchange, SharePoint and Teams audit logs are free in Sentinel; keep in Analytics and extend lake retention as needed. |
| `EmailEvents`, `EmailPostDeliveryEvents`, `UrlClickEvents`, `EmailAttachmentInfo`, `EmailUrlInfo`, `FileMaliciousContentInfo`, `MessageEvents`, `MessagePostDeliveryEvents`, `MessageUrlInfo`, `CallActivityEvents`, `SyntheticMediaDetectionEvents` | [Defender for Office 365](../email-collab/defender-for-office-365/README.md), [SharePoint](../email-collab/sharepoint-onedrive/README.md), [Teams](../email-collab/teams/README.md) | **Defender XDR default** (or **Data lake** for >30/90d; **Analytics** only for `EmailEvents` / `UrlClickEvents` if Sentinel rules require them) | Free in Defender XDR; use unified custom detections before paying for Sentinel streaming. |
| `CloudAppEvents` | [Defender for Cloud Apps](../cloud-apps/defender-for-cloud-apps/README.md), [Purview DLP](../data-security/purview-dlp/README.md) | **Defender XDR default** (or **Data lake** if long retention needed) | Medium to high volume; already free in Defender XDR for 30/90 days. |
| `McasShadowItReporting` | [Defender for Cloud Apps](../cloud-apps/defender-for-cloud-apps/README.md) | **Data lake** | High-volume shadow IT discovery logs used for periodic governance and hunting. |
| `SecurityAlert`, `SecurityIncident`, `AlertInfo`, `AlertEvidence` | All Defender and Purview guides | **Analytics** (free ingestion) | Free alert and incident synchronisation across all Microsoft security services. |
| `BehaviorInfo`, `BehaviorEntities`, `DataSecurityEvents` | [Purview DLP](../data-security/purview-dlp/README.md), [Insider Risk](../data-security/insider-risk/README.md) | **Defender XDR default** | Native Defender XDR hunting tables; `BehaviorInfo`/`BehaviorEntities` aren't available in the Event Streaming API. |
| `MicrosoftPurviewInformationProtection` | [Purview Information Protection](../data-security/information-protection/README.md) | **Analytics** (or **Data lake** if scanner/read volume is high) | Eligible for M365 E5 5 MB/user/day grant; keep label downgrade/removal events alertable. |

### Azure workloads and networking

| Table | Guide | Recommended tier | Why |
|---|---|---|---|
| `AzureActivity` | [Azure Activity](../azure/azure-activity/README.md) | **Analytics** (free ingestion) | Free control-plane audit across all subscriptions; always Analytics. |
| `SecurityRecommendation`, `SecureScores`, `SecurityRegulatoryCompliance`, `SecurityNestedRecommendation` | [Defender for Cloud](../azure/defender-for-cloud/README.md) | **Data lake** | Posture and compliance snapshots exported continuously; rarely need real-time alerting. |
| `AZKVAuditLogs` (or `AzureDiagnostics` `AuditEvent`) | [Azure Key Vault](../azure/key-vault/README.md) | **Analytics** | Secret reads, key operations and purges require near-real-time detection. |
| `AZKVPolicyEvaluationDetailsLogs` | [Azure Key Vault](../azure/key-vault/README.md) | **Data lake** (or skip) | Policy evaluation compliance noise; hunt-only. |
| `StorageBlobLogs`, `StorageFileLogs`, `StorageQueueLogs`, `StorageTableLogs` | [Azure Storage](../azure/storage/README.md) | **Data lake** (Analytics only for small, crown-jewel accounts or DCR-filtered writes/deletes) | High-volume data-plane reads make Analytics expensive; summarise anomalies to Analytics. |
| `AzureDiagnostics` (`SQLSecurityAuditEvents`, `DevOpsOperationsAudit`) | [Azure SQL](../azure/azure-sql/README.md) | **Analytics** (tune action groups; move verbose query logs to **Data lake**) | High-value database auth, permission and schema audit; `DevOpsOperationsAudit` is tiny. |
| `AKSAuditAdmin` | [AKS](../azure/aks/README.md) | **Analytics** | Excludes noisy `get`/`list` verbs; ideal for Kubernetes RBAC, pod exec and secret-write rules. |
| `AKSAudit`, `AKSControlPlane`, `ContainerLogV2` | [AKS](../azure/aks/README.md) | **Data lake** | High-volume full Kubernetes audit, control-plane components (`guard`) and container stdout/stderr. |
| `AZFWThreatIntel`, `AZFWIdpsSignature` | [Azure networking](../azure/network-nsg-flow-firewall/README.md) | **Analytics** | High-fidelity firewall threat intel and IDPS signature hits. |
| `AZFWNetworkRule`, `AZFWApplicationRule`, `AZFWNatRule`, `AZFWDnsQuery`, `AZFWFatFlow` | [Azure networking](../azure/network-nsg-flow-firewall/README.md) | **Data lake** | Very high-volume network traffic logs; promote denies/port-scans with summary rules. |
| `NTANetAnalytics` | [Azure networking](../azure/network-nsg-flow-firewall/README.md) | **Data lake** | VNet flow logs via Traffic Analytics; classic data lake candidate. |
| `AGWFirewallLogs`, `AzureDiagnostics` (`FrontDoorWebApplicationFirewallLog`) | [Azure networking](../azure/network-nsg-flow-firewall/README.md) | **Analytics** (or **Data lake** if untuned Detection mode is noisy) | WAF attack and block events; trim or move noisy rules to lake. |
| `AGWAccessLogs`, `DNSQueryLogs`, `DDoSMitigationFlowLogs` | [Azure networking](../azure/network-nsg-flow-firewall/README.md) | **Data lake** | High-volume HTTP access, DNS resolver and DDoS flow telemetry. |
| `AzureDiagnostics` (`DDoSProtectionNotifications`) | [Azure networking](../azure/network-nsg-flow-firewall/README.md) | **Analytics** | Rare, critical DDoS attack start/stop alerts. |
| `AppServiceAuditLogs`, `AppServiceIPSecAuditLogs` | [App Service & Functions](../azure/app-service-functions/README.md) | **Analytics** | Low-volume publishing/FTP auth and IP restriction audit signals. |
| `AppServiceHTTPLogs`, `FunctionAppLogs`, `AppServicePlatformLogs`, `AppServiceConsoleLogs`, `AppServiceAppLogs` | [App Service & Functions](../azure/app-service-functions/README.md) | **Data lake** | High-volume web and function runtime logs; keep `AppServiceHTTPLogs` in Analytics only for tier-0 internet apps needing TI IP rules. |

### Business apps, AI, DevOps, multi-cloud and Sentinel health

| Table | Guide | Recommended tier | Why |
|---|---|---|---|
| `PowerPlatformAdminActivity`, `PowerAutomateActivity` | [Power Platform](../business-apps/power-platform/README.md) | **Analytics** | Low volume, high signal for DLP tampering, tenant isolation and risky flows. |
| `DataverseActivity`, `FinanceOperationsActivity_CL` | [Dataverse & Dynamics 365](../business-apps/dataverse-dynamics-365/README.md) | **Analytics** (DCR-filter noisy system accounts if Read logs enabled) | Detects audit tampering, mass exports, role abuse and ERP bank-account fraud. |
| `CopilotActivity` | [Copilot Studio](../business-apps/copilot-studio/README.md), [Microsoft 365 Copilot](../ai/microsoft-365-copilot/README.md) | **Analytics** (or **Data lake** if hunt-only) | Required in Analytics for jailbreak and plugin tampering rules; move to lake if only hunting. |
| `AgentsInfo` | [Copilot Studio](../business-apps/copilot-studio/README.md), [Microsoft 365 Copilot](../ai/microsoft-365-copilot/README.md), [Microsoft Foundry](../ai/azure-openai-ai-foundry/README.md) | **Defender XDR default** | Native Agent 365 inventory table (30 days retention). |
| `AzureDiagnostics` (`Audit`, `AzureOpenAIRequestUsage`, `RequestResponse`, `Trace`) | [Microsoft Foundry & Azure OpenAI](../ai/azure-openai-ai-foundry/README.md) | **Analytics** (`Audit`); **Data lake** (`RequestResponse`, `AzureOpenAIRequestUsage`, `Trace`) | Keep auth/key/model admin events in Analytics; route high-volume inference request logs to lake. |
| `GitHubAuditLogsV3_CL`, `GitHubAuditLogsV2_CL`, `GitHubAdvancedSecurityAlerts_CL` | [GitHub](../devops/github/README.md) | **Analytics** (DCR-filter or route high-volume `git.*` events to **Data lake**) | Low-volume org/repo/PAT audit and secret-scanning alerts need fast alerting. |
| `ADOAuditLogs_CL`, `AzureDevOpsAuditing` | [Azure DevOps](../devops/azure-devops/README.md) | **Analytics** | Low volume, high supply-chain security value. |
| `AWSCloudTrail`, `AWSGuardDuty` | [AWS](../multi-cloud/aws/README.md) | **Analytics** | Core AWS control-plane audit and threat detection alerts. |
| `AWSVPCFlow`, `AWSCloudWatch` | [AWS](../multi-cloud/aws/README.md) | **Data lake** | High-volume network flow and operational log streams. |
| `AWSNetworkFirewall` | [AWS](../multi-cloud/aws/README.md) | **Analytics** (alert logs) or **Data lake** (flow logs) | Split alert logs from verbose flow logs. |
| `GCPAuditLogs`, `GoogleCloudSCC` | [Google Cloud](../multi-cloud/google-cloud/README.md) | **Analytics** (filter noisy Data Access logs at GCP sink or route to **Data lake**) | Admin Activity, System Events and Security Command Center findings belong in Analytics. |
| `GCPDNS`, `GCPVPCFlow` | [Google Cloud](../multi-cloud/google-cloud/README.md) | **Data lake** | High-volume DNS and VPC flow telemetry; use summary rules for alerting. |
| `SentinelHealth`, `SentinelAudit` | [Sentinel health](sentinel-health.md) | **Analytics** (`SentinelHealth` is free) | Low-volume SIEM self-monitoring and silent-source alerting. |
| `LAQueryLogs` | [Sentinel health](sentinel-health.md) | **Data lake** (or **Analytics** if alerting on query abuse) | Can grow in busy SOCs; keep in lake unless running query-audit rules. |

## Official links

- [Which logs to ingest directly into the Microsoft Sentinel data lake](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-log-ingestion-guidance)
- [Microsoft Sentinel data lake overview](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-overview)
- [Manage tables, tiers, and retention in Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention)
- [Manage tables, tiers, and retention in ISOC](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention-isoc)
- [What's new in Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/whats-new)
- [Aggregate Microsoft Sentinel data with summary rules](https://learn.microsoft.com/en-us/azure/sentinel/summary-rules)
- [Create KQL jobs in the Microsoft Sentinel data lake](https://learn.microsoft.com/en-us/azure/sentinel/datalake/kql-jobs)
- [Notebook examples for querying the Microsoft Sentinel data lake](https://learn.microsoft.com/en-us/azure/sentinel/datalake/notebook-examples)
- [Log sources to use for the Microsoft Sentinel data lake](https://learn.microsoft.com/en-us/azure/sentinel/basic-logs-use-cases)
- [Plan costs and understand pricing and billing](https://learn.microsoft.com/en-us/azure/sentinel/billing)
- [Microsoft Sentinel pricing](https://azure.microsoft.com/en-us/pricing/details/microsoft-sentinel/)

## Last verified

26 Nov 2026, against Microsoft Learn.
