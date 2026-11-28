# Defender best-practice security configurations

> Status: verified. Last verified: 28 Nov 2026.

Logging tells you when something goes wrong; hardening stops the bulk of it before an alert even fires. This handbook pulls together the recommended production security configuration for every Microsoft Defender product, structured as **"I'm trying to harden..."** so you can jump straight to the product you're configuring.

## Jump by product ("I'm trying to harden...")

| I'm trying to harden... | Jump to section | Logging guide |
|---|---|---|
| **Unified Defender XDR platform** (attack disruption, RBAC, Sentinel portal) | [Microsoft Defender XDR](#microsoft-defender-xdr-unified-platform) | [Defender XDR vs Sentinel](defender-xdr-vs-sentinel.md) |
| **Workstations & servers (EDR / AV / ASR)** | [Microsoft Defender for Endpoint](#microsoft-defender-for-endpoint) | [Defender for Endpoint](../endpoint/defender-for-endpoint/README.md) |
| **Exchange Online, Teams & SharePoint email threats** | [Microsoft Defender for Office 365](#microsoft-defender-for-office-365) | [Defender for Office 365](../email-collab/defender-for-office-365/README.md) |
| **On-premises Active Directory, AD FS & AD CS** | [Microsoft Defender for Identity](#microsoft-defender-for-identity) | [Defender for Identity](../identity/defender-for-identity/README.md) |
| **SaaS apps, OAuth apps & shadow IT** | [Microsoft Defender for Cloud Apps](#microsoft-defender-for-cloud-apps) | [Defender for Cloud Apps](../cloud-apps/defender-for-cloud-apps/README.md) |
| **Cloud posture, attack paths & governance** | [Defender CSPM](#defender-cspm-cloud-security-posture-management) | [Defender for Cloud](../azure/defender-for-cloud/README.md) |
| **Azure VMs & hybrid Arc servers** | [Defender for Servers (Plan 1 vs Plan 2)](#defender-for-servers) | [Windows Server](../servers/windows-server/README.md), [Linux](../servers/linux-syslog/README.md) |
| **Azure SQL PaaS & SQL Server on machines** | [Defender for SQL](#defender-for-sql) | [Azure SQL](../azure/azure-sql/README.md), [SQL Server](../servers/sql-server/README.md) |
| **Azure Storage accounts** | [Defender for Storage](#defender-for-storage) | [Azure Storage](../azure/storage/README.md) |
| **AKS & multi-cloud Kubernetes clusters** | [Defender for Containers](#defender-for-containers) | [AKS](../azure/aks/README.md) |
| **Key Vault, App Service, APIs, Databases, AI & ARM** | [Other Defender for Cloud workload plans](#other-defender-for-cloud-workload-plans) | [Key Vault](../azure/key-vault/README.md), [App Service](../azure/app-service-functions/README.md), [Foundry & OpenAI](../ai/azure-openai-ai-foundry/README.md) |

## Microsoft Defender XDR (unified platform)

| Setting | Recommended configuration | Why it matters |
|---|---|---|
| **Automatic attack disruption** | Keep **enabled** across Endpoint, Identity, Cloud Apps and Office 365, and configure exclusions only for break-glass or critical service accounts ([Microsoft Learn](https://learn.microsoft.com/en-us/defender-xdr/automatic-attack-disruption)). | Automatically contains hands-on-keyboard ransomware, BEC and adversary-in-the-middle attacks at machine speed (isolates devices, disables compromised AD/Entra accounts, suspends OAuth apps). |
| **Unified RBAC** | Migrate workload-specific roles into Defender XDR Unified RBAC with least privilege and scoped device/asset groups ([Microsoft Learn](https://learn.microsoft.com/en-us/defender-xdr/manage-rbac)). Sentinel workspaces onboarded to the Defender portal can be managed here too, but role assignments to service principals aren't supported. | One permission model across Defender XDR and Sentinel in the Defender portal without granting broad Entra Global Admin or Security Admin roles. |
| **Alert tuning & incident deduplication** | Onboard Sentinel to the Defender portal, turn off legacy standalone alert connectors and Microsoft incident creation rules, and use Defender portal **Alert tuning** rather than suppressing whole connectors. | Prevents duplicate incidents while keeping attack-story correlation intact. See [Defender XDR vs Sentinel](defender-xdr-vs-sentinel.md). |

## Microsoft Defender for Endpoint

Roll out restrictive controls in **Audit** mode for 14 to 30 days on a pilot ring, inspect blocks in `DeviceEvents`, add targeted path/certificate exclusions (never broad folder exclusions like `C:\`), then move to **Block** mode.

| Control | Recommended configuration | Official docs |
|---|---|---|
| **Tamper Protection** | **On** across all Windows and macOS devices (managed via Intune Endpoint Security; do not leave editable by local admins). | [Tamper protection overview](https://learn.microsoft.com/en-us/defender-endpoint/prevent-changes-to-security-settings-with-tamper-protection) |
| **EDR in block mode** | **On** for every device, especially where a third-party AV runs in active mode and Defender Antivirus is passive. | [EDR in block mode](https://learn.microsoft.com/en-us/defender-endpoint/edr-in-block-mode) |
| **Attack Surface Reduction (ASR) rules** | Enable all standard ASR rules via Intune: start in **Audit**, then move high-confidence rules (LSASS credential stealing, Office child processes, macro Win32 API calls, PsExec/WMI process creation, obfuscated scripts, vulnerable signed drivers) to **Block**. | [ASR rules overview](https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction) |
| **Network Protection** | Set to **Block** mode on Windows clients and servers (enforces SmartScreen and Defender TI URL/IP blocks across all browsers and processes, not just Edge). | [Turn on network protection](https://learn.microsoft.com/en-us/defender-endpoint/enable-network-protection) |
| **Cloud-delivered protection & Block at First Sight** | Cloud protection **On**, Cloud Block Level **High** (or **High+** on high-risk rings), Extended Cloud Check **50 seconds**, automatic sample submission **Send all samples** (or safe samples where required by policy). | [Configure block at first sight](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus) |
| **PUA protection** | Set to **Block** for both endpoint AV and Edge SmartScreen. | [Block potentially unwanted applications](https://learn.microsoft.com/en-us/defender-endpoint/detect-block-potentially-unwanted-apps-microsoft-defender-antivirus) |
| **Controlled Folder Access** | Pilot in **Audit** mode first, then enable **Block** on high-value workstations to stop untrusted processes encrypting user folders. | [Controlled folder access](https://learn.microsoft.com/en-us/defender-endpoint/controlled-folders) |
| **Automated Investigation and Remediation (AIR)** | Set device groups to **Full - remediate threats automatically** for standard workstations and semi-automated (or full after testing) for servers. | [Configure AIR](https://learn.microsoft.com/en-us/defender-endpoint/configure-automated-investigations-remediation) |
| **Live Response** | Disable **Live Response unsigned script execution** unless your SOC explicitly requires it, and restrict Live Response permissions via Unified RBAC. | [Unified RBAC](https://learn.microsoft.com/en-us/defender-xdr/manage-rbac) |

## Microsoft Defender for Office 365

| Control | Recommended configuration | Official docs |
|---|---|---|
| **Preset security policies** | Apply Microsoft's **Standard** preset to all users and the **Strict** preset to executives, finance, IT admins and other high-risk accounts, rather than maintaining fragile custom anti-spam/anti-phish rules. | [Preset security policies](https://learn.microsoft.com/en-us/defender-office-365/preset-security-policies) |
| **Safe Links** | Enable across **Email**, **Microsoft Teams** and **Office 365 apps**. Turn on **Track user clicks** and turn **off** "Let users click through to the original URL". | [Safe Links overview](https://learn.microsoft.com/en-us/defender-office-365/safe-links-about) |
| **Safe Attachments** | Use **Dynamic Delivery** (delivers message body while scanning attachments) and enable **Safe Attachments for SharePoint, OneDrive and Microsoft Teams**. | [Safe Attachments](https://learn.microsoft.com/en-us/defender-office-365/safe-attachments-about) |
| **Anti-phishing & email auth** | Enable mailbox intelligence, user and domain impersonation protection, first-contact safety tips, and enforce **SPF**, **DKIM** and **DMARC** (`p=reject` after monitoring) on every accepted domain. | [Anti-phishing policies](https://learn.microsoft.com/en-us/defender-office-365/anti-phishing-policies-about) |
| **Zero-hour Auto Purge (ZAP)** | Keep **enabled** for malware, high-confidence phish, spam and Microsoft Teams messages so post-delivery verdicts automatically pull malicious items out of mailboxes and chats. | [Zero-hour auto purge](https://learn.microsoft.com/en-us/defender-office-365/zero-hour-auto-purge) |

## Microsoft Defender for Identity

| Control | Recommended configuration | Official docs |
|---|---|---|
| **100% DC, AD FS and AD CS coverage** | Deploy the Defender for Identity sensor on **every** Domain Controller (including read-only DCs), every AD FS server and every AD CS server. Missing one DC creates a blind spot for Kerberos and lateral movement. | [Defender for Identity guide](../identity/defender-for-identity/README.md) |
| **Required Windows audit policies** | Enable Advanced Audit Policy subcategories (especially Directory Service Changes `4662` with SACLs, NTLM `4776`, Security Group Management, AD FS and AD CS auditing) so the sensor sees password changes, DCSync and certificate abuse. | [Configure Windows event auditing](https://learn.microsoft.com/en-us/defender-for-identity/configure-windows-event-collection) |
| **Entity tags (Sensitive & Honeytoken)** | Tag high-value non-default admin/VIP accounts and Exchange/PKI groups as **Sensitive**, and create at least two believable **Honeytoken** accounts with no real usage so any touch fires an immediate high-confidence alert. | [Entity tags](https://learn.microsoft.com/en-us/defender-for-identity/entity-tags) |
| **Action accounts (gMSA)** | Configure a dedicated **group Managed Service Account (gMSA)** with minimal delegated permissions so automatic attack disruption and SOC response actions can disable compromised on-premises AD accounts. | [Automatic attack disruption](https://learn.microsoft.com/en-us/defender-xdr/automatic-attack-disruption) |

## Microsoft Defender for Cloud Apps

| Control | Recommended configuration | Official docs |
|---|---|---|
| **Connect all major SaaS & cloud platforms** | Connect Microsoft 365, Azure, AWS, Google Cloud and key third-party IdP/SaaS apps (Okta, Salesforce, ServiceNow, Box, Google Workspace) so `CloudAppEvents` and anomaly policies have full coverage. | [MDCA best practices](https://learn.microsoft.com/en-us/defender-cloud-apps/best-practices) |
| **Native MDE Cloud Discovery** | Enable the **Microsoft Defender for Endpoint integration** inside MDCA settings so managed Windows/macOS endpoints feed shadow IT discovery automatically without deploying standalone log collectors. | [MDCA best practices](https://learn.microsoft.com/en-us/defender-cloud-apps/best-practices) |
| **App Governance** | Turn on **App Governance** and enable built-in OAuth app threat policies (overprivileged apps, dormant high-privilege apps, unusual Graph/mail access) to catch illicit consent grants. | [App governance](https://learn.microsoft.com/en-us/defender-cloud-apps/app-governance-manage-app-governance) |
| **Conditional Access App Control** | Route unmanaged or risky sessions for Microsoft 365 and sensitive SaaS apps through Conditional Access App Control session policies to block file downloads, cut/copy/paste or unsanctioned uploads in real time. | [Conditional Access app control](https://learn.microsoft.com/en-us/defender-cloud-apps/proxy-intro-aad) |
| **Purview Information Protection integration** | Enable Microsoft Purview Information Protection integration in MDCA so file policies can inspect and auto-apply sensitivity labels on cloud-stored files. | [MDCA best practices](https://learn.microsoft.com/en-us/defender-cloud-apps/best-practices) |

## Defender CSPM (Cloud Security Posture Management)

Enable **Defender CSPM** at subscription or management-group scale (via Azure Policy) across Azure, AWS and Google Cloud rather than relying on Foundational CSPM alone ([What is CSPM](https://learn.microsoft.com/en-us/azure/defender-for-cloud/concept-cloud-security-posture-management)).

| Capability | Recommended configuration | Official docs |
|---|---|---|
| **Agentless scanning for machines** | Enable **Agentless scanning** (snapshot-based vulnerability and secret scanning) so VMs without agents or with broken agents still get continuous CVE, software inventory and cleartext-secret coverage with zero runtime impact. | [Agentless machine scanning](https://learn.microsoft.com/en-us/azure/defender-for-cloud/concept-agentless-data-collection) |
| **Attack Path Analysis & Cloud Security Explorer** | Prioritise remediation by **critical attack paths** (for example internet-exposed VM with a high-privilege managed identity) rather than chasing raw Secure Score percentages. | [Security explorer and attack paths](https://learn.microsoft.com/en-us/azure/defender-for-cloud/concept-attack-path) |
| **Data-aware security posture** | Enable **Sensitive data discovery** inside Defender CSPM so attack paths highlight internet-exposed Storage accounts and SQL databases holding regulated or sensitive data. | [What is CSPM](https://learn.microsoft.com/en-us/azure/defender-for-cloud/concept-cloud-security-posture-management) |
| **Governance rules** | Configure **Governance rules** at management group or subscription scope to assign owners, enforce remediation SLAs (for example 7 days High, 30 days Medium) and email weekly overdue digests. | [Governance rules](https://learn.microsoft.com/en-us/azure/defender-for-cloud/governance-rules) |
| **Regulatory standards & DevOps Security** | Attach your required compliance frameworks (Microsoft Cloud Security Benchmark, Essential Eight, ISO 27001, NIST SP 800-53) and connect **GitHub** and **Azure DevOps** so IaC and secret findings map back to live cloud resources. | [What is CSPM](https://learn.microsoft.com/en-us/azure/defender-for-cloud/concept-cloud-security-posture-management) |

## Defender for Servers

Choose **Plan 2** for production Azure VMs and Azure Arc-enabled on-premises/multi-cloud servers; use **Plan 1** only where you want MDE EDR coverage without FIM, JIT, agentless scanning or the Sentinel data grant ([Plan Defender for Servers](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-servers-introduction)).

| Control | Recommended configuration | Official docs |
|---|---|---|
| **Auto-provisioning (MDE + AMA)** | Enable automatic provisioning of **Microsoft Defender for Endpoint** and the **Azure Monitor Agent** across Azure subscriptions and Azure Arc servers. | [Plan Defender for Servers](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-servers-introduction) |
| **Agentless vulnerability & secret scanning (P2)** | Keep enabled in Plan 2 alongside Defender Vulnerability Management for full OS and software inventory. | [Agentless machine scanning](https://learn.microsoft.com/en-us/azure/defender-for-cloud/concept-agentless-data-collection) |
| **File Integrity Monitoring (P2)** | Enable **Defender for Cloud FIM (via AMA)** on critical Windows and Linux servers (`MDCFileIntegrityMonitoringEvents`, covered by the 500 MB/node/day grant). | [File integrity monitoring](https://learn.microsoft.com/en-us/azure/defender-for-cloud/file-integrity-monitoring-overview) |
| **Just-in-Time (JIT) VM access (P2)** | Enable JIT on every VM that still needs RDP (`3389`) or SSH (`22`) management ports, or eliminate public IPs completely with Azure Bastion / Private Access. | [Just-in-time VM access](https://learn.microsoft.com/en-us/azure/defender-for-cloud/just-in-time-access-overview) |
| **500 MB/node/day Sentinel grant (P2)** | Link your Sentinel workspace to benefit from the pooled 500 MB/server/day free ingestion across eligible security tables (`SecurityEvent`, `MDCFileIntegrityMonitoringEvents`, etc.). | [Windows Server guide](../servers/windows-server/README.md) |

## Defender for SQL

Covers both **Azure SQL Database / Managed Instance / Synapse** and **SQL Server on Azure VMs, on-premises or multi-cloud via Azure Arc** ([Defender for Azure SQL](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-sql-introduction), [Defender for SQL on machines](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-sql-usage)).

| Control | Recommended configuration | Official docs |
|---|---|---|
| **Enable at subscription scope** | Turn on **Defender for Azure SQL Databases** and **Defender for SQL Servers on Machines** at subscription scope (via Azure Policy) so newly provisioned databases and Arc-connected SQL instances are protected automatically. | [Defender for Azure SQL](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-sql-introduction) |
| **Vulnerability Assessment (Express configuration)** | Enable **Express configuration** (stores baselines in Azure without needing a separate storage account), run the initial scan, approve a reviewed baseline, and review weekly recurring scan findings. | [SQL Vulnerability Assessment](https://learn.microsoft.com/en-us/azure/defender-for-cloud/sql-azure-vulnerability-assessment-overview) |
| **Advanced Threat Protection** | Keep all threat detection types active (SQL injection, anomalous client login/location, brute force, data exfiltration) and route alerts into Defender XDR and Sentinel (`SecurityAlert`, free). | [Defender for Azure SQL](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-sql-introduction) |
| **Entra-only auth & private networking** | Disable SQL local authentication where applications support Microsoft Entra ID, turn off **Allow Azure services and resources to access this server**, and enforce Private Endpoints + TLS 1.2+. | [Azure SQL guide](../azure/azure-sql/README.md) |
| **Auditing to Sentinel** | Enable server-level auditing to Log Analytics on Azure SQL, and SQL Server Audit `TO SECURITY_LOG` (Event ID `33205`) via AMA on SQL Server machines. | [SQL Server guide](../servers/sql-server/README.md) |

## Defender for Storage

| Control | Recommended configuration | Official docs |
|---|---|---|
| **Enable the current per-storage-account plan** | Use the modern **Microsoft Defender for Storage** plan (migrate off the legacy per-transaction Classic plan) at subscription scope. | [What is Defender for Storage](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-storage-introduction) |
| **On-upload Malware Scanning** | Enable **Malware Scanning** on storage accounts accepting external, user or partner uploads (set a monthly GB cap per account to control scan cost) and attach an Event Grid + Logic App/Function to automatically quarantine or delete malicious blobs based on the `Malware Scanning scan result` blob index tag. | [Defender for Storage Malware Scanning](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-storage-malware-scan) |
| **Sensitive Data Threat Detection** | Enable **Sensitive Data Threat Detection** so Defender prioritises alerts involving containers holding PII, credentials or financial data. | [What is Defender for Storage](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-storage-introduction) |
| **Baseline storage hardening** | Disable **Allow Blob anonymous access**, disable **Shared Key access** (enforce Entra RBAC + SAS expiry limits), enforce HTTPS-only and TLS 1.2+, and restrict public network access via Private Endpoints or VNet firewall rules. | [Azure Storage guide](../azure/storage/README.md) |

## Defender for Containers

| Control | Recommended configuration | Official docs |
|---|---|---|
| **Agentless discovery + Defender sensor** | Enable both **Agentless discovery for Kubernetes** (API-based posture and vulnerability visibility) and the **Defender sensor DaemonSet** (eBPF runtime threat detection and binary drift detection) across AKS, EKS and GKE. | [Defender for Containers](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-containers-introduction) |
| **Registry vulnerability assessment** | Enable continuous vulnerability scanning on Azure Container Registry (and AWS ECR / Google Artifact Registry), blocking or alerting on critical CVEs before deployment. | [Defender for Containers](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-containers-introduction) |
| **Kubernetes admission control** | Enable the **Azure Policy add-on for AKS** and enforce the built-in **Kubernetes cluster pod security restricted standards** (block privileged containers, hostPath mounts and root escalation). | [AKS guide](../azure/aks/README.md) |
| **Control plane hardening** | Use Entra ID RBAC (disable local Kubernetes accounts), restrict API server authorised IP ranges or use private AKS clusters, and collect `AKSAuditAdmin` in Sentinel Analytics. | [AKS guide](../azure/aks/README.md) |

## Other Defender for Cloud workload plans

| Plan | Best-practice configuration | Official docs |
|---|---|---|
| **Defender for Key Vault** | Enable subscription-wide, enforce **soft-delete** and **purge protection** on every production vault, migrate from legacy access policies to **Azure RBAC**, and restrict network access with Private Endpoints. | [Defender for Key Vault](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-key-vault-introduction) |
| **Defender for App Service** | Enable on production subscriptions, disable **FTP** and **SCM/Kudu basic publishing credentials** (use Entra ID / OIDC deployments), enforce HTTPS-only, TLS 1.2+ and managed identities instead of connection strings. | [Defender for App Service](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-app-service-introduction) |
| **Defender for Open-Source Relational Databases & Cosmos DB** | Enable across PostgreSQL, MySQL, MariaDB and Cosmos DB accounts for anomalous access, brute force and injection alerts; enforce Entra auth and Private Endpoints where supported. | [Defender for Open-Source Databases](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-databases-introduction) |
| **Defender for APIs** | Onboard Azure API Management APIs to discover shadow/unauthenticated APIs, detect OWASP API Top 10 risks and alert on anomalous API abuse. | [Defender for APIs](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-apis-introduction) |
| **Defender for Resource Manager** | Enable subscription-wide to detect suspicious Azure control-plane activity (anonymous/Tor ARM operations, suspicious RBAC escalation, deployment of known-bad templates) at minimal cost. | [Defender for Resource Manager](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-resource-manager-introduction) |
| **Defender for AI Services** | Enable on subscriptions hosting Azure OpenAI and Microsoft Foundry to detect prompt injection/jailbreaks, sensitive data exposure and credential abuse, paired with Azure AI Content Safety Prompt Shields. | [AI threat protection](https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-threat-protection) |

## Official links

- [Automatic attack disruption in Microsoft Defender](https://learn.microsoft.com/en-us/defender-xdr/automatic-attack-disruption)
- [Microsoft Defender unified RBAC](https://learn.microsoft.com/en-us/defender-xdr/manage-rbac)
- [Tamper protection overview](https://learn.microsoft.com/en-us/defender-endpoint/prevent-changes-to-security-settings-with-tamper-protection)
- [ASR rules overview](https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction)
- [EDR in block mode](https://learn.microsoft.com/en-us/defender-endpoint/edr-in-block-mode)
- [Preset security policies in Defender for Office 365](https://learn.microsoft.com/en-us/defender-office-365/preset-security-policies)
- [Configure Windows event auditing for Defender for Identity](https://learn.microsoft.com/en-us/defender-for-identity/configure-windows-event-collection)
- [Best practices for Defender for Cloud Apps](https://learn.microsoft.com/en-us/defender-cloud-apps/best-practices)
- [What is Cloud Security Posture Management (CSPM)?](https://learn.microsoft.com/en-us/azure/defender-for-cloud/concept-cloud-security-posture-management)
- [Plan a Defender for Servers deployment](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-servers-introduction)
- [Defender for Azure SQL Databases](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-sql-introduction)
- [What is Microsoft Defender for Storage?](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-storage-introduction)
- [Introduction to Defender for Containers](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-containers-introduction)
- [AI threat protection in Defender for Cloud](https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-threat-protection)

## Last verified

28 Nov 2026, against Microsoft Learn.
