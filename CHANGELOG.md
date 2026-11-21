# Changelog

Notable updates to the Microsoft security logging guide, including automated nightly refreshes when Microsoft Learn pages, `Azure/Azure-Sentinel` Content Hub solutions or links change.

## 21 Nov 2026

- Completed and verified all 38 product guides across Identity, Endpoint, Email and collaboration, Cloud apps, Azure, Data security, Business applications, AI, DevOps, Servers and Multi-cloud.
- Split Dataverse and Dynamics 365 (`business-apps/dataverse-dynamics-365`) and Microsoft Copilot Studio (`business-apps/copilot-studio`) out of the Power Platform guide.
- Completed cross-cutting guides: [architecture](docs/architecture.md), [prioritisation](docs/prioritisation.md) (checked against the May 2025 ASD ACSC PDF with page references), [Defender XDR vs Sentinel](docs/defender-xdr-vs-sentinel.md), [data lake tiering](docs/data-lake-tiering.md), [cost estimation](docs/cost-estimation.md), [Sentinel health and audit](docs/sentinel-health.md) and [watchlists and enrichment](docs/watchlists.md).
- Added the [validation query pack](queries/validation/README.md) (11 group queries plus master `health-all-tables.kql`) and [cost estimation query pack](queries/cost/README.md).
- Added CI checks (Markdown lint, writing style, Mermaid render check and link check), GitHub Pages publishing via MkDocs Material, and the nightly drift-check and refresh workflow.
- Rebuilt navigation around an "I'm trying to..." outcome-and-product flow: added [Start here](docs/start-here.md), streamlined [README.md](README.md) and all 11 group index pages, and grouped the GitHub Pages site into five top-level tabs.
