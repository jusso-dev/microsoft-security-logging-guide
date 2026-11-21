# Microsoft Defender XDR custom detections

This folder contains Defender XDR custom detection rule definitions and advanced hunting queries for every detection in the guide that queries native Microsoft Defender XDR tables (`DeviceProcessEvents`, `DeviceNetworkEvents`, `DeviceFileEvents`, `EmailPostDeliveryEvents`, `UrlClickEvents`, `IdentityDirectoryEvents`, `IdentityLogonEvents`, `CloudAppEvents`, `AgentsInfo`, `DataSecurityEvents`, `BehaviorInfo` and `BehaviorEntities`).

Running these directly in Microsoft Defender XDR avoids paying Microsoft Sentinel ingestion fees for raw Defender XDR telemetry while still using the included 30-day advanced hunting window (or 90 days on eligible ISOC plans). See [Defender XDR vs Sentinel](../docs/defender-xdr-vs-sentinel.md) for the cost and deduplication decision table.

## Inventory

### Custom detection rules (`defender-xdr/rules/`)

Every rule YAML includes the KQL query (adapted to `Timestamp` and projecting `Timestamp`, `ReportId`, plus `DeviceId` for Defender for Endpoint tables), run frequency, lookback period, severity, MITRE ATT&CK mapping, entity mappings and recommended response actions.

| Rule file | Product | Tables | Severity | Frequency |
|---|---|---|---|---|
| `defender_for_endpoint_C1_Office_app_spawns_a_script_interpreter.yaml` | Defender for Endpoint | `DeviceProcessEvents`, `DeviceNetworkEvents` | High | `PT1H` |
| `defender_for_endpoint_C2_Process_hash_matches_a_non_Microsoft.yaml` | Defender for Endpoint | `DeviceProcessEvents` | Medium | `PT1H` |
| `defender_for_endpoint_C3_Regular_low_rate_beaconing.yaml` | Defender for Endpoint | `DeviceNetworkEvents` | Medium | `P1D` |
| `defender_for_office_365_C1_ZAP_or_manual_remediation_failed_on.yaml` | Defender for Office 365 | `EmailPostDeliveryEvents` | High | `PT1H` |
| `defender_for_office_365_C2_User_clicked_through_a_Safe_Links.yaml` | Defender for Office 365 | `UrlClickEvents` | High | `PT1H` |
| `defender_for_office_365_C3_A_URL_domain_clicked_today_was_blocked.yaml` | Defender for Office 365 | `UrlClickEvents` | Medium | `P1D` |
| `defender_for_identity_C1_MDI_sensor_silence_per_domain_controller.yaml` | Defender for Identity | `IdentityDirectoryEvents` | High | `PT1H` |
| `defender_for_identity_C2_Dormant_account_added_to_a_privileged.yaml` | Defender for Identity | `IdentityDirectoryEvents`, `IdentityLogonEvents` | High | `PT1H` |
| `defender_for_cloud_apps_C1_Unusual_download_volume_from_a_web.yaml` | Defender for Cloud Apps | `CloudAppEvents` | High | `PT1H` |
| `defender_for_cloud_apps_C2_Mass_delete_in_a_non_Microsoft_SaaS_app.yaml` | Defender for Cloud Apps | `CloudAppEvents` | High | `PT1H` |
| `defender_for_cloud_apps_C3_Bulk_download_by_an_external_or_guest.yaml` | Defender for Cloud Apps | `CloudAppEvents` | High | `PT1H` |
| `information_protection_C3_Encrypted_or_highly_sensitive_files.yaml` | Purview Information Protection | `DeviceFileEvents` | Medium | `PT1H` |
| `insider_risk_C3_Repeated_blocked_or_bypassed_data.yaml` | Purview Insider Risk Management | `DataSecurityEvents` | Medium | `PT1H` |
| `purview_dlp_C3_High_volume_DLP_behaviours_in_Defender.yaml` | Purview Data Loss Prevention | `BehaviorInfo`, `BehaviorEntities` | Medium | `PT1H` |
| `copilot_studio_C4_Published_Copilot_Studio_agent_with.yaml` | Copilot Studio | `AgentsInfo` | Medium | `P1D` |

