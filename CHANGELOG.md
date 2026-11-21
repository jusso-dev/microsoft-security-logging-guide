# Changelog

All notable changes to the Microsoft security logging guide are documented in this file, including automated nightly refreshes when Microsoft Learn pages, `Azure/Azure-Sentinel` Content Hub solutions or links change.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

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
