# Changelog

All notable changes to the Microsoft security logging guide are documented in this file, including automated nightly refreshes when Microsoft Learn pages, `Azure/Azure-Sentinel` Content Hub solutions or links change.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Changed

- **28 Nov 2026 nightly refresh.** Five guides flagged by drift detection were re-checked against upstream changes:
  - [Defender best-practice configurations](docs/defender-best-practices.md): the Unified RBAC row now notes that Sentinel workspaces onboarded to the Defender portal can be managed in unified RBAC, and that role assignments to service principals aren't supported. Source: the [unified RBAC page](https://learn.microsoft.com/en-us/defender-xdr/manage-rbac) (updated 26 Nov 2026).
  - [Dataverse and Dynamics 365](business-apps/dataverse-dynamics-365/README.md): the "Audit logging disabled" rule now notes that organisation-level audit-disable events are detected from solution 3.2.6 (`Solutions/Microsoft Business Applications`, commit `890eeeb`, and merge `6b08944`). The rule's table and MITRE mapping are unchanged. The workbook variable rename is not in the guide.
  - [Power Platform](business-apps/power-platform/README.md): no content change. The same 3.2.6 solution update does not affect its tables or rules. The minimum solution version (3.2.5) is unchanged.
  - [Microsoft Entra ID](identity/entra-id/README.md): no content change. The Entra ID solution commits (`a5a2a58` adds package 3.3.22 with evidence updates, and `e3ef506` lowercases guest UPNs before the `#ext#` split in `UnusualGuestActivity`) do not change the tables, connectors or rule names the guide documents.
  - [AD FS](identity/adfs/README.md): no content change. The Entra ID solution commits above do not touch the AD FS content.
  - "Last verified" dates are set to 28 Nov 2026 for these five guides. The check covered the upstream pages and commits in the drift report, not every link in each guide.
- **27 Nov 2026 nightly refresh.** Five guides flagged by drift detection were re-checked:
  - [Azure networking](azure/network-nsg-flow-firewall/README.md): the NSG flow log creation date (30 June 2025) is replaced with the wording Microsoft Learn now uses, that new NSG flow logs can no longer be created. The 30 September 2027 retirement date is confirmed against the NSG flow logs overview (updated 26 Nov 2026). The VNet flow logs and Traffic Analytics pages were re-read, and no other changes were needed.
  - [Exchange Online](email-collab/exchange-online/README.md), [Microsoft Purview unified audit log](email-collab/purview-unified-audit/README.md), [SharePoint Online and OneDrive](email-collab/sharepoint-onedrive/README.md) and [Microsoft Teams](email-collab/teams/README.md): the audit log activities page (updated 24 Nov 2026) was re-read. Its Teams operation names, admin audit log behaviour and SharePoint file throttling notes match the guides. "Last verified" dates are unchanged because the full guide text was not re-checked in this run.
- **26 Nov 2026 nightly refresh.** Five guides re-checked against upstream Microsoft Learn changes:
  - [Azure App Service and Azure Functions](azure/app-service-functions/README.md): `AppServiceFileAuditLogs` and `AppServiceAntivirusScanAuditLogs` now note the Premium tier requirement, and the Linux and Windows gaps for `AppServiceFileAuditLogs` and `AppServicePlatformLogs` are documented. Disabling FTP or SCM basic auth now needs owner-level access to the app. Gotchas cover SCM basic auth for FTP and the app restart when a diagnostic setting is added.
  - [Azure Storage](azure/storage/README.md): added Azure Files diagnostic setting guidance. Logs are set on the `file` resource, aren't sent to Log Analytics by default, and cover both `Microsoft.Storage` and `Microsoft.FileShares` shares.
  - [Data lake tiering](docs/data-lake-tiering.md), [Defender XDR vs Sentinel](docs/defender-xdr-vs-sentinel.md) and [Prioritisation](docs/prioritisation.md): re-checked the ISOC retention page (updated 23 Nov 2026). The 90-day included retention covers Microsoft Defender and Microsoft Entra tables, not Azure Activity or Office 365 Activity, so the Defender XDR vs Sentinel text is corrected. No table names or tiers changed, so `queries/validation` is unchanged.
