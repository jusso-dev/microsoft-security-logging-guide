# Start here: what are you trying to do?

> Status: verified. Last verified: 21 Nov 2026.

Use this page to jump straight to the exact guide, decision table or KQL query for your goal, without reading the whole repo front to back.

## By outcome ("I'm trying to...")

| I'm trying to... | Do this |
|---|---|
| **Set up Microsoft Sentinel from scratch** | 1. Skim [Architecture overview](architecture.md) to see how logs flow.<br>2. Turn on the **free** sources first (`AzureActivity`, `OfficeActivity`, Defender XDR alerts) using [Prioritisation](prioritisation.md).<br>3. Work through the **P1 (start here)** guides in Identity, Email, Endpoint and Azure.<br>4. Run [health-all-tables.kql](../queries/validation/health-all-tables.kql) to prove every table is landing. |
| **Align logging to the ASD ACSC Priority Logs list** | Open [Prioritisation](prioritisation.md). Every product guide is mapped to the May 2025 ASD ACSC practitioner guidance PDF with exact page numbers, free sources, default tiers and explicit gaps. |
| **Stop paying twice for Defender XDR and Sentinel (or fix duplicate incidents)** | Read [Defender XDR vs Sentinel](defender-xdr-vs-sentinel.md). Use its per-product decision table to keep raw Defender tables in Defender XDR by default, turn off legacy alert connectors, and pick one format per rule (unified custom detection or Sentinel analytic rule). |
| **Harden Defender for Endpoint, MDO, MDI, MDCA, CSPM, Defender for SQL, Storage, Servers or Containers** | Follow [Defender best-practice security configurations](defender-best-practices.md) for recommended production settings (Tamper Protection, ASR, EDR in block mode, Preset Security Policies, CSPM agentless scanning, SQL Vulnerability Assessment, Storage Malware Scanning and more). |
| **Cut my Sentinel ingestion bill without losing detections** | 1. Run [01-gb-per-table.kql](../queries/cost/01-gb-per-table.kql) and [05-top-noisy-events-and-hosts.kql](../queries/cost/05-top-noisy-events-and-hosts.kql) from [Cost estimation](cost-estimation.md).<br>2. Move hunt-only high-volume tables to the **Data lake tier** using [Data lake tiering](data-lake-tiering.md).<br>3. Check if a commitment tier fits with [06-commitment-tier-sizing.kql](../queries/cost/06-commitment-tier-sizing.kql). |
| **Estimate cost before onboarding a noisy new source** | Follow the 31-day 10 GB/day trial workspace method in [Cost estimation](cost-estimation.md), or run [07-xdr-streaming-cost-preview.kql](../queries/cost/07-xdr-streaming-cost-preview.kql) directly in Defender XDR advanced hunting before turning on raw table streaming. |
| **Check if every table is landing and alert when a source goes quiet** | Run [health-all-tables.kql](../queries/validation/health-all-tables.kql) (or a single group file from [Validation query pack](../queries/validation/README.md)), then set up `SentinelHealth` and silent-source alerts using [Sentinel health and audit](sentinel-health.md). |
| **Enrich alerts with VIP users, leavers or corporate IP ranges** | Follow [Watchlists and enrichment](watchlists.md) to enable UEBA (`IdentityInfo`) and keep `VIPUsers`, `TerminatedEmployees` and `NetworkAddresses` watchlists current. |
| **Decide whether a table belongs in Analytics or Data lake tier** | Look up the exact table in [Data lake tiering](data-lake-tiering.md). It covers every active table across all 38 product guides, the September 2026 Table management flow, and summary rules / KQL jobs for promoting lake insights back to Analytics. |
| **Prepare for Sentinel retiring in the Azure portal (31 March 2027)** | Read the Defender portal sections of [Architecture overview](architecture.md) and [Defender XDR vs Sentinel](defender-xdr-vs-sentinel.md). Every product guide in this repo already uses Defender portal navigation. |

## By threat or workload ("I'm trying to monitor...")

