# Prioritisation

What to onboard first, and why. This page maps each product guide to the ASD ACSC [Priority logs for SIEM ingestion](https://www.cyber.gov.au/sites/default/files/2025-05/Priority%20logs%20for%20SIEM%20ingestion%20-%20Practitioner%20guidance.pdf) practitioner guidance and to Microsoft's [Prioritize data connectors](https://learn.microsoft.com/en-us/azure/sentinel/prioritize-data-connectors) advice.

> Status: draft. The ASD mapping column is a first pass and needs checking against the PDF (tracked in the "Prioritisation matrix" issue).

## How we rank

- **P1, start here.** Identity, email, endpoint and the Azure control plane. These cover the initial access and privilege escalation paths in most incidents, and several are free in Sentinel.
- **P2.** Workload and data sources that matter once P1 is solid: Azure resource logs, SharePoint and Teams, business apps, AI, DevOps and servers.
- **P3.** Specialist or optional sources.

## Matrix

| Guide | Priority | ASD ACSC category | Default tier |
|---|---|---|---|
| [Microsoft Entra ID (sign-in, audit and Graph activity logs)](../identity/entra-id/README.md) | P1 (start here) | Microsoft cloud: Entra ID sign-in and audit logs | To confirm |
| [Microsoft Entra ID Protection (risk detections)](../identity/entra-id-protection/README.md) | P1 (start here) | Microsoft cloud: Entra ID risk | To confirm |
| [Microsoft Defender for Identity](../identity/defender-for-identity/README.md) | P1 (start here) | Identity and domain controllers | To confirm |
| [Active Directory Domain Services (on-premises)](../identity/active-directory-on-prem/README.md) | P1 (start here) | Domain controllers (Windows security events) | To confirm |
| [Active Directory Federation Services (AD FS)](../identity/adfs/README.md) | P1 (start here) | Identity federation | To confirm |
| [Microsoft Entra Internet Access and Private Access (Global Secure Access)](../identity/entra-global-secure-access/README.md) | P3 | Not listed explicitly (to confirm) | To confirm |
| [Microsoft Defender for Endpoint](../endpoint/defender-for-endpoint/README.md) | P1 (start here) | EDR telemetry | To confirm |
| [Windows security event logs (clients)](../endpoint/windows-security-events/README.md) | P1 (start here) | Windows event logs | To confirm |
| [Microsoft Intune](../endpoint/intune/README.md) | P2 | Not listed explicitly (to confirm) | To confirm |
| [Exchange Online](../email-collab/exchange-online/README.md) | P1 (start here) | Microsoft cloud: Unified Audit Log (Exchange) | To confirm |
| [Microsoft Defender for Office 365](../email-collab/defender-for-office-365/README.md) | P1 (start here) | Email security gateway | To confirm |
| [SharePoint Online and OneDrive](../email-collab/sharepoint-onedrive/README.md) | P2 | Microsoft cloud: Unified Audit Log | To confirm |
| [Microsoft Teams](../email-collab/teams/README.md) | P2 | Microsoft cloud: Unified Audit Log | To confirm |
| [Microsoft Purview unified audit log](../email-collab/purview-unified-audit/README.md) | P1 (start here) | Microsoft cloud: Unified Audit Log | To confirm |
| [Microsoft Defender for Cloud Apps](../cloud-apps/defender-for-cloud-apps/README.md) | P2 | Not listed explicitly (to confirm) | To confirm |
| [Azure Activity (control plane)](../azure/azure-activity/README.md) | P1 (start here) | Microsoft cloud: Azure activity logs | To confirm |
| [Microsoft Defender for Cloud](../azure/defender-for-cloud/README.md) | P2 | Cloud security posture alerts | To confirm |
| [Azure Key Vault](../azure/key-vault/README.md) | P2 | Not listed explicitly (to confirm) | To confirm |
| [Azure Storage](../azure/storage/README.md) | P2 | Not listed explicitly (to confirm) | To confirm |
| [Azure SQL Database and Managed Instance](../azure/azure-sql/README.md) | P2 | Not listed explicitly (to confirm) | To confirm |
| [Azure Kubernetes Service (AKS)](../azure/aks/README.md) | P2 | Containers | To confirm |
| [Azure networking (VNet flow logs, Azure Firewall, WAF, DNS)](../azure/network-nsg-flow-firewall/README.md) | P2 | Network devices, firewalls, DNS | To confirm |
| [Azure App Service and Azure Functions](../azure/app-service-functions/README.md) | P3 | Not listed explicitly (to confirm) | To confirm |
| [Microsoft Purview Data Loss Prevention](../data-security/purview-dlp/README.md) | P2 | Not listed explicitly (to confirm) | To confirm |
| [Microsoft Purview Insider Risk Management](../data-security/insider-risk/README.md) | P3 | Not listed explicitly (to confirm) | To confirm |
| [Microsoft Purview Information Protection](../data-security/information-protection/README.md) | P3 | Not listed explicitly (to confirm) | To confirm |
| [Power Platform (Power Apps, Power Automate, admin)](../business-apps/power-platform/README.md) | P2 | Not listed explicitly (to confirm) | To confirm |
| [Microsoft Dataverse and Dynamics 365](../business-apps/dataverse-dynamics-365/README.md) | P2 | Not listed explicitly (to confirm) | To confirm |
| [Microsoft Copilot Studio](../business-apps/copilot-studio/README.md) | P2 | Not listed explicitly (to confirm) | To confirm |
| [Microsoft 365 Copilot](../ai/microsoft-365-copilot/README.md) | P2 | Not listed explicitly (to confirm) | To confirm |
| [Microsoft Foundry (formerly Azure AI Foundry) and Azure OpenAI](../ai/azure-openai-ai-foundry/README.md) | P2 | Not listed explicitly (to confirm) | To confirm |
| [GitHub (Enterprise Cloud)](../devops/github/README.md) | P2 | Not listed explicitly (to confirm) | To confirm |
| [Azure DevOps](../devops/azure-devops/README.md) | P3 | Not listed explicitly (to confirm) | To confirm |
| [Windows Server](../servers/windows-server/README.md) | P2 | Windows event logs | To confirm |
| [Linux (Syslog, CEF and auditd)](../servers/linux-syslog/README.md) | P2 | Linux and network appliances | To confirm |
| [SQL Server (on-premises and IaaS)](../servers/sql-server/README.md) | P3 | Not listed explicitly (to confirm) | To confirm |
| [Amazon Web Services (optional)](../multi-cloud/aws/README.md) | P3 | Not listed explicitly (to confirm) | To confirm |
| [Google Cloud (optional)](../multi-cloud/google-cloud/README.md) | P3 | Not listed explicitly (to confirm) | To confirm |

## Free and low-cost sources

Microsoft lists several data sources as free to ingest into Sentinel, including Azure Activity, Office 365 audit (Exchange, SharePoint, Teams) and alerts from Defender products. Confirm the current list on the [Sentinel pricing page](https://learn.microsoft.com/en-us/azure/sentinel/billing-reduce-costs) before you plan a budget.