- **25 Nov 2026 nightly refresh.** Five guides re-checked against upstream changes:
  - [Microsoft Purview Information Protection](data-security/information-protection/README.md): added the missing `FileSensitivityLabelRemoved`, `SiteSensitivityLabelApplied`, `SiteSensitivityLabelRemoved` and `FileSensitivityLabelRemoveFailed` operations from the Purview audit log activities page. The mass removal rule now covers Office for the web and SharePoint removals.
  - [Azure networking](azure/network-nsg-flow-firewall/README.md): noted the Front Door WAF category for Standard/Premium (`FrontDoorWebApplicationFirewallLog`) and the classic variant (`FrontdoorWebApplicationFirewallLog`), per the updated WAF monitoring page.
  - [Microsoft Defender for Cloud Apps](cloud-apps/defender-for-cloud-apps/README.md): GitHub connection guidance now states that an Enterprise-level connection disables existing Organization-level connectors, and lists the licence and owner prerequisites, per the updated GitHub protection page.
  - [Dataverse and Dynamics 365](business-apps/dataverse-dynamics-365/README.md) and [Power Platform](business-apps/power-platform/README.md): no content change. The upstream `Azure/Azure-Sentinel` commit `16de03e` only removed a 3.2.6 release-note line. The minimum solution version (3.2.5) is unchanged.

## 1.0.0 - 2026-11-21

### Added

- **38 verified product guides** across 11 product groups following a common [template](TEMPLATE.md) with high-value log sources, Sentinel table mappings, Analytics vs Data lake tiering, step-by-step setup, validation KQL, out-of-box analytic rules, custom detections, Mermaid architecture diagrams, recommended security configurations and official Microsoft Learn links:
  - **Identity:** Microsoft Entra ID, Microsoft Entra ID Protection, Microsoft Defender for Identity, Active Directory Domain Services (on-premises), Active Directory Federation Services (AD FS) and Microsoft Entra Global Secure Access.
  - **Endpoint:** Microsoft Defender for Endpoint, Windows security event logs (clients) and Microsoft Intune.
  - **Email and collaboration:** Exchange Online, Microsoft Defender for Office 365, SharePoint Online and OneDrive, Microsoft Teams and Microsoft Purview unified audit log.
  - **Cloud apps:** Microsoft Defender for Cloud Apps.
  - **Azure:** Azure Activity, Microsoft Defender for Cloud, Azure Key Vault, Azure Storage, Azure SQL Database and Managed Instance, Azure Kubernetes Service (AKS), Azure networking (VNet flow logs, Azure Firewall, WAF, DNS) and Azure App Service and Azure Functions.
  - **Data security:** Microsoft Purview Data Loss Prevention, Microsoft Purview Insider Risk Management and Microsoft Purview Information Protection.
  - **Business applications:** Power Platform, Microsoft Dataverse and Dynamics 365, and Microsoft Copilot Studio.
  - **AI:** Microsoft 365 Copilot, and Microsoft Foundry (formerly Azure AI Foundry) and Azure OpenAI.
  - **DevOps:** GitHub (Enterprise Cloud) and Azure DevOps.
  - **Servers:** Windows Server, Linux (Syslog, CEF and auditd) and SQL Server (on-premises and IaaS).
  - **Multi-cloud (optional):** Amazon Web Services and Google Cloud.
- **Cross-cutting architecture and operations guides** in `docs/`:
  - [Start here](docs/start-here.md) outcome-driven decision guide and 30-day onboarding sequence.
  - [Architecture overview](docs/architecture.md), [Defender XDR vs Sentinel](docs/defender-xdr-vs-sentinel.md) and [Data lake tiering](docs/data-lake-tiering.md).
  - [Prioritisation](docs/prioritisation.md) mapped against the May 2025 ASD ACSC Priority Logs PDF with exact page references.
  - [Cost estimation](docs/cost-estimation.md), [Sentinel health and audit](docs/sentinel-health.md) and [Watchlists and enrichment](docs/watchlists.md).
  - [Defender best-practice security configurations](docs/defender-best-practices.md) and the all-38-products [Microsoft recommended security configurations](docs/security-configurations.md) reference.
- **KQL query packs** in `queries/`:
  - [Validation query pack](queries/validation/README.md) covering all 11 product groups plus `health-all-tables.kql`.
  - [Cost estimation query pack](queries/cost/README.md) with 7 queries for per-table, per-solution and per-DCR volume, daily anomalies, top noisy events and hosts, commitment tier sizing and Defender XDR streaming cost preview.
- **Outcome-driven navigation and GitHub Pages site:** MkDocs Material site (`mkdocs.yml`, `scripts/build_pages.py`, `.github/workflows/pages.yml`) grouped into five top-level tabs, plus "I'm trying to..." navigation across [README.md](README.md) and all 11 product group index pages.
- **CI quality gates and nightly drift refresh:** GitHub Actions workflows for Markdown lint, writing-style checks (`scripts/check-style.mjs`), Mermaid diagram rendering (`scripts/check-mermaid.mjs`), external link verification via `lychee` (`.github/workflows/ci.yml`), and automated nightly upstream drift detection and refresh (`scripts/check-drift.mjs`, `.github/workflows/nightly-refresh.yml`).
- **Microsoft security logging stack cross-links** in [README.md](README.md) connecting `microsoft-security-logging-guide`, `soc-ready-logging`, `Bower`, `blueboard` and `crosswire`.