| I'm trying to monitor... | Start with these guides |
|---|---|
| **Account takeover, MFA fatigue, token theft or OAuth app abuse** | [Microsoft Entra ID](../identity/entra-id/README.md), [Microsoft Entra ID Protection](../identity/entra-id-protection/README.md) |
| **On-premises Active Directory, Kerberoasting, DCSync or AD FS** | [Microsoft Defender for Identity](../identity/defender-for-identity/README.md), [Active Directory Domain Services](../identity/active-directory-on-prem/README.md), [AD FS](../identity/adfs/README.md) |
| **Endpoints, ransomware execution, or mobile/device compliance** | [Microsoft Defender for Endpoint](../endpoint/defender-for-endpoint/README.md), [Windows security event logs (clients)](../endpoint/windows-security-events/README.md), [Microsoft Intune](../endpoint/intune/README.md) |
| **Phishing, BEC, inbox forwarding rules or SharePoint/Teams exfiltration** | [Exchange Online](../email-collab/exchange-online/README.md), [Microsoft Defender for Office 365](../email-collab/defender-for-office-365/README.md), [SharePoint Online and OneDrive](../email-collab/sharepoint-onedrive/README.md), [Microsoft Teams](../email-collab/teams/README.md), [Purview unified audit log](../email-collab/purview-unified-audit/README.md) |
| **Shadow IT, OAuth apps and third-party SaaS** | [Microsoft Defender for Cloud Apps](../cloud-apps/defender-for-cloud-apps/README.md), [Global Secure Access](../identity/entra-global-secure-access/README.md) |
| **Sensitive data leaving via USB, email, cloud apps or insiders** | [Microsoft Purview DLP](../data-security/purview-dlp/README.md), [Purview Insider Risk Management](../data-security/insider-risk/README.md), [Purview Information Protection](../data-security/information-protection/README.md) |
| **Azure subscriptions, keys, storage, SQL, AKS, firewalls or web apps** | Start with [Azure Activity](../azure/azure-activity/README.md) and [Defender for Cloud](../azure/defender-for-cloud/README.md), then pick workloads in [Azure](../azure/README.md) |
| **Citizen-developer apps, flows, Dynamics 365 and custom AI agents** | [Power Platform](../business-apps/power-platform/README.md), [Dataverse and Dynamics 365](../business-apps/dataverse-dynamics-365/README.md), [Copilot Studio](../business-apps/copilot-studio/README.md) |
| **Microsoft 365 Copilot and Azure OpenAI / Microsoft Foundry AI workloads** | [Microsoft 365 Copilot](../ai/microsoft-365-copilot/README.md), [Microsoft Foundry and Azure OpenAI](../ai/azure-openai-ai-foundry/README.md) |
| **Source code repos, PAT abuse and CI/CD supply chain** | [GitHub (Enterprise Cloud)](../devops/github/README.md), [Azure DevOps](../devops/azure-devops/README.md) |
| **Windows Server, Linux hosts, Syslog/CEF network appliances or SQL Server** | [Windows Server](../servers/windows-server/README.md), [Linux (Syslog, CEF and auditd)](../servers/linux-syslog/README.md), [SQL Server](../servers/sql-server/README.md) |
| **AWS or Google Cloud alongside Microsoft** | [Amazon Web Services](../multi-cloud/aws/README.md), [Google Cloud](../multi-cloud/google-cloud/README.md) |

## Quick onboarding sequence (first 30 days)

1. **Week 1 (free + high signal):** Connect [Azure Activity](../azure/azure-activity/README.md), [Defender XDR alerts](defender-xdr-vs-sentinel.md), [Exchange Online](../email-collab/exchange-online/README.md) / [Purview unified audit](../email-collab/purview-unified-audit/README.md), and [Sentinel health](sentinel-health.md).
2. **Week 2 (identity + endpoint P1):** Connect [Microsoft Entra ID](../identity/entra-id/README.md), [Entra ID Protection](../identity/entra-id-protection/README.md), [Defender for Identity](../identity/defender-for-identity/README.md), [AD DS](../identity/active-directory-on-prem/README.md) (if hybrid), and confirm [Defender for Endpoint](../endpoint/defender-for-endpoint/README.md) and [Defender for Office 365](../email-collab/defender-for-office-365/README.md) detections.
3. **Week 3 (measure & tune):** Run the [Cost estimation query pack](../queries/cost/README.md) and [Validation query pack](../queries/validation/README.md). Route verbose tables to the Data lake tier per [Data lake tiering](data-lake-tiering.md) and populate core watchlists per [Watchlists and enrichment](watchlists.md).
4. **Week 4 (P2 workloads):** Add Azure workloads ([Key Vault](../azure/key-vault/README.md), [Storage](../azure/storage/README.md), [Azure SQL](../azure/azure-sql/README.md), [AKS](../azure/aks/README.md), [Azure networking](../azure/network-nsg-flow-firewall/README.md)), [Purview DLP](../data-security/purview-dlp/README.md), [Power Platform](../business-apps/power-platform/README.md), [AI](../ai/README.md), [GitHub](../devops/github/README.md) and [Servers](../servers/README.md).
