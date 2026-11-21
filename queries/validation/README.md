# Validation query pack

KQL queries that verify whether every documented Microsoft Sentinel table is landing, how fresh it is, and how much volume (GB/day) it generates.

Run these in the Microsoft Defender portal under **Investigation & response > Advanced hunting** (with your Sentinel workspace selected) or in Log Analytics **Logs**.

- Tables set to **Data lake tier only** do not appear in Analytics workspace `union` queries; verify those in **Data lake exploration** or on the connector status graph.
- Native Defender XDR tables (`Device*`, `Email*`, `Identity*`, `CloudAppEvents`, `EntraIdSignInEvents`, `BehaviorInfo`, `AgentsInfo`) only appear in Sentinel queries if you turned on raw event streaming. Otherwise, query them directly in Defender XDR advanced hunting.
- For connector-level polling failures (`SentinelHealth`) and silent-source alerting, see [docs/sentinel-health.md](../../docs/sentinel-health.md).

## Master health check

- [health-all-tables.kql](health-all-tables.kql): single `union isfuzzy=true` check against the expected table list across all 11 groups plus `SentinelHealth`, `SentinelAudit` and `LAQueryLogs`. Trim `ExpectedTables` to your active connectors before scheduling it as an alert rule.

## Group validation queries

| Group | Query file | Covers |
|---|---|---|
| Identity | [identity.kql](identity.kql) | Entra ID, ID Protection, Defender for Identity, AD DS, AD FS, Global Secure Access |
| Endpoint | [endpoint.kql](endpoint.kql) | Defender for Endpoint, Windows security events (clients), Intune |
| Email and collaboration | [email-collab.kql](email-collab.kql) | Exchange Online, Defender for Office 365, SharePoint and OneDrive, Teams, Purview audit |
| Cloud apps | [cloud-apps.kql](cloud-apps.kql) | Defender for Cloud Apps |
| Azure | [azure.kql](azure.kql) | Azure Activity, Defender for Cloud, Key Vault, Storage, Azure SQL, AKS, networking, App Service and Functions |
| Data security | [data-security.kql](data-security.kql) | Purview DLP, Insider Risk Management, Information Protection |
| Business applications | [business-apps.kql](business-apps.kql) | Power Platform, Dataverse and Dynamics 365, Copilot Studio |
| AI | [ai.kql](ai.kql) | Microsoft 365 Copilot, Microsoft Foundry and Azure OpenAI |
| DevOps | [devops.kql](devops.kql) | GitHub (Enterprise Cloud), Azure DevOps |
| Servers | [servers.kql](servers.kql) | Windows Server, Linux (Syslog, CEF and auditd), SQL Server |
| Multi-cloud | [multi-cloud.kql](multi-cloud.kql) | Amazon Web Services, Google Cloud |
