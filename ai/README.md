# AI

Microsoft 365 Copilot and Microsoft Foundry (formerly Azure AI Foundry), including Azure OpenAI.

## What are you trying to do?

| I'm trying to... | Do this |
|---|---|
| **Monitor Microsoft 365 Copilot interactions, jailbreak flags, plugin tampering and DSPM for AI** | Open [Microsoft 365 Copilot](microsoft-365-copilot/README.md) (`CopilotActivity`, `OfficeActivity`, `CloudAppEvents`). |
| **Monitor Azure OpenAI and Microsoft Foundry API keys, model deployments, inference usage and Defender for AI alerts** | Open [Microsoft Foundry and Azure OpenAI](azure-openai-ai-foundry/README.md). |
| **Monitor custom Copilot Studio agents** | Go to [Microsoft Copilot Studio](../business-apps/copilot-studio/README.md) under Business applications. |
| **Check if all AI tables are landing** | Run [ai.kql](../queries/validation/ai.kql). |

## Guides in this group

| Guide | Priority | Primary tables | Default tier | Status |
|---|---|---|---|---|
| [Microsoft 365 Copilot](microsoft-365-copilot/README.md) | P2 | `CopilotActivity`, `OfficeActivity` (free), `CloudAppEvents` | Analytics (or Data lake if hunt-only) | Verified |
| [Microsoft Foundry (formerly Azure AI Foundry) and Azure OpenAI](azure-openai-ai-foundry/README.md) | P2 | `AzureDiagnostics` (`Audit`, `RequestResponse`, `AzureOpenAIRequestUsage`), `AzureActivity` (free), `SecurityAlert` (free) | Analytics (`Audit` & alerts); Data lake (`RequestResponse`/usage) | Verified |
