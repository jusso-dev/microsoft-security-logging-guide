# Identity

Sign-in, directory, risk and on-premises identity telemetry. Identity is the first thing to get right because almost every other detection joins back to it.

## What are you trying to do?

| I'm trying to... | Do this |
|---|---|
| **Detect password spray, token replay, MFA fatigue or illicit OAuth consent** | Start with [Microsoft Entra ID](entra-id/README.md) (`SigninLogs`, `AuditLogs`, `AADNonInteractiveUserSignInLogs`, `AADServicePrincipalSignInLogs`). |
| **Alert on compromised accounts, risky users or risky workload identities** | Open [Microsoft Entra ID Protection](entra-id-protection/README.md) (`AADUserRiskEvents`, `AADRiskyUsers`, free `SecurityAlert`). |
| **Detect Kerberoasting, DCSync, Pass-the-Hash or Golden Ticket on-premises** | Enable [Microsoft Defender for Identity](defender-for-identity/README.md) first, then collect DC security events with [Active Directory Domain Services](active-directory-on-prem/README.md). |
| **Monitor legacy AD FS token signing and federation abuse** | Follow [Active Directory Federation Services (AD FS)](adfs/README.md). Skip if you are cloud-only or migrated off AD FS. |
| **Monitor Global Secure Access (Internet and Private Access) network traffic** | Follow [Microsoft Entra Global Secure Access](entra-global-secure-access/README.md) and route `NetworkAccessTraffic` to the Data lake tier. |
| **Check if all Identity tables are landing** | Run [identity.kql](../queries/validation/identity.kql). |

## Guides in this group

| Guide | Priority | Primary tables | Default tier | Status |
|---|---|---|---|---|
| [Microsoft Entra ID (sign-in, audit and Graph activity logs)](entra-id/README.md) | P1 (start here) | `SigninLogs`, `AuditLogs`, `AADServicePrincipalSignInLogs`, `MicrosoftGraphActivityLogs` | Analytics (Graph and Provisioning in Data lake) | Verified |
| [Microsoft Entra ID Protection (risk detections)](entra-id-protection/README.md) | P1 (start here) | `SecurityAlert` (free), `AADUserRiskEvents`, `AADRiskyUsers` | Analytics | Verified |
| [Microsoft Defender for Identity](defender-for-identity/README.md) | P1 (start here) | `IdentityLogonEvents`, `IdentityQueryEvents`, `IdentityDirectoryEvents`, `SecurityAlert` (free) | Defender XDR default (alerts in Analytics) | Verified |
| [Active Directory Domain Services (on-premises)](active-directory-on-prem/README.md) | P1 (start here) | `SecurityEvent` (`Common` + XPath 4769/4776) | Analytics | Verified |
| [Active Directory Federation Services (AD FS)](adfs/README.md) | P1 (start here) | `ADFSSignInLogs`, `SecurityEvent` | Analytics | Verified |
| [Microsoft Entra Internet Access and Private Access (Global Secure Access)](entra-global-secure-access/README.md) | P3 | `NetworkAccessTraffic`, `RemoteNetworkHealthLogs`, `NetworkAccessAlerts` | Data lake (`NetworkAccessTraffic`); Analytics (alerts/health) | Verified |
