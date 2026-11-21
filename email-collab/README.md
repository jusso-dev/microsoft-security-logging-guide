# Email and collaboration

Exchange Online, Microsoft Defender for Office 365, SharePoint Online, OneDrive, Microsoft Teams and the Microsoft Purview unified audit log.

## What are you trying to do?

| I'm trying to... | Do this |
|---|---|
| **Turn on the underlying audit feed every Microsoft 365 connector needs** | Start with [Microsoft Purview unified audit log](purview-unified-audit/README.md). `OfficeActivity` for Exchange, SharePoint and Teams is free in Sentinel. |
| **Detect BEC, malicious inbox forwarding rules, mailbox delegation or `MailItemsAccessed`** | Open [Exchange Online](exchange-online/README.md). |
| **Hunt phishing emails, malicious attachments and Safe Links clicks** | Open [Microsoft Defender for Office 365](defender-for-office-365/README.md). Keep `Email*` and `UrlClickEvents` in Defender XDR by default and sync alerts free. |
| **Detect mass file downloads, anonymous links or external sharing** | Open [SharePoint Online and OneDrive](sharepoint-onedrive/README.md). |
| **Monitor external Teams phishing, guest invites and Teams admin changes** | Open [Microsoft Teams](teams/README.md). |
| **Check if all Email and collaboration tables are landing** | Run [email-collab.kql](../queries/validation/email-collab.kql). |

## Guides in this group

| Guide | Priority | Primary tables | Default tier | Status |
|---|---|---|---|---|
| [Exchange Online](exchange-online/README.md) | P1 (start here) | `OfficeActivity` (free), `EmailEvents` | Analytics | Verified |
| [Microsoft Defender for Office 365](defender-for-office-365/README.md) | P1 (start here) | `EmailEvents`, `UrlClickEvents`, `EmailPostDeliveryEvents`, `SecurityAlert` (free) | Defender XDR default (Analytics if Sentinel rules read them) | Verified |
| [SharePoint Online and OneDrive](sharepoint-onedrive/README.md) | P2 | `OfficeActivity` (free), `CloudAppEvents`, `FileMaliciousContentInfo` | Analytics (`OfficeActivity`); Defender XDR default (rest) | Verified |
| [Microsoft Teams](teams/README.md) | P2 | `OfficeActivity` (free), `MessageEvents`, `CallActivityEvents` | Analytics (`OfficeActivity`); Defender XDR default (rest) | Verified |
| [Microsoft Purview unified audit log](purview-unified-audit/README.md) | P1 (start here) | `OfficeActivity` (free), `SentinelHealth` (free) | Analytics | Verified |
