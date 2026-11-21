# Business applications

Power Platform, Microsoft Dataverse, Dynamics 365 and Microsoft Copilot Studio.

## What are you trying to do?

| I'm trying to... | Do this |
|---|---|
| **Detect DLP policy edits, tenant isolation changes, risky Power Automate flows or wide Power App sharing** | Start with [Power Platform](power-platform/README.md) (`PowerPlatformAdminActivity`, `PowerAutomateActivity`). |
| **Monitor Dataverse / Dynamics 365 CE mass exports, role abuse or Dynamics 365 F&O bank-account fraud** | Open [Microsoft Dataverse and Dynamics 365](dataverse-dynamics-365/README.md) (`DataverseActivity`, `FinanceOperationsActivity_CL`). |
| **Block or detect unauthenticated Copilot Studio agents, jailbreak flags and agent inventory** | Open [Microsoft Copilot Studio](copilot-studio/README.md) (`CopilotActivity`, Dataverse `bot` audit, `AgentsInfo`). |
| **Check if all Business applications tables are landing** | Run [business-apps.kql](../queries/validation/business-apps.kql). |

## Guides in this group

| Guide | Priority | Primary tables | Default tier | Status |
|---|---|---|---|---|
| [Power Platform (Power Apps, Power Automate, admin)](power-platform/README.md) | P2 | `PowerPlatformAdminActivity`, `PowerAutomateActivity` | Analytics | Verified |
| [Microsoft Dataverse and Dynamics 365](dataverse-dynamics-365/README.md) | P2 | `DataverseActivity`, `FinanceOperationsActivity_CL` | Analytics (DCR-filter noisy Read logs if enabled) | Verified |
| [Microsoft Copilot Studio](copilot-studio/README.md) | P2 | `CopilotActivity`, `DataverseActivity` (`bot`), `AgentsInfo` | Analytics (or Data lake for hunt-only `CopilotActivity`) | Verified |
