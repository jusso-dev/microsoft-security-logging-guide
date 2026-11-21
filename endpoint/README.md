# Endpoint

Device telemetry from Microsoft Defender for Endpoint, Windows client event logs and Microsoft Intune.

## What are you trying to do?

| I'm trying to... | Do this |
|---|---|
| **Get endpoint EDR alerts and process/network hunting without blowing up Sentinel cost** | Start with [Microsoft Defender for Endpoint](defender-for-endpoint/README.md). Keep `Device*` tables in Defender XDR advanced hunting (free for 30 days, or 90 days on ISOC) and sync alerts/incidents free. |
| **Collect Windows Security and PowerShell logs from workstations via AMA** | Follow [Windows security event logs (clients)](windows-security-events/README.md). Skip duplicating events Defender for Endpoint already captures unless compliance requires them. |
| **Alert on Intune device wipes, script pushes or compliance tampering** | Follow [Microsoft Intune](intune/README.md) (`IntuneAuditLogs`, `IntuneOperationalLogs`). |
| **Check if all Endpoint tables are landing** | Run [endpoint.kql](../queries/validation/endpoint.kql). |

## Guides in this group

| Guide | Priority | Primary tables | Default tier | Status |
|---|---|---|---|---|
| [Microsoft Defender for Endpoint](defender-for-endpoint/README.md) | P1 (start here) | `DeviceProcessEvents`, `DeviceNetworkEvents`, `DeviceFileEvents`, `SecurityAlert` (free) | Defender XDR default (Data lake only if >30/90d retention needed) | Verified |
| [Windows security event logs (clients)](windows-security-events/README.md) | P1 (start here) | `SecurityEvent`, `WindowsEvent`, `Event` | Analytics (DCR-filtered) | Verified |
| [Microsoft Intune](intune/README.md) | P2 | `IntuneAuditLogs`, `IntuneOperationalLogs`, `IntuneDevices` | Analytics (audit/ops); Data lake (inventory) | Verified |
