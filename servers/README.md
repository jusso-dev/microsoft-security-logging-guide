# Servers

Windows Server, Linux hosts, Syslog/CEF network appliances and SQL Server on-premises or IaaS via the Azure Monitor Agent (AMA) and Azure Arc.

## What are you trying to do?

| I'm trying to... | Do this |
|---|---|
| **Collect Windows Server security events, PowerShell 4104, DNS Server or IIS logs via AMA (and use your Defender for Servers P2 500 MB/day grant)** | Open [Windows Server](windows-server/README.md). |
| **Collect Linux `auth`/`authpriv`, `auditd` or third-party firewall/appliance CEF and Syslog via AMA** | Open [Linux (Syslog, CEF and auditd)](linux-syslog/README.md). |
| **Audit on-premises or IaaS SQL Server logins, permissions and Defender for SQL on machines** | Open [SQL Server (on-premises and IaaS)](sql-server/README.md) (write audit to Windows Security log Event ID `33205`). |
| **Collect Domain Controller events specifically** | Go to [Active Directory Domain Services](../identity/active-directory-on-prem/README.md) under Identity. |
| **Check if all Servers tables are landing** | Run [servers.kql](../queries/validation/servers.kql). |

## Guides in this group

| Guide | Priority | Primary tables | Default tier | Status |
|---|---|---|---|---|
| [Windows Server](windows-server/README.md) | P2 | `SecurityEvent`, `Event`, `ASimDnsActivityLogs`, `W3CIISLog`, `MDCFileIntegrityMonitoringEvents` | Analytics (`SecurityEvent`, `Event`, FIM); Data lake (DNS, IIS) | Verified |
| [Linux (Syslog, CEF and auditd)](linux-syslog/README.md) | P2 | `Syslog`, `CommonSecurityLog`, `Device*` (MDE on Linux) | Analytics (`auth`/`authpriv`, IDS/IPS); Data lake (verbose firewall CEF) | Verified |
| [SQL Server (on-premises and IaaS)](sql-server/README.md) | P3 | `SecurityEvent` (ID `33205`), `Event`, `SecurityAlert` (free) | Analytics | Verified |
