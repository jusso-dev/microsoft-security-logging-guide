# Prioritisation

> Status: verified. Last verified: 21 Nov 2026.

What to onboard first, and why. This matrix maps every product guide in this repo to the May 2025 ASD ACSC [Priority logs for SIEM ingestion: practitioner guidance](https://www.cyber.gov.au/sites/default/files/2025-05/Priority%20logs%20for%20SIEM%20ingestion%20-%20Practitioner%20guidance.pdf) PDF (with exact page references) and to Microsoft's [Prioritize data connectors for Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/prioritize-data-connectors) guidance.

## How we rank

- **P1, start here.** Identity, email, endpoint and the Azure control plane. These cover the initial access, persistence and privilege escalation paths in most incidents, and several are free in Sentinel or already included in Defender XDR.
- **P2.** High-value workload and data sources once P1 is solid: Azure resource logs, SharePoint and Teams, Purview DLP, business apps, AI, GitHub and servers.
- **P3.** Specialist, compliance-driven or optional sources.

Note on PDF numbering: the ASD ACSC PDF table of contents (p. 3) numbers sections 1 to 13, while the body headings shift by one after section 8 (Cloud platform logging, p. 22), running to section 14 (Apple macOS endpoint logs, p. 31). Page numbers below cite the actual PDF page.

## Prioritisation matrix

| Guide | Priority | ASD ACSC category (PDF page) | Free in Sentinel / Defender XDR | Default tier |
|---|---|---|---|---|
| [Microsoft Entra ID (sign-in, audit and Graph activity logs)](../identity/entra-id/README.md) | P1 (start here) | Critical Azure service and app logs: Signin, Managed Identity, Non-Interactive, Service Principal, Unified Audit, Breakglass (pp. 24-25) | `EntraIdSignInEvents` and `EntraIdSpnSignInEvents` free in Defender XDR (P2); Sentinel tables paid | Analytics (`SigninLogs`, `AuditLogs`, `AADServicePrincipalSignInLogs`); Data lake (`MicrosoftGraphActivityLogs`, `AADProvisioningLogs`) |
| [Microsoft Entra ID Protection (risk detections)](../identity/entra-id-protection/README.md) | P1 (start here) | Cloud platform logging: authentication and risky sign-ins (pp. 22, 25) | `SecurityAlert` (IPC) free in Sentinel; `AADUserRiskEvents` and `AADRiskyUsers` paid | Analytics |
| [Microsoft Defender for Identity](../identity/defender-for-identity/README.md) | P1 (start here) | Microsoft Domain Controller and AD Security Logs (pp. 12-17) | `SecurityAlert` and `SecurityIncident` free in Sentinel; `Identity*` tables free in Defender XDR (30d / 90d ISOC) | Defender XDR default; Analytics if streamed |
| [Active Directory Domain Services (on-premises)](../identity/active-directory-on-prem/README.md) | P1 (start here) | Microsoft Domain Controller and AD Security Logs (pp. 12-17, GPO annex pp. 34-37) | Paid (500 MB/server/day grant with Defender for Servers P2) | Analytics (`Common` + XPath 4769/4776) |
| [Active Directory Federation Services (AD FS)](../identity/adfs/README.md) | P1 (start here) | Microsoft Domain Controller: Federation Services (p. 13); Critical Azure: ADFS Signin Log (p. 25) | Paid | Analytics |
| [Microsoft Entra Internet Access and Private Access (Global Secure Access)](../identity/entra-global-secure-access/README.md) | P3 | Network device logs: Web Proxies and VPN (pp. 10-11) | Paid | Data lake (`NetworkAccessTraffic`); Analytics (`RemoteNetworkHealthLogs` or summary rules) |
| [Microsoft Defender for Endpoint](../endpoint/defender-for-endpoint/README.md) | P1 (start here) | Endpoint detection and response (EDR) logs (pp. 7-8) | `SecurityAlert` and `SecurityIncident` free in Sentinel; `Device*` free in Defender XDR (30d / 90d ISOC) | Defender XDR default; Data lake if long retention needed |
| [Windows security event logs (clients)](../endpoint/windows-security-events/README.md) | P1 (start here) | Microsoft Windows endpoint logs (pp. 17-20, GPO annex p. 35) | Paid | Analytics (filtered via DCR; skip if Defender for Endpoint already covers telemetry) |
| [Microsoft Intune](../endpoint/intune/README.md) | P2 | Mobile device management (pp. 28-29) | Paid | Analytics (`IntuneAuditLogs`, `IntuneOperationalLogs`); Data lake (`IntuneDevices`, `IntuneDeviceComplianceOrg`) |
| [Exchange Online](../email-collab/exchange-online/README.md) | P1 (start here) | Critical Azure service and app logs: Microsoft Office 365 Unified Audit Log (p. 25) | `OfficeActivity` (Exchange) free in Sentinel | Analytics |
| [Microsoft Defender for Office 365](../email-collab/defender-for-office-365/README.md) | P1 (start here) | Network device logs: Mail Appliance (p. 11) | `SecurityAlert` and `SecurityIncident` free in Sentinel; `Email*` and `UrlClickEvents` free in Defender XDR (30d / 90d ISOC) | Defender XDR default; Analytics for `EmailEvents` and `UrlClickEvents` if Sentinel rules read them |
| [SharePoint Online and OneDrive](../email-collab/sharepoint-onedrive/README.md) | P2 | Critical Azure service and app logs: Microsoft Office 365 Unified Audit Log (p. 25) | `OfficeActivity` (SharePoint) free in Sentinel | Analytics |
| [Microsoft Teams](../email-collab/teams/README.md) | P2 | Critical Azure service and app logs: Microsoft Office 365 Unified Audit Log (p. 25) | `OfficeActivity` (Teams) free in Sentinel | Analytics |
| [Microsoft Purview unified audit log](../email-collab/purview-unified-audit/README.md) | P1 (start here) | Critical Azure service and app logs: Microsoft Office 365 Unified Audit Log (pp. 24-25) | `OfficeActivity` (Exchange, SharePoint, Teams) free in Sentinel; other Purview feeds paid | Analytics |
| [Microsoft Defender for Cloud Apps](../cloud-apps/defender-for-cloud-apps/README.md) | P2 | Cloud platform logging: third-party SaaS authentication and API activity (p. 22) | `SecurityAlert` and `SecurityIncident` free in Sentinel; `CloudAppEvents` free in Defender XDR (30d / 90d ISOC) | Defender XDR default; Data lake (`McasShadowItReporting`) |
| [Azure Activity (control plane)](../azure/azure-activity/README.md) | P1 (start here) | Critical Azure service and app logs: Azure Audit Log (p. 25) | `AzureActivity` free in Sentinel | Analytics |
| [Microsoft Defender for Cloud](../azure/defender-for-cloud/README.md) | P2 | Cloud platform logging: cloud service security controls (p. 22) | `SecurityAlert` free in Sentinel; continuous export tables paid | Analytics (`SecurityAlert`); Data lake (`SecurityRecommendation`, `SecureScores`, `SecurityRegulatoryCompliance`) |
| [Azure Key Vault](../azure/key-vault/README.md) | P2 | Cloud platform logging: administrative changes, keys and secrets (pp. 22-23) | Paid | Analytics (`AZKVAuditLogs` or `AzureDiagnostics`) |
| [Azure Storage](../azure/storage/README.md) | P2 | Critical Azure service and app logs: Azure Storage Container Log (p. 25) | Paid | Data lake (`StorageBlobLogs`, `StorageFileLogs`, `StorageQueueLogs`, `StorageTableLogs`), or Analytics for sensitive accounts |
| [Azure SQL Database and Managed Instance](../azure/azure-sql/README.md) | P2 | Database logs (p. 27) | `SecurityAlert` (Defender for SQL) free; audit tables paid | Analytics (`AzureDiagnostics` `SQLSecurityAuditEvents`, `DevOpsOperationsAudit`) or Data lake for high-volume query logs |
| [Azure Kubernetes Service (AKS)](../azure/aks/README.md) | P2 | Container logs (pp. 26-27) | `SecurityAlert` (Defender for Containers) free; AKS logs paid | Analytics (`AKSAuditAdmin`); Data lake (`AKSAudit`, `ContainerLogV2`, `AKSControlPlane`) |
| [Azure networking (VNet flow logs, Azure Firewall, WAF, DNS)](../azure/network-nsg-flow-firewall/README.md) | P2 | Network device logs: Firewall, Border Firewall, IDS/IPS, Application Layer Gateways (pp. 9-10) | Paid | Data lake (`NTANetAnalytics`, `AZFWNetworkRule`, `AZFWApplicationRule`, `AZFWDnsQuery`, `DNSQueryLogs`, `DDoSMitigationFlowLogs`, WAF logs); Analytics (`AZFWThreatIntel`, `AZFWIdpsSignature`, `DDoSProtectionNotifications`) |
| [Azure App Service and Azure Functions](../azure/app-service-functions/README.md) | P3 | Cloud platform logging: internet-facing services (p. 22) | Paid | Analytics (`AppServiceAuditLogs`, `AppServiceIPSecAuditLogs`); Data lake (`AppServiceHTTPLogs`, `AppServiceAppLogs`, `FunctionAppLogs`) |
| [Microsoft Purview Data Loss Prevention](../data-security/purview-dlp/README.md) | P2 | Cloud platform logging: compliance events and critical data holdings (p. 22) | `SecurityAlert` and `SecurityIncident` via Defender XDR free; `OfficeActivity` free | Analytics (alerts and policy audit) |
| [Microsoft Purview Insider Risk Management](../data-security/insider-risk/README.md) | P3 | Cloud platform logging: compliance events (p. 22) | `SecurityAlert` and `SecurityIncident` via Defender XDR free | Analytics (alerts) |
| [Microsoft Purview Information Protection](../data-security/information-protection/README.md) | P3 | Cloud platform logging: compliance events and data holdings (p. 22) | `OfficeActivity` free; `MicrosoftPurviewInformationProtection` paid (E5 grant eligible) | Data lake or Analytics depending on rules |
| [Power Platform (Power Apps, Power Automate, admin)](../business-apps/power-platform/README.md) | P2 | Cloud platform logging: SaaS admin, permissions and API activity (p. 22) | Paid | Analytics (`PowerPlatformAdminActivity`, `PowerAutomateActivity`) |
| [Microsoft Dataverse and Dynamics 365](../business-apps/dataverse-dynamics-365/README.md) | P2 | Cloud platform logging: critical data holdings and database/SaaS access (pp. 22, 27) | Paid | Analytics (`DataverseActivity` CRUD and access); Data lake or DCR filter if Read logs enabled |
| [Microsoft Copilot Studio](../business-apps/copilot-studio/README.md) | P2 | Cloud platform logging: SaaS configuration and API activity (p. 22) | `AgentsInfo` in Defender XDR (Agent 365 licence); Sentinel tables paid | Analytics (`CopilotActivity`, Dataverse `bot` audit) |
| [Microsoft 365 Copilot](../ai/microsoft-365-copilot/README.md) | P2 | Cloud platform logging: SaaS user and API activity (p. 22) | Paid | Analytics (`CopilotActivity`), or Data lake if hunt-only |
| [Microsoft Foundry (formerly Azure AI Foundry) and Azure OpenAI](../ai/azure-openai-ai-foundry/README.md) | P2 | Cloud platform logging: cloud APIs and internet-facing services (p. 22) | `AzureActivity` and Defender for AI `SecurityAlert` free; diagnostic logs paid | Analytics (`Audit` category, `AzureActivity`, `SecurityAlert`); Data lake (`RequestResponse` / usage logs) |
| [GitHub (Enterprise Cloud)](../devops/github/README.md) | P2 | Cloud platform logging: third-party SaaS authentication, permissions and admin changes (p. 22) | Paid (`SecurityAlert` from Defender for Cloud DevOps free) | Analytics (`GitHubAuditLogsV3_CL` or `GitHubAuditLogsV2_CL`, `GitHubAdvancedSecurityAlerts_CL`) |
| [Azure DevOps](../devops/azure-devops/README.md) | P3 | Cloud platform logging: admin changes, permissions and CI/CD pipelines (p. 22) | Paid (`SecurityAlert` from Defender for Cloud DevOps free) | Analytics (`ADOAuditLogs_CL` or `AzureDevOpsAuditing`) |
| [Windows Server](../servers/windows-server/README.md) | P2 | Microsoft Windows endpoint logs (pp. 17-20); Windows DNS server analytic event logs (p. 29); Virtual Machine Windows OS logs (p. 25) | Paid (500 MB/server/day grant with Defender for Servers P2) | Analytics (`SecurityEvent`, `Event`, `MDCFileIntegrityMonitoringEvents`); Data lake (`ASimDnsActivityLogs`, `W3CIISLog`) |
| [Linux (Syslog, CEF and auditd)](../servers/linux-syslog/README.md) | P2 | Linux endpoint auditing logs (pp. 29-31); Network device logs via Syslog/CEF (pp. 9-11); Virtual Machine Linux OS logs (p. 25) | Paid (500 MB/server/day grant with Defender for Servers P2) | Analytics (`Syslog` auth/authpriv, high-value `CommonSecurityLog` alerts); Data lake (verbose firewall/proxy `CommonSecurityLog`) |
| [SQL Server (on-premises and IaaS)](../servers/sql-server/README.md) | P3 | Database logs (p. 27) | `SecurityAlert` (Defender for SQL) free; AMA logs paid | Analytics (`SecurityEvent` / `Event` ID 33205) |
| [Amazon Web Services (optional)](../multi-cloud/aws/README.md) | P3 | Amazon Web Services logs: CloudTrail, S3, Secrets Manager, EC2, VPC, IAM, STS, RDS, Lambda (pp. 23-24) | Paid | Analytics (`AWSCloudTrail`, `AWSGuardDuty`); Data lake (`AWSVPCFlow`, S3 access logs) |
| [Google Cloud (optional)](../multi-cloud/google-cloud/README.md) | P3 | Google Cloud Platform (GCP) logs: Admin Activity, Login, VPC Firewall, VPC Flow, Storage (p. 25) | Paid | Analytics (`GCPAuditLogs`, Security Command Center); Data lake (VPC Flow and verbose Data Access logs) |

## ASD ACSC categories not yet covered by a guide

The May 2025 ASD ACSC PDF lists four categories that do not have a dedicated product guide in this repo yet:

| ASD ACSC category | PDF pages | Current coverage and gap |
|---|---|---|
| **Virtualisation system logs** (VM creation, deployment, migration, hypervisor objects) | pp. 20-21 | Azure VM lifecycle events are captured by [Azure Activity](../azure/azure-activity/README.md). On-premises Hyper-V and VMware ESXi / vCenter logs have no dedicated guide yet (forward ESXi/vCenter via Syslog/CEF using [Linux Syslog/CEF](../servers/linux-syslog/README.md)). |
| **Operational technology (OT) logging** | pp. 21-22 | No Microsoft Defender for IoT / OT guide in this repo yet. Defender for IoT alerts (`SecurityAlert`) are a free Sentinel data source. |
| **Google Workspace (GWS) logs** | p. 26 | Out of scope for a Microsoft-focused repo, though Sentinel ships a Google Workspace content solution if you run GWS alongside Microsoft workloads. |
| **Apple macOS endpoint logs** (Unified Logging, `syspolicyd`, `auditd`, Jamf) | pp. 31-33 | [Microsoft Defender for Endpoint](../endpoint/defender-for-endpoint/README.md) provides macOS EDR telemetry (`Device*` tables), and [Microsoft Intune](../endpoint/intune/README.md) covers MDM compliance, but there is no dedicated macOS Unified Logging / Jamf collection guide yet. |

## Free data sources and data grants

Start with sources that cost zero Sentinel ingestion ([free data sources](https://learn.microsoft.com/en-us/azure/sentinel/billing#free-data-sources)):

- **Always free in Sentinel:** `AzureActivity`, `SentinelHealth`, `OfficeActivity` (Exchange Online, SharePoint Online and Microsoft Teams audit logs), and `SecurityAlert` / `SecurityIncident` from Microsoft Defender XDR, Defender for Cloud, Defender for Endpoint, Defender for Office 365, Defender for Identity, Defender for Cloud Apps, Defender for IoT and Entra ID Protection.
- **Included in Defender XDR (no Sentinel ingestion needed):** `Device*`, `Email*`, `UrlClickEvents`, `Identity*`, `CloudAppEvents`, `EntraIdSignInEvents` (P2) and `EntraIdSpnSignInEvents` (P2) stay in Defender XDR advanced hunting for 30 days by default, or up to 90 days for eligible ISOC customers from 15 November 2026 ([manage tables in ISOC](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention-isoc)).
- **Data grants:** Microsoft 365 E5 / A5 / F5 / G5 gives a 5 MB/user/day Sentinel grant across eligible Microsoft 365/Entra/Defender tables, and Defender for Servers Plan 2 gives 500 MB/server/day across eligible Windows and Linux security tables. Check your entitlements on the [Sentinel billing page](https://learn.microsoft.com/en-us/azure/sentinel/billing) and [reduce costs](https://learn.microsoft.com/en-us/azure/sentinel/billing-reduce-costs).

## Official links

- [ASD ACSC: Priority logs for SIEM ingestion: practitioner guidance (May 2025 PDF)](https://www.cyber.gov.au/sites/default/files/2025-05/Priority%20logs%20for%20SIEM%20ingestion%20-%20Practitioner%20guidance.pdf)
- [Prioritize data connectors for Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/prioritize-data-connectors)
- [Plan costs and understand pricing and billing](https://learn.microsoft.com/en-us/azure/sentinel/billing)
- [Reduce costs for Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/billing-reduce-costs)
- [Manage tables, tiers, and retention in ISOC](https://learn.microsoft.com/en-us/azure/sentinel/manage-table-tiers-retention-isoc)

## Last verified

21 Nov 2026, against the May 2025 ASD ACSC practitioner guidance PDF and Microsoft Learn.
