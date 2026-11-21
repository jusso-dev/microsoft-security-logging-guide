# Azure

Azure control plane, Microsoft Defender for Cloud and the Azure resource logs that matter most for security.

## What are you trying to do?

| I'm trying to... | Do this |
|---|---|
| **Log every Azure RBAC, resource delete, key and policy change for free** | Start with [Azure Activity (control plane)](azure-activity/README.md) and enforce it via Azure Policy at management group scope. |
| **Bring Defender for Cloud alerts into Sentinel without duplicate or empty incidents** | Open [Microsoft Defender for Cloud](defender-for-cloud/README.md). Enable both Defender XDR integration and the tenant-based Defender for Cloud connector. |
| **Detect secret dumping, key deletion or vault policy tampering** | Open [Azure Key Vault](key-vault/README.md) (`AZKVAuditLogs` or `AzureDiagnostics`). |
| **Detect blob/file exfiltration or ransomware deletes without huge ingestion bills** | Open [Azure Storage](storage/README.md) and route high-volume data-plane logs to the Data lake tier. |
| **Audit Azure SQL access, schema changes and Microsoft support operations** | Open [Azure SQL Database and Managed Instance](azure-sql/README.md). |
| **Catch Kubernetes pod exec, RBAC changes and secret access in AKS** | Open [Azure Kubernetes Service (AKS)](aks/README.md) and use `AKSAuditAdmin` (not noisy `AKSAudit`) in Analytics. |
| **Log VNet flow logs, Azure Firewall, WAF, DNS and DDoS (and migrate off NSG flow logs)** | Open [Azure networking](network-nsg-flow-firewall/README.md). Keep threat intel/IDPS in Analytics and flow/rule logs in Data lake. |
| **Catch rogue FTP/Kudu deployments or web attacks on App Service and Functions** | Open [Azure App Service and Azure Functions](app-service-functions/README.md). |
| **Check if all Azure tables are landing** | Run [azure.kql](../queries/validation/azure.kql). |

## Guides in this group

| Guide | Priority | Primary tables | Default tier | Status |
|---|---|---|---|---|
| [Azure Activity (control plane)](azure-activity/README.md) | P1 (start here) | `AzureActivity` (free) | Analytics | Verified |
| [Microsoft Defender for Cloud](defender-for-cloud/README.md) | P2 | `SecurityAlert` (free), `SecurityRecommendation`, `SecureScores` | Analytics (`SecurityAlert`); Data lake (posture export) | Verified |
| [Azure Key Vault](key-vault/README.md) | P2 | `AZKVAuditLogs` (or `AzureDiagnostics`) | Analytics | Verified |
| [Azure Storage](storage/README.md) | P2 | `StorageBlobLogs`, `StorageFileLogs`, `StorageQueueLogs`, `StorageTableLogs` | Data lake (Analytics for crown-jewel accounts) | Verified |
| [Azure SQL Database and Managed Instance](azure-sql/README.md) | P2 | `AzureDiagnostics` (`SQLSecurityAuditEvents`, `DevOpsOperationsAudit`), `SecurityAlert` (free) | Analytics (Data lake for verbose query logs) | Verified |
| [Azure Kubernetes Service (AKS)](aks/README.md) | P2 | `AKSAuditAdmin`, `AKSAudit`, `AKSControlPlane`, `ContainerLogV2` | Analytics (`AKSAuditAdmin`); Data lake (rest) | Verified |
| [Azure networking (VNet flow logs, Azure Firewall, WAF, DNS)](network-nsg-flow-firewall/README.md) | P2 | `AZFWThreatIntel`, `AZFWIdpsSignature`, `AZFWNetworkRule`, `NTANetAnalytics`, `AGWFirewallLogs` | Analytics (TI/IDPS/WAF); Data lake (flow/rule logs) | Verified |
| [Azure App Service and Azure Functions](app-service-functions/README.md) | P3 | `AppServiceAuditLogs`, `AppServiceIPSecAuditLogs`, `AppServiceHTTPLogs`, `FunctionAppLogs` | Analytics (audit/IPSec); Data lake (HTTP/app/function) | Verified |
