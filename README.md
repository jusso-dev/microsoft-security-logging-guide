# Microsoft security logging guide

Practical, product-by-product guidance on getting high-value security logs from Microsoft products into Microsoft Sentinel and Microsoft Defender XDR.

Microsoft's guidance on what to log is spread across hundreds of product pages. This repo pulls it into one place, with a folder per product that tells a security team which logs matter, which table they land in, how to connect them, what they cost, and which detections to switch on. Every guide links back to the official Microsoft documentation it's based on.

> **Disclaimer.** This is community guidance, not official Microsoft documentation. Microsoft changes table names, connectors and licensing often. Always check the linked Microsoft Learn pages before you rely on anything here, and test in a non-production workspace first.

## Start here: what are you trying to do?

Pick your goal below to jump straight to the right page (or open the full [Start here decision guide](docs/start-here.md)):

| I'm trying to... | Do this |
|---|---|
| **Start a new Sentinel deployment from scratch** | Follow the 4-week rollout in [Start here](docs/start-here.md#quick-onboarding-sequence-first-30-days), starting with free sources in [Prioritisation](docs/prioritisation.md) and [Architecture overview](docs/architecture.md). |
| **Map logging to ASD ACSC Priority Logs** | Use the checked matrix in [Prioritisation](docs/prioritisation.md) (exact May 2025 PDF page references, free sources, default tiers and gaps). |
| **Avoid paying twice for Defender XDR and Sentinel (or fix duplicate alerts)** | Follow the per-product decision table in [Defender XDR vs Sentinel](docs/defender-xdr-vs-sentinel.md). |
| **Harden Defender for Endpoint, Office 365, Identity, Cloud Apps, CSPM, SQL, Storage and other Defender plans** | Follow the product-by-product configuration checklist in [Defender best-practice security configurations](docs/defender-best-practices.md). |
| **Cut Sentinel ingestion costs or estimate spend before onboarding** | Run the 7 queries in [Cost estimation](docs/cost-estimation.md) ([queries/cost/](queries/cost/README.md)) and move hunt-only tables to the data lake using [Data lake tiering](docs/data-lake-tiering.md). |
| **Check if every table is landing and alert when a feed stops** | Run [health-all-tables.kql](queries/validation/health-all-tables.kql) from the [Validation query pack](queries/validation/README.md) and set up `SentinelHealth` alerts with [Sentinel health and audit](docs/sentinel-health.md). |
| **Feed VIP users, leavers or IP ranges into detections** | Set up UEBA `IdentityInfo` and watchlists using [Watchlists and enrichment](docs/watchlists.md). |
| **Onboard a specific product** | Jump to your product group below, or browse [by threat and workload](docs/start-here.md#by-threat-or-workload-im-trying-to-monitor). |

Every product guide follows the same [template](TEMPLATE.md), so once you open one you can jump straight to **High-value log sources**, **Step-by-step setup**, **Validation KQL**, **Out-of-box analytic rules** or **Custom detections**. Check the **Last verified** date at the bottom of each guide.

## Three rules behind every guide

Not every log belongs in the same place. We ask three questions for every source:

- **Does a detection need it in near real time?** If an analytic rule or custom detection reads it, keep it in the Sentinel **Analytics tier**.
- **Is it mostly for hunting, investigations or compliance?** High-volume logs such as flow logs, firewall traffic, proxy logs and verbose storage/Graph logs belong in the **Data lake tier**, where storage is far cheaper and you can promote insights back to Analytics via summary rules or KQL jobs. See [Data lake tiering](docs/data-lake-tiering.md).
- **Is it already in Defender XDR?** Defender XDR keeps 30 days of advanced hunting data (90 days for eligible ISOC plans) at no Sentinel ingestion cost. Streaming raw tables into Sentinel costs money, so do it on purpose. See [Defender XDR vs Sentinel](docs/defender-xdr-vs-sentinel.md).

## Browse by product group

Each group page starts with an **"I'm trying to..."** guide for that area, a table of primary log tables and default tiers, and a link to that group's validation KQL pack.

### [Identity](identity/README.md)

- [Microsoft Entra ID (sign-in, audit and Graph activity logs)](identity/entra-id/README.md) (P1, start here)
- [Microsoft Entra ID Protection (risk detections)](identity/entra-id-protection/README.md) (P1, start here)
- [Microsoft Defender for Identity](identity/defender-for-identity/README.md) (P1, start here)
- [Active Directory Domain Services (on-premises)](identity/active-directory-on-prem/README.md) (P1, start here)
- [Active Directory Federation Services (AD FS)](identity/adfs/README.md) (P1, start here)
- [Microsoft Entra Internet Access and Private Access (Global Secure Access)](identity/entra-global-secure-access/README.md) (P3)

### [Endpoint](endpoint/README.md)

- [Microsoft Defender for Endpoint](endpoint/defender-for-endpoint/README.md) (P1, start here)
- [Windows security event logs (clients)](endpoint/windows-security-events/README.md) (P1, start here)
- [Microsoft Intune](endpoint/intune/README.md) (P2)

### [Email and collaboration](email-collab/README.md)

- [Exchange Online](email-collab/exchange-online/README.md) (P1, start here)
- [Microsoft Defender for Office 365](email-collab/defender-for-office-365/README.md) (P1, start here)
- [SharePoint Online and OneDrive](email-collab/sharepoint-onedrive/README.md) (P2)
- [Microsoft Teams](email-collab/teams/README.md) (P2)
- [Microsoft Purview unified audit log](email-collab/purview-unified-audit/README.md) (P1, start here)

### [Cloud apps](cloud-apps/README.md)

- [Microsoft Defender for Cloud Apps](cloud-apps/defender-for-cloud-apps/README.md) (P2)

### [Azure](azure/README.md)

- [Azure Activity (control plane)](azure/azure-activity/README.md) (P1, start here)
- [Microsoft Defender for Cloud](azure/defender-for-cloud/README.md) (P2)
- [Azure Key Vault](azure/key-vault/README.md) (P2)
- [Azure Storage](azure/storage/README.md) (P2)
- [Azure SQL Database and Managed Instance](azure/azure-sql/README.md) (P2)
- [Azure Kubernetes Service (AKS)](azure/aks/README.md) (P2)
- [Azure networking (VNet flow logs, Azure Firewall, WAF, DNS)](azure/network-nsg-flow-firewall/README.md) (P2)
- [Azure App Service and Azure Functions](azure/app-service-functions/README.md) (P3)

### [Data security](data-security/README.md)

- [Microsoft Purview Data Loss Prevention](data-security/purview-dlp/README.md) (P2)
- [Microsoft Purview Insider Risk Management](data-security/insider-risk/README.md) (P3)
- [Microsoft Purview Information Protection](data-security/information-protection/README.md) (P3)

### [Business applications](business-apps/README.md)

- [Power Platform (Power Apps, Power Automate, admin)](business-apps/power-platform/README.md) (P2)
- [Microsoft Dataverse and Dynamics 365](business-apps/dataverse-dynamics-365/README.md) (P2)
- [Microsoft Copilot Studio](business-apps/copilot-studio/README.md) (P2)

### [AI](ai/README.md)

- [Microsoft 365 Copilot](ai/microsoft-365-copilot/README.md) (P2)
- [Microsoft Foundry (formerly Azure AI Foundry) and Azure OpenAI](ai/azure-openai-ai-foundry/README.md) (P2)

### [DevOps](devops/README.md)

- [GitHub (Enterprise Cloud)](devops/github/README.md) (P2)
- [Azure DevOps](devops/azure-devops/README.md) (P3)

### [Servers](servers/README.md)

- [Windows Server](servers/windows-server/README.md) (P2)
- [Linux (Syslog, CEF and auditd)](servers/linux-syslog/README.md) (P2)
- [SQL Server (on-premises and IaaS)](servers/sql-server/README.md) (P3)

### [Multi-cloud (optional)](multi-cloud/README.md)

- [Amazon Web Services (optional)](multi-cloud/aws/README.md) (P3)
- [Google Cloud (optional)](multi-cloud/google-cloud/README.md) (P3)

## Repository layout

```text
docs/              Start here, architecture, prioritisation, tiering, cost, health and watchlists
queries/           Validation and cost estimation KQL packs
TEMPLATE.md        The structure every product guide follows
CHANGELOG.md       Dated history of manual and nightly automated updates
identity/          Entra ID, ID Protection, Defender for Identity, AD DS, AD FS, Global Secure Access
endpoint/          Defender for Endpoint, Windows security events, Intune
email-collab/      Exchange Online, Defender for Office 365, SharePoint and OneDrive, Teams, Purview audit
cloud-apps/        Defender for Cloud Apps
azure/             Azure Activity, Defender for Cloud, Key Vault, Storage, SQL, AKS, networking, App Service
data-security/     Purview DLP, Insider Risk Management, Information Protection
business-apps/     Power Platform, Dataverse and Dynamics 365, Copilot Studio
ai/                Microsoft 365 Copilot, Microsoft Foundry and Azure OpenAI
devops/            GitHub, Azure DevOps
servers/           Windows Server, Linux, SQL Server
multi-cloud/       AWS and Google Cloud (optional)
```

## Key sources

These are the closest things to a single source of truth, and this repo builds on them:

- ASD ACSC, [Priority logs for SIEM ingestion: practitioner guidance](https://www.cyber.gov.au/sites/default/files/2025-05/Priority%20logs%20for%20SIEM%20ingestion%20-%20Practitioner%20guidance.pdf) (May 2025)
- Microsoft Learn, [Prioritize data connectors for Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/prioritize-data-connectors)
- Microsoft Learn, [Which logs to ingest into the Microsoft Sentinel data lake](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-log-ingestion-guidance)
- Microsoft Zero Trust workshop, [Integrate all Entra logs into SIEM](https://microsoft.github.io/zerotrustassessment/docs/workshop-guidance/identity/RMI_074)

## Keeping it current

This guide is checked automatically every night (`17:30 UTC`) by a GitHub Actions workflow. It scans every linked Microsoft Learn page for newer `updated_at` or `ms.date` timestamps, checks linked `Azure/Azure-Sentinel` Content Hub solution folders for new commits, checks for broken links, and flags guides last verified more than six months ago. When drift is found, affected guides are updated automatically and only pushed to `main` (and published to [GitHub Pages](https://jusso-dev.github.io/microsoft-security-logging-guide/)) if Markdown lint, writing style, Mermaid rendering, link checking and MkDocs strict build checks all pass.

See [CHANGELOG.md](CHANGELOG.md) for a history of updates.

## Contributing

Contributions are very welcome, especially from people running these connectors in production. Read [CONTRIBUTING.md](CONTRIBUTING.md), pick an open issue, and copy [TEMPLATE.md](TEMPLATE.md) when you start a guide. Corrections are just as valuable as new guides, so if a table has been renamed or a link has moved, open a correction issue.

## Licence

- Documentation and diagrams: [Creative Commons Attribution 4.0](LICENSE) (CC BY 4.0). Reuse it in your own runbooks, just credit the source.
- Code (KQL queries, scripts, workflows): [MIT](LICENSE-CODE).

Microsoft, Microsoft Sentinel, Microsoft Defender and other product names are trademarks of Microsoft Corporation. This project isn't affiliated with or endorsed by Microsoft.