Three of these rules (`AgentsInfo`, `DataSecurityEvents` and `BehaviorInfo`/`BehaviorEntities`) query tables that are only available in Defender XDR advanced hunting and cannot be streamed to Microsoft Sentinel.

### Advanced hunting queries (`defender-xdr/hunting/`)

Standalone `.kql` files ready to paste into **Investigation & response > Hunting > Advanced hunting**:

- `copilot_studio_H1_Microsoft_Copilot_Studio_advanced.kql` (`AgentsInfo` active agent census)
- `defender_for_cloud_apps_H1_Events_MDCA_enrichment_flagged_as.kql` (`CloudAppEvents` uncommon events)
- `insider_risk_H1_High_risk_actions_on_renamed.kql` (`DataSecurityEvents` renamed sensitive files)
- `purview_dlp_H1_Endpoint_DLP_policy_matches_in.kql` (`DataSecurityEvents` endpoint DLP matches)
- `purview_dlp_H2_Cloud_DLP_matches_joined_to_recent.kql` (`EntraIdSignInEvents` + `CloudAppEvents` risky sign-ins with DLP matches)
- `xdr_streaming_cost_preview.kql` (pre-streaming GB/day estimate across XDR tables)

## How to import into Microsoft Defender XDR

### Option 1: Microsoft Defender portal (manual)

1. Open the [Microsoft Defender portal](https://security.microsoft.com) and go to **Investigation & response > Hunting > Advanced hunting**.
2. Open the YAML file from `defender-xdr/rules/` and copy the `query` block into the query editor.
3. Review any `// ASSUMPTION:` lines and run the query over the last 7 days to check baseline volume and tune thresholds.
4. Select **Create detection rule** in the toolbar.
5. Copy the metadata fields from the YAML file into the wizard:
   - **Detection name** and **Alert title**: `displayName`
   - **Frequency**: `frequency` (`PT1H` = Every hour, `P1D` = Every 24 hours)
   - **Severity**: `severity`
   - **MITRE ATT&CK techniques**: `tactics` and `relevantTechniques`
   - **Description** and **Recommended actions**: `description` and `recommendedActions`
   - **Impacted entities**: map each entry under `entityMappings` (`entityType`, `identifier`, `columnName`)
6. Choose target device/user scopes and optional automated response actions, then save.

### Option 2: Microsoft Graph Security API (automated)

Microsoft Defender XDR custom detection rules can be created programmatically via the Microsoft Graph Security detection rules API (`POST https://graph.microsoft.com/v1.0/security/rules/detectionRules`, requiring `CustomDetection.ReadWrite.All` permission; see [detectionRule resource type in Microsoft Learn](https://learn.microsoft.com/en-us/graph/api/resources/security-detectionrule?view=graph-rest-1.0)).

Map each YAML file to the API payload:

- `displayName` -> `displayName`
- `query` -> `queryCondition.queryText`
- `frequency` -> `schedule.period` (`"1H"` for `PT1H`, `"24H"` for `P1D`)
- `severity`, `description`, `tactics`, `recommendedActions` -> `detectionAction.alertTemplate`
- `entityMappings` -> `detectionAction.alertTemplate.impactedAssets`

## Avoiding duplicate alerts

If you also deployed the Microsoft Sentinel solution in [solution/](../solution/README.md), enable only **one** copy of any overlapping rule (`Device*`, `Email*`, `UrlClickEvents`, `Identity*`, `CloudAppEvents`). Use the Defender XDR copy by default and leave the Sentinel analytic rule template disabled unless you require Sentinel-only correlation or retention beyond 30/90 days.

## Official links

- [Overview of custom detections in Microsoft Defender XDR](https://learn.microsoft.com/en-us/defender-xdr/custom-detections-overview)
- [Create and manage custom detection rules](https://learn.microsoft.com/en-us/defender-xdr/custom-detection-rules)
- [Data tables in the Microsoft Defender advanced hunting schema](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-schema-tables)
- [Microsoft Graph Security detectionRule resource type](https://learn.microsoft.com/en-us/graph/api/resources/security-detectionrule?view=graph-rest-1.0)
