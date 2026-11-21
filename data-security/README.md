# Data security

Microsoft Purview Data Loss Prevention, Insider Risk Management and Information Protection telemetry.

## What are you trying to do?

| I'm trying to... | Do this |
|---|---|
| **Surface DLP matches, user overrides and DLP policy tampering (and understand why DLP alerts show up as behaviours)** | Open [Microsoft Purview Data Loss Prevention](purview-dlp/README.md). |
| **Correlate insider risk alerts with SOC incidents while managing HR/privacy pseudonymisation tradeoffs** | Open [Microsoft Purview Insider Risk Management](insider-risk/README.md). |
| **Detect sensitivity label downgrades or removals across files and endpoints** | Open [Microsoft Purview Information Protection](information-protection/README.md). |
| **Check if all Data security tables are landing** | Run [data-security.kql](../queries/validation/data-security.kql). |

## Guides in this group

| Guide | Priority | Primary tables | Default tier | Status |
|---|---|---|---|---|
| [Microsoft Purview Data Loss Prevention](purview-dlp/README.md) | P2 | `OfficeActivity` (free), `AlertInfo` / `SecurityAlert` (free), `BehaviorInfo`, `DataSecurityEvents` | Analytics (alerts & `OfficeActivity`); Defender XDR default (behaviours/raw) | Verified |
| [Microsoft Purview Insider Risk Management](insider-risk/README.md) | P3 | `AlertInfo` / `SecurityAlert` (free), `DataSecurityEvents`, `OfficeActivity` (free) | Analytics (alerts); Defender XDR default (`DataSecurityEvents`) | Verified |
| [Microsoft Purview Information Protection](information-protection/README.md) | P3 | `MicrosoftPurviewInformationProtection`, `OfficeActivity` (free), `DeviceFileEvents` | Analytics (or Data lake if scanner volume is high) | Verified |
