# Microsoft recommended security configurations (all products)

> Status: verified. Last verified: 21 Nov 2026.

Every product guide in this repo includes a **Best-practice security configuration** section right after setup. This page pulls all 38 products into one scannable cheat sheet so you can see the top controls Microsoft recommends before (or while) you turn on logging.

For deep-dive hardening across all Microsoft Defender products (MDE, MDO, MDI, MDCA, Defender CSPM, Defender for Servers, SQL, Storage, Containers, Key Vault, App Service, APIs, Resource Manager and AI Services), see [Defender best-practice security configurations](defender-best-practices.md).

## Identity

| Product | Top Microsoft recommended controls | Guide section |
|---|---|---|
| **Microsoft Entra ID** | Phishing-resistant MFA + Conditional Access (block legacy auth), PIM for all admin roles, two cloud-only FIDO2 break-glass accounts, disable unrestricted end-user OAuth consent | [Entra ID](../identity/entra-id/README.md#best-practice-security-configuration) |
| **Microsoft Entra ID Protection** | Conditional Access user-risk policy (password change + MFA on High) and sign-in risk policy (MFA/block on Medium+); workload identity risk policy if licensed | [Entra ID Protection](../identity/entra-id-protection/README.md#best-practice-security-configuration) |
| **Microsoft Defender for Identity** | Sensor on 100% of DCs, AD FS and AD CS servers; required `4662`/`4776` auditing; Sensitive and Honeytoken tags; gMSA action account + automatic attack disruption | [Defender for Identity](../identity/defender-for-identity/README.md#best-practice-security-configuration) |
| **Active Directory (on-premises)** | Tier-0 isolation & PAWs, Protected Users group, minimal permanent Domain Admins, enforce LDAP/SMB signing & channel binding, disable NTLMv1/SMBv1 and unconstrained delegation | [AD DS](../identity/active-directory-on-prem/README.md#best-practice-security-configuration) |
| **AD FS** | Enable Extranet Smart Lockout, treat AD FS servers as Tier-0 with MDI sensors, disable unused legacy endpoints, plan migration to Entra cloud auth | [AD FS](../identity/adfs/README.md#best-practice-security-configuration) |
| **Global Secure Access** | Conditional Access Compliant network check (prevents token replay outside tunnel), web filtering, least-privilege Private Access segments, source IP restoration | [Global Secure Access](../identity/entra-global-secure-access/README.md#best-practice-security-configuration) |

## Endpoint

| Product | Top Microsoft recommended controls | Guide section |
|---|---|---|
| **Microsoft Defender for Endpoint** | Tamper Protection On, EDR in block mode On, ASR rules (Audit then Block), Network Protection & PUA Block, Block at First Sight (High/High+), AIR Full, automatic attack disruption | [Defender for Endpoint](../endpoint/defender-for-endpoint/README.md#best-practice-security-configuration) |
| **Windows clients** | Intune Windows & MDE Security Baselines, Credential Guard + HVCI, Windows LAPS + remove local admin rights, BitLocker + PowerShell `4104` logging | [Windows clients](../endpoint/windows-security-events/README.md#best-practice-security-configuration) |
| **Microsoft Intune** | Enrolment restrictions, compliance policies enforced by Conditional Access, Multi-Admin Approval (MAA) for wipes/scripts, scoped RBAC | [Intune](../endpoint/intune/README.md#best-practice-security-configuration) |

## Email, collaboration and cloud apps

| Product | Top Microsoft recommended controls | Guide section |
|---|---|---|
| **Exchange Online** | Keep Basic Auth & unused SMTP AUTH disabled, block automatic external forwarding, use Exchange RBAC for Applications, enforce SPF/DKIM/DMARC (`p=reject`) | [Exchange Online](../email-collab/exchange-online/README.md#best-practice-security-configuration) |
| **Microsoft Defender for Office 365** | Standard preset for all users & Strict preset for execs/admins, Safe Links (click tracking on, no click-through), Safe Attachments Dynamic Delivery + SPO/Teams, ZAP On | [Defender for Office 365](../email-collab/defender-for-office-365/README.md#best-practice-security-configuration) |
| **SharePoint Online & OneDrive** | Restrict Anyone/anonymous links (short expiry), default to Specific people, browser-only on unmanaged devices, idle session sign-out, sensitivity labels on sites | [SharePoint & OneDrive](../email-collab/sharepoint-onedrive/README.md#best-practice-security-configuration) |
| **Microsoft Teams** | Allow-list external federated domains (instead of open federation), require approval for third-party apps, enforce meeting lobby, Safe Links & ZAP for Teams | [Teams](../email-collab/teams/README.md#best-practice-security-configuration) |
| **Microsoft Purview unified audit** | Confirm `UnifiedAuditLogIngestionEnabled = True`, set explicit Audit (Premium) retention policies, grant analysts View-Only Audit Logs | [Purview unified audit](../email-collab/purview-unified-audit/README.md#best-practice-security-configuration) |
| **Microsoft Defender for Cloud Apps** | Connect M365 + cloud/SaaS apps, enable native MDE Cloud Discovery, turn on App Governance OAuth policies, Conditional Access App Control session policies | [Defender for Cloud Apps](../cloud-apps/defender-for-cloud-apps/README.md#best-practice-security-configuration) |

## Azure

| Product | Top Microsoft recommended controls | Guide section |
|---|---|---|
| **Azure Activity** | Management-group Azure Policy (Microsoft Cloud Security Benchmark + diagnostic settings), Entra PIM for Owner/Contributor, `CanNotDelete` locks on critical workspaces | [Azure Activity](../azure/azure-activity/README.md#best-practice-security-configuration) |
| **Microsoft Defender for Cloud & CSPM** | Defender CSPM (agentless CVE + secret scanning, Attack Path Analysis, Sensitive data discovery), Governance rules with SLAs, core workload plans + multi-cloud/DevOps onboarding | [Defender for Cloud](../azure/defender-for-cloud/README.md#best-practice-security-configuration) |
| **Azure Key Vault** | Defender for Key Vault, soft-delete + purge protection on all prod vaults, Azure RBAC (not legacy access policies), Private Endpoints | [Key Vault](../azure/key-vault/README.md#best-practice-security-configuration) |
| **Azure Storage** | Modern Defender for Storage + Malware Scanning on upload accounts (Event Grid quarantine), Sensitive Data Threat Detection, disable anonymous blob & shared key access, TLS 1.2+ | [Storage](../azure/storage/README.md#best-practice-security-configuration) |
| **Azure SQL** | Defender for Azure SQL, Express Vulnerability Assessment baseline, Advanced Threat Protection, Entra-only auth, disable Allow Azure Services, Private Endpoints + TLS 1.2+ | [Azure SQL](../azure/azure-sql/README.md#best-practice-security-configuration) |
| **Azure Kubernetes Service (AKS)** | Defender for Containers (agentless + eBPF sensor), ACR image scanning, Azure Policy Kubernetes restricted pod security, Entra RBAC (`--disable-local-accounts`), private API server | [AKS](../azure/aks/README.md#best-practice-security-configuration) |
| **Azure networking** | Azure Firewall Premium (Threat Intel & IDPS Alert and deny), WAF in Prevention mode, migrate NSG flow logs to VNet flow logs before 30 Sep 2027, DDoS Network Protection | [Azure networking](../azure/network-nsg-flow-firewall/README.md#best-practice-security-configuration) |
| **Azure App Service & Functions** | Defender for App Service, disable FTP & SCM basic auth (deploy via Entra/OIDC), HTTPS-only, TLS 1.2+, Managed Identities + Key Vault references | [App Service & Functions](../azure/app-service-functions/README.md#best-practice-security-configuration) |

## Data security

| Product | Top Microsoft recommended controls | Guide section |
|---|---|---|
| **Microsoft Purview DLP** | Progressive rollout (Simulation → Block with override → Block), cover M365 + Endpoint DLP + MDCA, protect DLP admin roles with PIM | [Purview DLP](../data-security/purview-dlp/README.md#best-practice-security-configuration) |
| **Microsoft Purview Insider Risk** | Separate Admin vs Investigator roles, keep pseudonymisation in Purview (HR/Legal sign-off before XDR sharing), connect HR leaver feed, use Adaptive Protection | [Insider Risk](../data-security/insider-risk/README.md#best-practice-security-configuration) |
| **Microsoft Purview Information Protection** | Keep taxonomy to 4 to 5 top-level labels, set default label + downgrade justification, enable container labels (Teams/SPO) and auto-labelling | [Information Protection](../data-security/information-protection/README.md#best-practice-security-configuration) |

## Business applications and AI

| Product | Top Microsoft recommended controls | Guide section |
|---|---|---|
| **Power Platform** | Tenant-wide Data (DLP) policies blocking consumer/raw HTTP connectors, Tenant Isolation, Managed Environments sharing caps, environment security groups | [Power Platform](../business-apps/power-platform/README.md#best-practice-security-configuration) |
| **Dataverse & Dynamics 365** | Environment security groups, least-privilege custom roles + column-level security, IP firewall & cookie binding, Managed Identities/certs for app users | [Dataverse & Dynamics 365](../business-apps/dataverse-dynamics-365/README.md#best-practice-security-configuration) |
| **Microsoft Copilot Studio** | Block `Chat without Microsoft Entra ID authentication` connector in DLP, require Entra auth on internal agents, restrict grounding sources, Defender Agent 365 posture | [Copilot Studio](../business-apps/copilot-studio/README.md#best-practice-security-configuration) |
| **Microsoft 365 Copilot** | Remediate SharePoint oversharing first (Restricted SharePoint Search & site access reviews), enable Purview DSPM for AI + sensitivity labels, govern plugins via allow-list | [Microsoft 365 Copilot](../ai/microsoft-365-copilot/README.md#best-practice-security-configuration) |
| **Microsoft Foundry & Azure OpenAI** | Defender for AI Services, Content Safety Prompt Shields (direct + indirect), disable local API keys (`disableLocalAuth = true`), Private Endpoints | [Foundry & Azure OpenAI](../ai/azure-openai-ai-foundry/README.md#best-practice-security-configuration) |

## DevOps, servers and multi-cloud

| Product | Top Microsoft recommended controls | Guide section |
|---|---|---|
| **GitHub (Enterprise Cloud)** | Entra SAML SSO / EMU + 2FA, Secret scanning push protection, branch rulesets, OIDC federated cloud deploys (no static keys), pin Actions to SHAs, fine-grained PAT approval | [GitHub](../devops/github/README.md#best-practice-security-configuration) |
| **Azure DevOps** | Entra-backed orgs + Conditional Access validation, restrict PAT creation/lifetimes, migrate service connections to Workload Identity Federation (OIDC), branch & environment approvals | [Azure DevOps](../devops/azure-devops/README.md#best-practice-security-configuration) |
| **Windows Server** | Defender for Servers Plan 2 (MDE + AMA auto-provisioning, agentless scanning, FIM via AMA, JIT VM access / Bastion), Tamper Protection + EDR block mode + ASR | [Windows Server](../servers/windows-server/README.md#best-practice-security-configuration) |
| **Linux (Syslog, CEF & auditd)** | Defender for Servers Plan 2 (MDE on Linux + agentless scanning + FIM + JIT), SSH key-only auth (`PermitRootLogin no`), restrict Syslog forwarder port `514` & use TLS | [Linux](../servers/linux-syslog/README.md#best-practice-security-configuration) |
| **SQL Server (on-premises & IaaS)** | Azure Arc + Defender for SQL on machines, approved Vulnerability Assessment baseline, disable `sa` / prefer Windows or Entra auth, TLS 1.2+ | [SQL Server](../servers/sql-server/README.md#best-practice-security-configuration) |
| **Amazon Web Services** | Hardware MFA on root (zero root keys), Entra federation via IAM Identity Center, org-wide CloudTrail + GuardDuty, S3 Block Public Access, IMDSv2, Defender CSPM | [AWS](../multi-cloud/aws/README.md#best-practice-security-configuration) |
| **Google Cloud** | Entra workforce federation, Workload Identity Federation (disable JSON SA keys), org-level log sinks + SCC, uniform bucket access + public access prevention, Defender CSPM | [Google Cloud](../multi-cloud/google-cloud/README.md#best-practice-security-configuration) |

## Last verified

21 Nov 2026, against Microsoft Learn, GitHub Docs, AWS Docs and Google Cloud Docs.
