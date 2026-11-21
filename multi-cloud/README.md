# Multi-cloud (optional)

Amazon Web Services and Google Cloud sources that commonly sit alongside Microsoft estates in Sentinel.

## What are you trying to do?

| I'm trying to... | Do this |
|---|---|
| **Ingest AWS CloudTrail, GuardDuty and VPC Flow Logs into Sentinel via S3 + OIDC** | Open [Amazon Web Services](aws/README.md). Keep `AWSCloudTrail` and `AWSGuardDuty` in Analytics and `AWSVPCFlow` in the Data lake tier. |
| **Ingest Google Cloud Audit Logs, Security Command Center, DNS and VPC Flow Logs via CCF + Workload Identity Federation** | Open [Google Cloud](google-cloud/README.md). Keep `GCPAuditLogs` and `GoogleCloudSCC` in Analytics and `GCPDNS` / `GCPVPCFlow` in the Data lake tier. |
| **Check if Multi-cloud tables are landing** | Run [multi-cloud.kql](../queries/validation/multi-cloud.kql). |

## Guides in this group

| Guide | Priority | Primary tables | Default tier | Status |
|---|---|---|---|---|
| [Amazon Web Services (optional)](aws/README.md) | P3 | `AWSCloudTrail`, `AWSGuardDuty`, `AWSVPCFlow`, `AWSNetworkFirewall` | Analytics (CloudTrail/GuardDuty); Data lake (VPCFlow) | Verified |
| [Google Cloud (optional)](google-cloud/README.md) | P3 | `GCPAuditLogs`, `GoogleCloudSCC`, `GCPDNS`, `GCPVPCFlow` | Analytics (Audit/SCC); Data lake (DNS/VPCFlow) | Verified |
