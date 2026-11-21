# Microsoft Sentinel solution package

This folder packages the KQL detections, hunting queries, validation queries and cost estimation queries from the Microsoft security logging guide into a deployable **Microsoft Sentinel Content Hub V3** solution (`MicrosoftSecurityLoggingGuide`).

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fjusso-dev%2Fmicrosoft-security-logging-guide%2Fmain%2Fsolution%2FSolutions%2FMicrosoftSecurityLoggingGuide%2FPackage%2FmainTemplate.json)

## What gets deployed

Clicking **Deploy to Azure** installs the V3 solution package (`contentPackages` and `contentTemplates`) into an existing Microsoft Sentinel-enabled Log Analytics workspace. Every analytic rule installs as a **rule template** (disabled by default) so deployment succeeds even if you have not connected all 38 log sources yet, and nothing fires until you review, tune and enable the rules you need.

| Content type | Count | Source in this repository |
|---|---|---|
| Analytic rule templates (YAML) | 122 | 119 Sentinel-compatible custom detections across all 38 product guides, plus 3 operational health and audit rules from [docs/sentinel-health.md](../docs/sentinel-health.md) |
| Hunting queries (YAML) | 22 | 17 Sentinel-compatible hunting queries from the product guides, plus 5 operational health, query-audit, watchlist and cost anomaly hunts |
| Workbooks (JSON) | 2 | **Ingestion Health and Table Freshness** (from [queries/validation/](../queries/validation/README.md) and [docs/sentinel-health.md](../docs/sentinel-health.md)) and **Cost Estimation and Volume Monitoring** (from [queries/cost/](../queries/cost/README.md) and [docs/cost-estimation.md](../docs/cost-estimation.md)) |
| Defender XDR custom detections | 15 | Packaged separately in [defender-xdr/](../defender-xdr/README.md) so you can run detections on `Device*`, `Email*`, `Identity*`, `CloudAppEvents`, `AgentsInfo`, `DataSecurityEvents` and `BehaviorInfo` without paying Sentinel ingestion |

Playbooks and Logic Apps are not packaged here because the guide recommends reusing official Microsoft Content Hub playbooks (such as `Block-AADUser`, `Revoke-AADSignInSessions` and `Isolate-MDEMachine`) documented in each product guide.

## Solution layout

The layout follows the official [Azure/Azure-Sentinel Solutions](https://github.com/Azure/Azure-Sentinel/tree/master/Solutions) Content Hub V3 convention:

```text
solution/
  README.md
  Solutions/
    MicrosoftSecurityLoggingGuide/
      SolutionMetadata.json
      ReleaseNotes.md
      Data/
        Solution_MicrosoftSecurityLoggingGuide.json
      Analytic Rules/          # 122 Scheduled analytic rule YAML templates
      Hunting Queries/         # 22 Hunting query YAML templates
      Workbooks/               # 2 Sentinel workbook JSON templates
      Package/
        mainTemplate.json      # Content Hub V3 ARM template (147 resources)
        createUiDefinition.json
```

## Deployment options

### Option 1: One-click Deploy to Azure

1. Select the **Deploy to Azure** button at the top of this page.
2. Choose the **Subscription** and **Resource group** containing your Microsoft Sentinel workspace.
3. Enter your existing Log Analytics workspace name in **Workspace**, confirm **Workspace-location** matches the workspace region, and toggle which content groups (`DeployAnalyticsRule`, `DeployHuntingQuery`, `DeployWorkbook`) to install.
4. Select **Review + create**, then **Create**.

### Option 2: Azure CLI

Deploy into an existing Sentinel workspace in resource group `rg-sentinel`:

```bash
az deployment group create \
  --resource-group rg-sentinel \
  --template-file solution/Solutions/MicrosoftSecurityLoggingGuide/Package/mainTemplate.json \
  --parameters workspace="law-sentinel-prod" workspace-location="australiaeast"
```

To deploy only the workbooks and hunting queries without analytic rule templates:

```bash
az deployment group create \
  --resource-group rg-sentinel \
  --template-file solution/Solutions/MicrosoftSecurityLoggingGuide/Package/mainTemplate.json \
  --parameters workspace="law-sentinel-prod" workspace-location="australiaeast" \
               DeployAnalyticsRule=false
```

### Option 3: PowerShell

```powershell
New-AzResourceGroupDeployment `
  -ResourceGroupName "rg-sentinel" `
  -TemplateFile "solution/Solutions/MicrosoftSecurityLoggingGuide/Package/mainTemplate.json" `
  -workspace "law-sentinel-prod" `
  -workspace-location "australiaeast"
```

## After deployment

1. Open the Microsoft Defender portal and navigate to **Microsoft Sentinel > Content management > Content hub** (or **Configuration > Analytics > Rule templates**).
2. Enable only the analytic rules matching connectors you actively ingest. Read any `// ASSUMPTION:` comments in the rule KQL and replace placeholder lists (such as `approved_admins`, `gitops_accounts` or watchlists) with your environment's values before enabling.
3. For detections targeting Microsoft Defender XDR tables (`Device*`, `Email*`, `UrlClickEvents`, `Identity*`, `CloudAppEvents`, `AgentsInfo`, `DataSecurityEvents`, `BehaviorInfo`), prefer the Defender XDR custom detections in [defender-xdr/](../defender-xdr/README.md) unless you already stream those tables to Sentinel. Never enable both the Sentinel rule and the Defender XDR custom detection for the same logic, or you will raise duplicate alerts (see [Defender XDR vs Sentinel](../docs/defender-xdr-vs-sentinel.md)).
4. Open **Workbooks > Templates** to save and run **Ingestion Health and Table Freshness** and **Cost Estimation and Volume Monitoring**.

## Rebuilding and validating

All files under `solution/Solutions/MicrosoftSecurityLoggingGuide/` and `defender-xdr/rules/` are generated reproducibly from the guide Markdown and query packs so the documentation remains the single source of truth:

```bash
python3 scripts/build_solution.py
python3 scripts/validate_sentinel.py
```

See [ReleaseNotes.md](Solutions/MicrosoftSecurityLoggingGuide/ReleaseNotes.md) for package version history.
