# Cloud apps

SaaS activity, OAuth app governance and shadow IT discovery through Microsoft Defender for Cloud Apps.

## What are you trying to do?

| I'm trying to... | Do this |
|---|---|
| **Monitor connected SaaS apps, OAuth app abuse and cloud app sessions without duplicate billing** | Open [Microsoft Defender for Cloud Apps](defender-for-cloud-apps/README.md). Keep `CloudAppEvents` in Defender XDR advanced hunting unless Sentinel rules or >30/90 day retention need it, and sync alerts free. |
| **Retain shadow IT discovery logs long term** | Follow the classic discovery section of [Microsoft Defender for Cloud Apps](defender-for-cloud-apps/README.md) and put `McasShadowItReporting` in the Data lake tier. |
| **Check if Cloud apps tables are landing** | Run [cloud-apps.kql](../queries/validation/cloud-apps.kql). |

## Guides in this group

| Guide | Priority | Primary tables | Default tier | Status |
|---|---|---|---|---|
| [Microsoft Defender for Cloud Apps](defender-for-cloud-apps/README.md) | P2 | `CloudAppEvents`, `McasShadowItReporting`, `SecurityAlert` (free) | Defender XDR default (`CloudAppEvents`); Data lake (`McasShadowItReporting`) | Verified |
