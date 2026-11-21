#!/usr/bin/env python3
"""Package KQL detections, hunting queries and workbooks from the guide into:

1. A Microsoft Sentinel Content Hub V3 solution under
   solution/Solutions/MicrosoftSecurityLoggingGuide/ (Data manifest,
   SolutionMetadata.json, Analytic Rules YAML, Hunting Queries YAML,
   Workbooks JSON, Package/mainTemplate.json, Package/createUiDefinition.json).
2. Microsoft Defender XDR custom detection definitions and advanced hunting
   queries under defender-xdr/ for rules targeting Defender XDR tables.

All guide Markdown files remain untouched as the single source of truth.
Deterministic UUIDv5 identifiers ensure stable diffs across rebuilds.
"""

from __future__ import annotations

import json
import re
import shutil
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SOLUTION_NAME = "MicrosoftSecurityLoggingGuide"
SOLUTION_DISPLAY_NAME = "Microsoft Security Logging Guide"
SOLUTION_VERSION = "3.0.0"
SOLUTION_ID = "jusso-dev.microsoft-security-logging-guide"
PUBLISHER_ID = "jusso-dev"
OFFER_ID = "microsoft-security-logging-guide"
AUTHOR_NAME = "jusso-dev"
SUPPORT_LINK = "https://github.com/jusso-dev/microsoft-security-logging-guide/issues"
REPO_URL = "https://github.com/jusso-dev/microsoft-security-logging-guide"
FIRST_PUBLISH_DATE = "2026-11-21"

SOLUTION_DIR = ROOT / "solution" / "Solutions" / SOLUTION_NAME
XDR_DIR = ROOT / "defender-xdr"

UUID_NS = uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/jusso-dev/microsoft-security-logging-guide")

# Defender XDR tables that cannot be streamed into Sentinel Log Analytics workspaces
XDR_ONLY_TABLES = {
    "AgentsInfo",
    "DataSecurityEvents",
    "BehaviorInfo",
    "BehaviorEntities",
    "EntraIdSignInEvents",
    "EntraIdSpnSignInEvents",
    "EntraIdDirectoryAuditEvents",
    "GraphAPIAuditEvents",
}

# All Defender XDR advanced hunting tables (native or dual-streamed)
XDR_ALL_TABLES = XDR_ONLY_TABLES | {
    "DeviceEvents",
    "DeviceProcessEvents",
    "DeviceNetworkEvents",
    "DeviceFileEvents",
    "DeviceRegistryEvents",
    "DeviceLogonEvents",
    "DeviceImageLoadEvents",
    "DeviceInfo",
    "DeviceNetworkInfo",
    "DeviceFileCertificateInfo",
    "EmailEvents",
    "EmailUrlInfo",
    "EmailAttachmentInfo",
    "EmailPostDeliveryEvents",
    "UrlClickEvents",
    "IdentityLogonEvents",
    "IdentityDirectoryEvents",
    "IdentityQueryEvents",
    "CloudAppEvents",
    "AlertInfo",
    "AlertEvidence",
    "OAuthAppInfo",
}

MDE_DEVICE_TABLES = {
    "DeviceEvents",
    "DeviceProcessEvents",
    "DeviceNetworkEvents",
    "DeviceFileEvents",
    "DeviceRegistryEvents",
    "DeviceLogonEvents",
    "DeviceImageLoadEvents",
    "DeviceInfo",
    "DeviceNetworkInfo",
    "DeviceFileCertificateInfo",
}

# Map Sentinel Log Analytics table names -> official Sentinel Data Connector IDs
TABLE_TO_CONNECTOR: dict[str, str] = {
    # Entra ID & Identity
    "SigninLogs": "AzureActiveDirectory",
    "AADNonInteractiveUserSignInLogs": "AzureActiveDirectory",
    "AADServicePrincipalSignInLogs": "AzureActiveDirectory",
    "AADManagedIdentitySignInLogs": "AzureActiveDirectory",
    "AuditLogs": "AzureActiveDirectory",
    "AADProvisioningLogs": "AzureActiveDirectory",
    "MicrosoftGraphActivityLogs": "AzureActiveDirectory",
    "ADFSSignInLogs": "AzureActiveDirectory",
    "AADUserRiskEvents": "AzureActiveDirectoryIdentityProtection",
    "AADRiskyUsers": "AzureActiveDirectoryIdentityProtection",
    "AADRiskyServicePrincipals": "AzureActiveDirectoryIdentityProtection",
    "AADServicePrincipalRiskEvents": "AzureActiveDirectoryIdentityProtection",
    "NetworkAccessTraffic": "GlobalSecureAccess",
    "NetworkAccessGenerativeAIInsights": "GlobalSecureAccess",
    # Defender XDR / M365 Defender
    "DeviceProcessEvents": "MicrosoftThreatProtection",
    "DeviceNetworkEvents": "MicrosoftThreatProtection",
    "DeviceFileEvents": "MicrosoftThreatProtection",
    "DeviceRegistryEvents": "MicrosoftThreatProtection",
    "DeviceLogonEvents": "MicrosoftThreatProtection",
    "DeviceImageLoadEvents": "MicrosoftThreatProtection",
    "DeviceEvents": "MicrosoftThreatProtection",
    "DeviceInfo": "MicrosoftThreatProtection",
    "EmailEvents": "MicrosoftThreatProtection",
    "EmailUrlInfo": "MicrosoftThreatProtection",
    "EmailAttachmentInfo": "MicrosoftThreatProtection",
    "EmailPostDeliveryEvents": "MicrosoftThreatProtection",
    "UrlClickEvents": "MicrosoftThreatProtection",
    "IdentityLogonEvents": "MicrosoftThreatProtection",
    "IdentityDirectoryEvents": "MicrosoftThreatProtection",
    "IdentityQueryEvents": "MicrosoftThreatProtection",
    "CloudAppEvents": "MicrosoftThreatProtection",
    "AlertInfo": "MicrosoftThreatProtection",
    "AlertEvidence": "MicrosoftThreatProtection",
    "SecurityAlert": "MicrosoftThreatProtection",
    "SecurityIncident": "MicrosoftThreatProtection",
    # M365 / Office / Purview / Copilot
    "OfficeActivity": "Office365",
    "CopilotActivity": "MicrosoftCopilot",
    "MicrosoftPurviewInformationProtection": "MicrosoftPurviewInformationProtection",
    # Business Applications
    "PowerPlatformAdminActivity": "PowerPlatformAdmin",
    "PowerAutomateActivity": "PowerAutomate",
    "PowerAppsActivity": "PowerApps",
    "DataverseActivity": "Dataverse",
    "FinanceOperationsActivity_CL": "Dynamics365",
    # Endpoint & Servers
    "SecurityEvent": "SecurityEvents",
    "WindowsEvent": "WindowsSecurityEvents",
    "Event": "WindowsForwardedEvents",
    "IntuneAuditLogs": "Intune",
    "IntuneOperationalLogs": "Intune",
    "IntuneDevices": "Intune",
    "Syslog": "SyslogAma",
    "CommonSecurityLog": "CefAma",
    "W3CIISLog": "AzureMonitorWindowsAgent",
    "ASimDnsActivityLogs": "WindowsServerDNS",
    # Azure
    "AzureActivity": "AzureActivity",
    "AzureDiagnostics": "AzureActivity",
    "AZKVAuditLogs": "AzureKeyVault",
    "StorageBlobLogs": "AzureStorageAccount",
    "StorageFileLogs": "AzureStorageAccount",
    "AKSAuditAdmin": "AzureKubernetesServices",
    "AKSAudit": "AzureKubernetesServices",
    "AppServiceAuditLogs": "AzureAppService",
    "AppServiceHTTPLogs": "AzureAppService",
    "AppServiceIPSecAuditLogs": "AzureAppService",
    "FunctionAppLogs": "AzureAppService",
    "AZFWThreatIntel": "AzureFirewall",
    "AZFWIdpsSignature": "AzureFirewall",
    "NTANetAnalytics": "AzureNetworkWatcher",
    "DNSQueryLogs": "AzureDNS",
    "SecureScores": "AzureSecurityCenter",
    "SecurityRecommendation": "AzureSecurityCenter",
    "SecurityRegulatoryCompliance": "AzureSecurityCenter",
    # DevOps
    "AzureDevOpsAuditing": "AzureDevOpsAuditing",
    "GitHubAuditData": "GitHubEnterpriseAuditLog",
    # Multi-cloud
    "AWSCloudTrail": "AWS",
    "AWSGuardDuty": "AWS",
    "GCPAuditLogs": "GCPAuditLogs",
    "GoogleCloudSCC": "GoogleCloudSCC",
    # Sentinel self-monitoring
    "SentinelHealth": "MicrosoftSentinelHealth",
    "SentinelAudit": "MicrosoftSentinelAudit",
    "LAQueryLogs": "AzureMonitor",
    "Usage": "AzureMonitor",
    "Watchlist": "MicrosoftSentinelWatchlists",
}

VALID_SENTINEL_TACTICS = {
    "Reconnaissance",
    "ResourceDevelopment",
    "InitialAccess",
    "Execution",
    "Persistence",
    "PrivilegeEscalation",
    "DefenseEvasion",
    "CredentialAccess",
    "Discovery",
    "LateralMovement",
    "Collection",
    "CommandAndControl",
    "Exfiltration",
    "Impact",
}

TACTIC_PHRASES: list[tuple[str, str]] = [
    ("initial access", "InitialAccess"),
    ("execution", "Execution"),
    ("persistence", "Persistence"),
    ("privilege escalation", "PrivilegeEscalation"),
    ("defense evasion", "DefenseEvasion"),
    ("defence evasion", "DefenseEvasion"),
    ("credential access", "CredentialAccess"),
    ("discovery", "Discovery"),
    ("lateral movement", "LateralMovement"),
    ("collection", "Collection"),
    ("command and control", "CommandAndControl"),
    ("exfiltration", "Exfiltration"),
    ("impact", "Impact"),
    ("reconnaissance", "Reconnaissance"),
    ("resource development", "ResourceDevelopment"),
]

# Fallback technique -> tactic mapping when text mentions technique ID without tactic phrase
TECHNIQUE_TO_TACTIC: dict[str, str] = {
    "T1003": "CredentialAccess",
    "T1021": "LateralMovement",
    "T1041": "Exfiltration",
    "T1048": "Exfiltration",
    "T1052": "Exfiltration",
    "T1053": "Persistence",
    "T1059": "Execution",
    "T1068": "PrivilegeEscalation",
    "T1069": "Discovery",
    "T1070": "DefenseEvasion",
    "T1071": "CommandAndControl",
    "T1074": "Collection",
    "T1078": "InitialAccess",
    "T1087": "Discovery",
    "T1098": "Persistence",
    "T1105": "CommandAndControl",
    "T1110": "CredentialAccess",
    "T1114": "Collection",
    "T1134": "PrivilegeEscalation",
    "T1136": "Persistence",
    "T1190": "InitialAccess",
    "T1203": "Execution",
    "T1204": "Execution",
    "T1213": "Collection",
    "T1484": "DefenseEvasion",
    "T1485": "Impact",
    "T1486": "Impact",
    "T1490": "Impact",
    "T1496": "Impact",
    "T1499": "Impact",
    "T1505": "Persistence",
    "T1528": "CredentialAccess",
    "T1530": "Collection",
    "T1537": "Exfiltration",
    "T1539": "CredentialAccess",
    "T1543": "Persistence",
    "T1548": "PrivilegeEscalation",
    "T1550": "LateralMovement",
    "T1552": "CredentialAccess",
    "T1556": "CredentialAccess",
    "T1558": "CredentialAccess",
    "T1562": "DefenseEvasion",
    "T1564": "DefenseEvasion",
    "T1566": "InitialAccess",
    "T1567": "Exfiltration",
    "T1570": "LateralMovement",
    "T1571": "CommandAndControl",
    "T1578": "DefenseEvasion",
    "T1609": "Execution",
    "T1610": "Execution",
    "T1611": "PrivilegeEscalation",
}

NON_TABLES = {
    "CUSTOM", "ASSUMPTION", "MITRE", "NOTE", "HUNT", "ALERT", "TODO",
    "TimeGenerated", "Timestamp", "ActionType", "OperationName", "EventID",
    "ResultType", "Category", "Severity", "Level", "Status", "True", "False",
    "Null", "DeviceId", "AccountName", "UserPrincipalName", "IPAddress",
    "Computer", "ResourceId", "SubscriptionId", "Operation", "Activity",
    "EventData", "AdditionalFields", "Properties", "Parsed", "RawEventData",
    "Table", "TableName",
}

# Column name -> (Sentinel entityType, Sentinel identifier)
# Checked strictly against columns actually returned by the query!
COLUMN_ENTITY_RULES: list[tuple[str, str, str]] = [
    # Accounts (prioritise UPN / FullName / AadUserId / Name)
    ("UserPrincipalName", "Account", "FullName"),
    ("AccountUpn", "Account", "FullName"),
    ("ActorUpn", "Account", "FullName"),
    ("ActorUPN", "Account", "FullName"),
    ("InitiatingProcessAccountUpn", "Account", "FullName"),
    ("MemberUpn", "Account", "FullName"),
    ("UserUpn", "Account", "FullName"),
    ("PrincipalEmail", "Account", "FullName"),
    ("AADEmail", "Account", "FullName"),
    ("MailboxOwnerUPN", "Account", "FullName"),
    ("AccountObjectId", "Account", "AadUserId"),
    ("ActorUserId", "Account", "AadUserId"),
    ("ServicePrincipalId", "Account", "AadUserId"),
    ("Account", "Account", "FullName"),
    ("AccountName", "Account", "Name"),
    ("InitiatingProcessAccountName", "Account", "Name"),
    ("TargetAccount", "Account", "FullName"),
    ("TargetUserName", "Account", "Name"),
    ("SubjectUserName", "Account", "Name"),
    ("AddedAccount", "Account", "Name"),
    ("Actor", "Account", "FullName"),
    ("ActorName", "Account", "FullName"),
    ("AddedBy", "Account", "FullName"),
    ("UserId", "Account", "FullName"),
    ("User", "Account", "FullName"),
    ("Username", "Account", "Name"),
    ("Caller", "Account", "FullName"),
    ("Identity", "Account", "FullName"),
    ("ServicePrincipalName", "Account", "Name"),
    ("server_principal_name_s", "Account", "Name"),
    ("PrincipalName", "Account", "FullName"),
    ("Maker", "Account", "FullName"),
    ("ModifiedBy", "Account", "FullName"),
    ("InitiatedBy", "Account", "FullName"),
    # Mail
    ("RecipientEmailAddress", "Mailbox", "MailboxPrimaryAddress"),
    ("SenderFromAddress", "MailMessage", "Sender"),
    ("NetworkMessageId", "MailMessage", "NetworkMessageId"),
    # Hosts
    ("Computer", "Host", "HostName"),
    ("DeviceName", "Host", "HostName"),
    ("DestinationDeviceName", "Host", "HostName"),
    ("HostName", "Host", "HostName"),
    ("Host", "Host", "HostName"),
    ("LogicalServerName_s", "Host", "HostName"),
    ("Cluster", "Host", "HostName"),
    ("DeviceId", "Host", "AzureID"),
    # IPs
    ("IPAddress", "IP", "Address"),
    ("IpAddress", "IP", "Address"),
    ("ClientIP", "IP", "Address"),
    ("ClientIp", "IP", "Address"),
    ("ClientIPAddress", "IP", "Address"),
    ("ClientIpAddress", "IP", "Address"),
    ("CallerIpAddress", "IP", "Address"),
    ("CallerIPAddress", "IP", "Address"),
    ("CallerIp", "IP", "Address"),
    ("SrcIpAddr", "IP", "Address"),
    ("SourceIP", "IP", "Address"),
    ("SourceIp", "IP", "Address"),
    ("SourceIPAddress", "IP", "Address"),
    ("SourceIpAddress", "IP", "Address"),
    ("SrcIp", "IP", "Address"),
    ("DestIp", "IP", "Address"),
    ("RemoteIP", "IP", "Address"),
    ("cIP", "IP", "Address"),
    ("client_ip_s", "IP", "Address"),
    # URLs & DNS
    ("Url", "URL", "Url"),
    ("RequestUrl", "URL", "Url"),
    ("Site_Url", "URL", "Url"),
    ("DestinationUrl", "URL", "Url"),
    ("UrlDomain", "DNS", "DomainName"),
    ("Domain", "DNS", "DomainName"),
    ("DestinationFqdn", "DNS", "DomainName"),
    ("QueryName", "DNS", "DomainName"),
    # Files & Hashes
    ("FileName", "File", "Name"),
    ("SourceFileName", "File", "Name"),
    ("SHA1", "FileHash", "Value"),
    # Process
    ("ProcessCommandLine", "Process", "CommandLine"),
    ("Cmd", "Process", "CommandLine"),
    ("CommandLine", "Process", "CommandLine"),
    # Azure Resources & Cloud Apps
    ("_ResourceId", "AzureResource", "ResourceId"),
    ("ResourceId", "AzureResource", "ResourceId"),
    ("ResourceName", "AzureResource", "ResourceId"),
    ("Application", "CloudApplication", "Name"),
    ("OfficeWorkload", "CloudApplication", "Name"),
    ("AgentName", "CloudApplication", "Name"),
    ("AppId", "CloudApplication", "AppId"),
]


def det_uuid(key: str) -> str:
    return str(uuid.uuid5(UUID_NS, key))


def slugify(text: str, max_len: int = 64) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    if len(s) <= max_len:
        return s
    cut = s[:max_len]
    if "_" in cut:
        cut = cut.rsplit("_", 1)[0]
    return cut.rstrip("_")


def strip_kql_comments(code: str) -> str:
    return "\n".join(l for l in code.splitlines() if not l.strip().startswith("//"))


def extract_tables(code: str) -> list[str]:
    nc = strip_kql_comments(code)
    found: list[str] = []
    seen: set[str] = set()
    # Start of statement or let assignment or subquery
    for m in re.finditer(r"(?:^|;|let\s+\w+\s*=\s*|\(\s*\n?\s*)([A-Z][A-Za-z0-9_]+)\s*(?=\n\s*\||\s*\|)", nc, re.M):
        t = m.group(1)
        if t not in NON_TABLES and t not in seen:
            seen.add(t)
            found.append(t)
    # Union statements
    for m in re.finditer(r"union\s+(?:withsource=\w+\s+)?(?:isfuzzy=true\s+)?([^\n|]+(?:\n\s*[A-Z][^\n|]*)*)", nc):
        for tok in re.findall(r"\b([A-Z][A-Za-z0-9_]+)\b", m.group(1)):
            if tok not in NON_TABLES and tok not in seen:
                seen.add(tok)
                found.append(tok)
    return found


def build_required_connectors(tables: list[str]) -> list[dict[str, Any]]:
    by_conn: dict[str, list[str]] = {}
    for t in tables:
        cid = TABLE_TO_CONNECTOR.get(t, "AzureMonitor")
        by_conn.setdefault(cid, [])
        if t not in by_conn[cid]:
            by_conn[cid].append(t)
    return [{"connectorId": cid, "dataTypes": dts} for cid, dts in by_conn.items()]


def extract_output_columns(code: str) -> tuple[str, list[str]]:
    nc = strip_kql_comments(code)
    stages: list[str] = []
    depth = 0
    cur: list[str] = []
    in_str: str | None = None
    i = 0
    while i < len(nc):
        ch = nc[i]
        nxt = nc[i + 1] if i + 1 < len(nc) else ""
        if in_str:
            if ch == "\\" and i + 1 < len(nc):
                cur.append(ch)
                cur.append(nxt)
                i += 2
                continue
            cur.append(ch)
            if ch == in_str:
                in_str = None
        else:
            if ch == "@" and nxt in ('"', "'"):
                # Verbatim string literal
                q = nxt
                cur.append(ch)
                cur.append(q)
                i += 2
                while i < len(nc):
                    cur.append(nc[i])
                    if nc[i] == q:
                        if i + 1 < len(nc) and nc[i + 1] == q:
                            cur.append(nc[i + 1])
                            i += 2
                            continue
                        break
                    i += 1
                i += 1
                continue
            if ch in ('"', "'"):
                in_str = ch
                cur.append(ch)
            elif ch == "(":
                depth += 1
                cur.append(ch)
            elif ch == ")":
                depth = max(0, depth - 1)
                cur.append(ch)
            elif ch == "|" and depth == 0:
                stages.append("".join(cur).strip())
                cur = []
            elif ch == ";" and depth == 0:
                stages = []
                cur = []
            else:
                cur.append(ch)
        i += 1
    if cur:
        stages.append("".join(cur).strip())

    # If final top-level stage is a parenthesised union(...) with inner | project, parse last inner project
    if len(stages) == 1 and re.match(r"^union\b", stages[0]):
        inner_projects = re.findall(r"\|\s*project\s+([^\n)]+)", stages[0])
        if inner_projects:
            stages.append("project " + inner_projects[-1].strip())

    for st in reversed(stages):
        if re.match(r"^project\b(?!-away)", st):
            body = re.sub(r"^project\s+", "", st)
            cols: list[str] = []
            d = 0
            tok: list[str] = []
            for ch in body:
                if ch == "(":
                    d += 1
                elif ch == ")":
                    d -= 1
                if ch == "," and d == 0:
                    cols.append("".join(tok).strip())
                    tok = []
                else:
                    tok.append(ch)
            if tok:
                cols.append("".join(tok).strip())
            out = []
            for c in cols:
                name = c.split("=", 1)[0].strip() if "=" in c else c.strip()
                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
                    out.append(name)
            return ("project", out)
        if re.match(r"^summarize\b", st):
            out = []
            m = re.search(r"\bby\b(.*)$", st, re.S)
            if m:
                d = 0
                tok = []
                parts = []
                for ch in m.group(1):
                    if ch == "(":
                        d += 1
                    elif ch == ")":
                        d -= 1
                    if ch == "," and d == 0:
                        parts.append("".join(tok).strip())
                        tok = []
                    else:
                        tok.append(ch)
                if tok:
                    parts.append("".join(tok).strip())
                for part in parts:
                    name = part.split("=", 1)[0].strip() if "=" in part else part.strip()
                    if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
                        out.append(name)
            return ("summarize", out)

    # Raw table output: collect any extended columns plus known referenced columns
    extended = re.findall(r"\|\s*extend\s+([A-Za-z_][A-Za-z0-9_]*)\s*=", nc)
    # Also include columns from the underlying table schema if raw
    tables = extract_tables(code)
    table_defaults: dict[str, list[str]] = {
        "SecurityEvent": ["Computer", "Account", "TargetAccount", "IpAddress"],
        "WindowsEvent": ["Computer"],
        "Event": ["Computer"],
        "OfficeActivity": ["UserId", "ClientIP", "OfficeWorkload"],
        "AZFWThreatIntel": ["SourceIp", "DestinationIp"],
        "AZFWIdpsSignature": ["SourceIp", "DestinationIp"],
        "AzureDiagnostics": ["_ResourceId"],
        "AzureActivity": ["Caller", "CallerIpAddress", "_ResourceId"],
        "AppServiceIPSecAuditLogs": ["CIp", "_ResourceId"],
        "FunctionAppLogs": ["_ResourceId"],
        "AKSAuditAdmin": ["_ResourceId"],
    }
    cols = list(extended)
    for t in tables:
        for c in table_defaults.get(t, []):
            if c not in cols:
                cols.append(c)
    return ("raw", cols)


def build_entity_mappings(code: str, tables: list[str]) -> list[dict[str, Any]]:
    kind, cols = extract_output_columns(code)
    col_set = set(cols)
    nc = strip_kql_comments(code)

    mappings: list[dict[str, Any]] = []
    used_types_cols: set[tuple[str, str]] = set()
    used_entity_types: dict[str, int] = {}

    for col_name, etype, ident in COLUMN_ENTITY_RULES:
        if col_name not in col_set:
            continue
        # Ensure column name actually appears in query (or is a known raw table column)
        if kind != "raw" and not re.search(rf"\b{re.escape(col_name)}\b", nc):
            continue
        if (etype, col_name) in used_types_cols:
            continue
        if used_entity_types.get(etype, 0) >= 2:
            continue
        if len(mappings) >= 5:
            break
        used_types_cols.add((etype, col_name))
        used_entity_types[etype] = used_entity_types.get(etype, 0) + 1
        mappings.append({
            "entityType": etype,
            "fieldMappings": [
                {"identifier": ident, "columnName": col_name}
            ],
        })

    # If a raw query had no column found in nc, guarantee at least one valid column exists
    if not mappings and kind == "raw":
        if "SecurityEvent" in tables:
            mappings.append({"entityType": "Host", "fieldMappings": [{"identifier": "HostName", "columnName": "Computer"}]})
            mappings.append({"entityType": "Account", "fieldMappings": [{"identifier": "FullName", "columnName": "Account"}]})
        elif "OfficeActivity" in tables:
            mappings.append({"entityType": "Account", "fieldMappings": [{"identifier": "FullName", "columnName": "UserId"}]})
        elif "AZFWThreatIntel" in tables or "AZFWIdpsSignature" in tables:
            mappings.append({"entityType": "IP", "fieldMappings": [{"identifier": "Address", "columnName": "SourceIp"}]})
    return mappings


def extract_mitre(text: str, default_tactic: str = "Discovery") -> tuple[list[str], list[str]]:
    techs = sorted(set(re.findall(r"\bT\d{4}(?:\.\d{3})?\b", text)))
    low = text.lower()
    tactics: list[str] = []
    for phrase, tac in TACTIC_PHRASES:
        if phrase in low and tac not in tactics:
            tactics.append(tac)
    for t in techs:
        base = t.split(".")[0]
        tac = TECHNIQUE_TO_TACTIC.get(base)
        if tac and tac not in tactics:
            tactics.append(tac)
    if not tactics:
        tactics = [default_tactic]
    return tactics, techs


def parse_severity(heading: str) -> str:
    m = re.search(r"\((High|Medium|Low|Informational)[^)]*\)", heading, re.I)
    if m:
        raw = m.group(1).capitalize()
        # Handle "Low to Medium" -> Medium, "Medium to High" -> High
        paren = m.group(0).lower()
        if "high" in paren and raw != "High":
            return "High"
        if "medium" in paren and raw == "Low":
            return "Medium"
        return raw
    return "Medium"


def infer_schedule(code: str, ctx: str) -> tuple[str, str]:
    """Return (queryFrequency, queryPeriod) as valid Sentinel YAML durations (max 14d)."""
    nc = strip_kql_comments(code)
    agos = re.findall(r"ago\((\d+)([smhd])\)", nc)
    max_hours = 1.0
    for val, unit in agos:
        v = int(val)
        h = v * {"s": 1 / 3600, "m": 1 / 60, "h": 1, "d": 24}[unit]
        if h > max_hours:
            max_hours = h

    low_ctx = (ctx + "\n" + code).lower()
    if "daily" in low_ctx or max_hours >= 24:
        freq = "1d"
    else:
        freq = "1h"

    if max_hours <= 1:
        period = "1h"
    elif max_hours <= 2:
        period = "2h"
    elif max_hours <= 6:
        period = "6h"
    elif max_hours <= 12:
        period = "12h"
    elif max_hours <= 24:
        period = "1d"
    elif max_hours <= 72:
        period = "3d"
    elif max_hours <= 168:
        period = "7d"
    else:
        # Sentinel API cap for Scheduled rule queryPeriod is 14 days
        period = "14d"

    # Guarantee period >= freq
    dur_hours = {"1h": 1, "2h": 2, "6h": 6, "12h": 12, "1d": 24, "3d": 72, "7d": 168, "14d": 336}
    if dur_hours[period] < dur_hours[freq]:
        period = freq
    return freq, period


def yaml_dur_to_iso(d: str) -> str:
    m = re.match(r"^(\d+)([mhd])$", d)
    if not m:
        return "PT1H"
    val, unit = m.group(1), m.group(2)
    if unit == "m":
        return f"PT{val}M"
    if unit == "h":
        return f"PT{val}H"
    return f"P{val}D"


def yaml_quote(s: str) -> str:
    """Safely single-quote a YAML scalar."""
    return "'" + s.replace("'", "''") + "'"


def dump_block_scalar(text: str, indent: int = 2) -> str:
    pad = " " * indent
    lines = text.rstrip().splitlines()
    return "\n".join(pad + l if l else "" for l in lines)


def render_analytic_rule_yaml(rule: dict[str, Any]) -> str:
    lines = [
        f"id: {rule['id']}",
        f"name: {yaml_quote(rule['name'])}",
        "description: |",
        dump_block_scalar(rule["description"], 2),
        f"severity: {rule['severity']}",
        "status: Available",
        "requiredDataConnectors:",
    ]
    for conn in rule["requiredDataConnectors"]:
        lines.append(f"  - connectorId: {conn['connectorId']}")
        lines.append("    dataTypes:")
        for dt in conn["dataTypes"]:
            lines.append(f"      - {dt}")
    lines.extend([
        f"queryFrequency: {rule['queryFrequency']}",
        f"queryPeriod: {rule['queryPeriod']}",
        f"triggerOperator: {rule['triggerOperator']}",
        f"triggerThreshold: {rule['triggerThreshold']}",
        "tactics:",
    ])
    for t in rule["tactics"]:
        lines.append(f"  - {t}")
    if rule["relevantTechniques"]:
        lines.append("relevantTechniques:")
        for tech in rule["relevantTechniques"]:
            lines.append(f"  - {tech}")
    lines.append("query: |")
    lines.append(dump_block_scalar(rule["query"], 2))
    if rule["entityMappings"]:
        lines.append("entityMappings:")
        for em in rule["entityMappings"]:
            lines.append(f"  - entityType: {em['entityType']}")
            lines.append("    fieldMappings:")
            for fm in em["fieldMappings"]:
                lines.append(f"      - identifier: {fm['identifier']}")
                lines.append(f"        columnName: {fm['columnName']}")
    lines.extend([
        f"version: {rule['version']}",
        "kind: Scheduled",
        "",
    ])
    return "\n".join(lines)


def render_hunting_query_yaml(hq: dict[str, Any]) -> str:
    lines = [
        f"id: {hq['id']}",
        f"name: {yaml_quote(hq['name'])}",
        "description: |",
        dump_block_scalar(hq["description"], 2),
        "requiredDataConnectors:",
    ]
    for conn in hq["requiredDataConnectors"]:
        lines.append(f"  - connectorId: {conn['connectorId']}")
        lines.append("    dataTypes:")
        for dt in conn["dataTypes"]:
            lines.append(f"      - {dt}")
    lines.append("tactics:")
    for t in hq["tactics"]:
        lines.append(f"  - {t}")
    if hq["relevantTechniques"]:
        lines.append("relevantTechniques:")
        for tech in hq["relevantTechniques"]:
            lines.append(f"  - {tech}")
    lines.append("query: |")
    lines.append(dump_block_scalar(hq["query"], 2))
    if hq["entityMappings"]:
        lines.append("entityMappings:")
        for em in hq["entityMappings"]:
            lines.append(f"  - entityType: {em['entityType']}")
            lines.append("    fieldMappings:")
            for fm in em["fieldMappings"]:
                lines.append(f"      - identifier: {fm['identifier']}")
                lines.append(f"        columnName: {fm['columnName']}")
    lines.extend([
        f"version: {hq['version']}",
        "",
    ])
    return "\n".join(lines)


def render_xdr_rule_yaml(rule: dict[str, Any]) -> str:
    lines = [
        f"id: {rule['id']}",
        f"displayName: {yaml_quote(rule['displayName'])}",
        "description: |",
        dump_block_scalar(rule["description"], 2),
        f"severity: {rule['severity']}",
        f"frequency: {rule['frequency']}",
        f"lookbackPeriod: {rule['lookbackPeriod']}",
        f"sourceGuide: {yaml_quote(rule['sourceGuide'])}",
        "requiredTables:",
    ]
    for t in rule["requiredTables"]:
        lines.append(f"  - {t}")
    lines.append("tactics:")
    for t in rule["tactics"]:
        lines.append(f"  - {t}")
    if rule["relevantTechniques"]:
        lines.append("relevantTechniques:")
        for tech in rule["relevantTechniques"]:
            lines.append(f"  - {tech}")
    lines.append("entityMappings:")
    for em in rule["entityMappings"]:
        lines.append(f"  - entityType: {em['entityType']}")
        lines.append(f"    identifier: {em['identifier']}")
        lines.append(f"    columnName: {em['columnName']}")
    lines.append("recommendedActions: |")
    lines.append(dump_block_scalar(rule["recommendedActions"], 2))
    lines.append("query: |")
    lines.append(dump_block_scalar(rule["query"], 2))
    lines.append("")
    return "\n".join(lines)


def clean_title(h3: str) -> str:
    # Strip leading "C1. " and trailing "(High)" / "(Medium, High in production)"
    t = re.sub(r"^C\d+\.\s*", "", h3).strip()
    t = re.sub(r"\s*\((?:High|Medium|Low|Informational)[^)]*\)\s*$", "", t, flags=re.I).strip()
    t = t.replace("`", "")
    return t


def clean_prose(text: str) -> str:
    # Strip markdown links [label](url) -> label, remove backticks, trim
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    s = s.replace("`", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_guide_kql() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    detections: list[dict[str, Any]] = []
    hunts: list[dict[str, Any]] = []

    skip_top = {".git", ".github", "node_modules", "_site", "site-src", "docs", "queries", "scripts", "solution", "defender-xdr"}

    for p in sorted(ROOT.rglob("README.md")):
        rel = p.relative_to(ROOT)
        if len(rel.parts) < 3 or rel.parts[0] in skip_top:
            continue
        lines = p.read_text(encoding="utf-8").splitlines()
        product = next((l[2:].strip() for l in lines if l.startswith("# ")), rel.parts[1])
        group = rel.parts[0]
        slug = rel.parts[1]
        h2 = ""
        h3 = ""
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("## "):
                h2 = line[3:].strip()
                h3 = ""
            elif line.startswith("### "):
                h3 = line[4:].strip()
            elif re.match(r"^```(kql|kusto)", line.strip(), re.I):
                start = i
                i += 1
                buf = []
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    buf.append(lines[i])
                    i += 1
                code = "\n".join(buf).strip()
                pre_lines = []
                j = start - 1
                while j >= 0 and not lines[j].startswith("#") and not lines[j].startswith("```"):
                    pre_lines.insert(0, lines[j])
                    j -= 1
                post_lines = []
                j = i + 1
                while j < len(lines) and not lines[j].startswith("#") and not lines[j].startswith("```"):
                    post_lines.append(lines[j])
                    j += 1
                entry = {
                    "file": rel.as_posix(),
                    "group": group,
                    "product_slug": slug,
                    "product": product,
                    "h2": h2,
                    "h3": h3,
                    "pre": "\n".join(pre_lines).strip(),
                    "post": "\n".join(post_lines).strip(),
                    "code": code,
                }
                if re.match(r"^C\d+\.", h3) or "// CUSTOM" in code:
                    detections.append(entry)
                elif "hunt" in h2.lower() or "// Hunt:" in code or "// HUNT" in code:
                    hunts.append(entry)
            i += 1
    return detections, hunts


def build_sentinel_analytic_rules(raw_detections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rules: list[dict[str, Any]] = []
    for d in raw_detections:
        tables = extract_tables(d["code"])
        # Skip rules that depend on XDR-only tables unavailable in Sentinel Log Analytics
        if any(t in XDR_ONLY_TABLES for t in tables):
            continue

        code = d["code"]
        # Convert DeviceFileEvents C3 (authored with Timestamp in guide) to Sentinel TimeGenerated
        if "DeviceFileEvents" in tables and re.search(r"\bTimestamp\b", code):
            code = re.sub(r"\bTimestamp\b", "TimeGenerated", code)

        code_id = re.match(r"^(C\d+)\.", d["h3"])
        cid_tag = code_id.group(1) if code_id else "C0"
        title = clean_title(d["h3"])
        short_product = d["product"].replace("Microsoft ", "").strip()
        # Keep displayName crisp and within Sentinel limits
        name = f"{short_product} - {title}"
        if len(name) > 128:
            name = name[:125].rstrip() + "..."

        desc_parts = []
        if d["pre"] and not d["pre"].startswith("|"):
            desc_parts.append(clean_prose(d["pre"]))
        if d["post"]:
            desc_parts.append(clean_prose(d["post"]))
        if not desc_parts:
            desc_parts.append(f"Custom detection for {d['product']}: {title}.")
        desc_parts.append(f"Source guide: {d['file']} ({cid_tag}).")
        description = " ".join(desc_parts)

        severity = parse_severity(d["h3"])
        tactics, techs = extract_mitre(d["post"] + "\n" + d["pre"] + "\n" + d["h3"] + "\n" + code)
        freq, period = infer_schedule(code, d["pre"] + "\n" + d["post"])
        connectors = build_required_connectors(tables)
        entity_mappings = build_entity_mappings(code, tables)

        # Ensure every rule has at least one valid entity mapping when possible
        filename = f"{slugify(d['product_slug'], 32)}_{cid_tag}_{slugify(title, 44)}.yaml"
        rules.append({
            "filename": filename,
            "id": det_uuid(f"analytic-rule:{d['file']}:{cid_tag}"),
            "name": name,
            "description": description,
            "severity": severity,
            "requiredDataConnectors": connectors,
            "queryFrequency": freq,
            "queryPeriod": period,
            "triggerOperator": "gt",
            "triggerThreshold": 0,
            "tactics": tactics,
            "relevantTechniques": techs,
            "query": code,
            "entityMappings": entity_mappings,
            "version": "1.0.0",
            "group": d["group"],
            "product": d["product"],
            "sourceGuide": d["file"],
            "tables": tables,
        })

    # Add 3 operational Sentinel health and integrity rules from docs/sentinel-health.md
    operational_rules = [
        {
            "filename": "sentinel_health_connector_fetch_failure.yaml",
            "id": det_uuid("analytic-rule:docs/sentinel-health.md:connector-failure"),
            "name": "Sentinel Health - Data connector fetch failure",
            "description": (
                "Detects supported Microsoft Sentinel data connectors reporting a Data fetch status change "
                "failure in SentinelHealth. Source guide: docs/sentinel-health.md."
            ),
            "severity": "High",
            "requiredDataConnectors": [{"connectorId": "MicrosoftSentinelHealth", "dataTypes": ["SentinelHealth"]}],
            "queryFrequency": "1h",
            "queryPeriod": "1h",
            "triggerOperator": "gt",
            "triggerThreshold": 0,
            "tactics": ["DefenseEvasion"],
            "relevantTechniques": ["T1562.008"],
            "query": (
                "// Operational alert: a supported data connector stopped fetching successfully\n"
                "SentinelHealth\n"
                "| where TimeGenerated > ago(1h)\n"
                "| where OperationName == 'Data fetch status change'\n"
                "| where Status == 'Failure'\n"
                "| project TimeGenerated, Connector = SentinelResourceName, ResourceId = SentinelResourceId,\n"
                "          Status, Reason, ExtendedProperties"
            ),
            "entityMappings": [
                {"entityType": "AzureResource", "fieldMappings": [{"identifier": "ResourceId", "columnName": "ResourceId"}]}
            ],
            "version": "1.0.0",
            "group": "operations",
            "product": "Microsoft Sentinel Health",
            "sourceGuide": "docs/sentinel-health.md",
            "tables": ["SentinelHealth"],
        },
        {
            "filename": "sentinel_health_critical_table_stale.yaml",
            "id": det_uuid("analytic-rule:docs/sentinel-health.md:stale-table"),
            "name": "Sentinel Health - Critical security log table stale or empty",
            "description": (
                "Detects core security log tables that have gone silent beyond their expected freshness budget. "
                "Trim the expected datatable to match your active connectors before enabling. "
                "Source guide: docs/sentinel-health.md."
            ),
            "severity": "High",
            "requiredDataConnectors": [
                {"connectorId": "AzureActiveDirectory", "dataTypes": ["SigninLogs", "AuditLogs"]},
                {"connectorId": "AzureActivity", "dataTypes": ["AzureActivity"]},
                {"connectorId": "Office365", "dataTypes": ["OfficeActivity"]},
                {"connectorId": "SecurityEvents", "dataTypes": ["SecurityEvent"]},
                {"connectorId": "CefAma", "dataTypes": ["CommonSecurityLog"]},
            ],
            "queryFrequency": "1h",
            "queryPeriod": "14d",
            "triggerOperator": "gt",
            "triggerThreshold": 0,
            "tactics": ["DefenseEvasion"],
            "relevantTechniques": ["T1562.008"],
            "query": (
                "// Operational alert: critical tables are stale or empty\n"
                "// ASSUMPTION: trim the table list and staleness budget to match your environment.\n"
                "let expected = datatable(Table: string, MaxStaleMinutes: long)\n"
                "    [\"SigninLogs\", 120,\n"
                "     \"AuditLogs\", 120,\n"
                "     \"AzureActivity\", 120,\n"
                "     \"OfficeActivity\", 720,\n"
                "     \"SecurityEvent\", 120,\n"
                "     \"CommonSecurityLog\", 120];\n"
                "let seen = union withsource=TableName isfuzzy=true\n"
                "        SigninLogs, AuditLogs, AzureActivity, OfficeActivity, SecurityEvent, CommonSecurityLog\n"
                "    | where TimeGenerated > ago(14d)\n"
                "    | summarize Latest = max(TimeGenerated) by TableName;\n"
                "expected\n"
                "| join kind=leftouter seen on $left.Table == $right.TableName\n"
                "| extend StaleMinutes = round((now() - coalesce(Latest, ago(14d))) / 1m)\n"
                "| where StaleMinutes > MaxStaleMinutes\n"
                "| project Table, Latest, StaleMinutes, MaxStaleMinutes"
            ),
            "entityMappings": [
                {"entityType": "CloudApplication", "fieldMappings": [{"identifier": "Name", "columnName": "Table"}]}
            ],
            "version": "1.0.0",
            "group": "operations",
            "product": "Microsoft Sentinel Health",
            "sourceGuide": "docs/sentinel-health.md",
            "tables": ["SigninLogs", "AuditLogs", "AzureActivity", "OfficeActivity", "SecurityEvent", "CommonSecurityLog"],
        },
        {
            "filename": "sentinel_audit_analytic_rule_tampering.yaml",
            "id": det_uuid("analytic-rule:docs/sentinel-health.md:rule-tampering"),
            "name": "Sentinel Audit - Analytics rule disabled, deleted or modified",
            "description": (
                "Detects analytics rule delete, disable or update operations recorded in SentinelAudit. "
                "Attackers with workspace access weaken or disable detections to blind the SOC. "
                "Source guide: docs/sentinel-health.md."
            ),
            "severity": "High",
            "requiredDataConnectors": [{"connectorId": "MicrosoftSentinelAudit", "dataTypes": ["SentinelAudit"]}],
            "queryFrequency": "1h",
            "queryPeriod": "1h",
            "triggerOperator": "gt",
            "triggerThreshold": 0,
            "tactics": ["DefenseEvasion"],
            "relevantTechniques": ["T1562.001"],
            "query": (
                "// Operational alert: analytics rules disabled, deleted or modified\n"
                "SentinelAudit\n"
                "| where TimeGenerated > ago(1h)\n"
                "| where SentinelResourceType == 'AlertRule'\n"
                "| where OperationName has_any ('Delete', 'Disable', 'Update')\n"
                "| project TimeGenerated, Rule = SentinelResourceName, ResourceId = SentinelResourceId,\n"
                "          OperationName, Description, ExtendedProperties"
            ),
            "entityMappings": [
                {"entityType": "AzureResource", "fieldMappings": [{"identifier": "ResourceId", "columnName": "ResourceId"}]}
            ],
            "version": "1.0.0",
            "group": "operations",
            "product": "Microsoft Sentinel Health",
            "sourceGuide": "docs/sentinel-health.md",
            "tables": ["SentinelAudit"],
        },
    ]
    rules.extend(operational_rules)
    return rules


def build_sentinel_hunting_queries(raw_hunts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    queries: list[dict[str, Any]] = []
    per_product_idx: dict[str, int] = {}

    for h in raw_hunts:
        tables = extract_tables(h["code"])
        if any(t in XDR_ONLY_TABLES for t in tables):
            continue

        slug = h["product_slug"]
        per_product_idx[slug] = per_product_idx.get(slug, 0) + 1
        idx = per_product_idx[slug]

        # Derive crisp title from comment or preceding bullet bold heading
        title = ""
        first_comment = next((l.strip()[2:].strip() for l in h["code"].splitlines() if l.strip().startswith("//") and not l.strip().startswith("// ASSUMPTION")), "")
        if first_comment:
            title = re.sub(r"^(?:HUNT|Hunt)\s*[-:]\s*", "", first_comment).strip()
        if not title and h["pre"]:
            m = re.search(r"\*\*([^*]+)\*\*", h["pre"].splitlines()[-1])
            if m:
                title = m.group(1).strip().rstrip(".")
        if not title:
            title = f"{h['product']} hunting query {idx}"
        title = title.replace("`", "")
        short_product = h["product"].replace("Microsoft ", "").strip()
        name = f"{short_product} - {title}"
        if len(name) > 128:
            name = name[:125].rstrip() + "..."

        desc = clean_prose(h["pre"].splitlines()[-1]) if h["pre"] else title
        desc = f"{desc} Source guide: {h['file']}."
        tactics, techs = extract_mitre(h["pre"] + "\n" + h["post"] + "\n" + h["code"], default_tactic="Discovery")
        connectors = build_required_connectors(tables)
        entity_mappings = build_entity_mappings(h["code"], tables)

        filename = f"{slugify(slug, 32)}_H{idx}_{slugify(title, 40)}.yaml"
        queries.append({
            "filename": filename,
            "id": det_uuid(f"hunting-query:{h['file']}:H{idx}"),
            "name": name,
            "description": desc,
            "requiredDataConnectors": connectors,
            "tactics": tactics,
            "relevantTechniques": techs,
            "query": h["code"],
            "entityMappings": entity_mappings,
            "version": "1.0.0",
            "group": h["group"],
            "product": h["product"],
            "sourceGuide": h["file"],
            "tables": tables,
        })

    # Add 5 operational hunting queries from docs/sentinel-health.md, docs/watchlists.md, queries/cost/
    cost_anomaly_kql = (ROOT / "queries/cost/04-daily-trend-and-anomalies.kql").read_text(encoding="utf-8").strip()
    operational_hunts = [
        {
            "filename": "sentinel_health_H1_connector_health_summary.yaml",
            "id": det_uuid("hunting-query:docs/sentinel-health.md:connector-summary"),
            "name": "Sentinel Health - Data connector health summary over 7 days",
            "description": "Summarises data connector polling volume and failure counts over the last 7 days in SentinelHealth. Source guide: docs/sentinel-health.md.",
            "requiredDataConnectors": [{"connectorId": "MicrosoftSentinelHealth", "dataTypes": ["SentinelHealth"]}],
            "tactics": ["DefenseEvasion"],
            "relevantTechniques": ["T1562.008"],
            "query": (
                "// Connector health at a glance over a week\n"
                "SentinelHealth\n"
                "| where TimeGenerated > ago(7d)\n"
                "| where SentinelResourceType == 'DataConnector'\n"
                "| summarize Events = count(),\n"
                "            Failures = countif(Status == 'Failure'),\n"
                "            Latest = arg_max(TimeGenerated, Status)\n"
                "    by Connector = SentinelResourceName\n"
                "| order by Failures desc"
            ),
            "entityMappings": [
                {"entityType": "CloudApplication", "fieldMappings": [{"identifier": "Name", "columnName": "Connector"}]}
            ],
            "version": "1.0.0",
            "group": "operations",
            "product": "Microsoft Sentinel Health",
            "sourceGuide": "docs/sentinel-health.md",
            "tables": ["SentinelHealth"],
        },
        {
            "filename": "sentinel_audit_H2_sensitive_table_query_audit.yaml",
            "id": det_uuid("hunting-query:docs/sentinel-health.md:laquerylogs-sensitive"),
            "name": "Sentinel Audit - Users querying sensitive security tables",
            "description": "Hunts LAQueryLogs for users querying high-sensitivity security tables such as SigninLogs, SecurityEvent and SentinelAudit. Source guide: docs/sentinel-health.md.",
            "requiredDataConnectors": [{"connectorId": "AzureMonitor", "dataTypes": ["LAQueryLogs"]}],
            "tactics": ["Discovery", "Collection"],
            "relevantTechniques": ["T1087"],
            "query": (
                "// Who queried the most sensitive tables this week\n"
                "LAQueryLogs\n"
                "| where TimeGenerated > ago(7d)\n"
                "| where QueryText has_any ('SigninLogs', 'SecurityEvent', 'SentinelAudit')\n"
                "| summarize Queries = count(), LastRun = max(TimeGenerated) by AADEmail, RequestClientApp\n"
                "| order by Queries desc"
            ),
            "entityMappings": [
                {"entityType": "Account", "fieldMappings": [{"identifier": "FullName", "columnName": "AADEmail"}]}
            ],
            "version": "1.0.0",
            "group": "operations",
            "product": "Microsoft Sentinel Health",
            "sourceGuide": "docs/sentinel-health.md",
            "tables": ["LAQueryLogs"],
        },
        {
            "filename": "sentinel_audit_H3_failed_or_slow_queries.yaml",
            "id": det_uuid("hunting-query:docs/sentinel-health.md:laquerylogs-slow"),
            "name": "Sentinel Audit - Failed or extremely slow workspace queries",
            "description": "Finds failed queries (ResponseCode != 200) or queries taking over 5 minutes in LAQueryLogs. Source guide: docs/sentinel-health.md.",
            "requiredDataConnectors": [{"connectorId": "AzureMonitor", "dataTypes": ["LAQueryLogs"]}],
            "tactics": ["Impact"],
            "relevantTechniques": ["T1499"],
            "query": (
                "// Failed or extremely slow queries\n"
                "LAQueryLogs\n"
                "| where TimeGenerated > ago(7d)\n"
                "| where ResponseCode != 200 or ResponseDurationMs > 300000\n"
                "| project TimeGenerated, AADEmail, ResponseCode, ResponseDurationMs, RequestClientApp, QueryText"
            ),
            "entityMappings": [
                {"entityType": "Account", "fieldMappings": [{"identifier": "FullName", "columnName": "AADEmail"}]}
            ],
            "version": "1.0.0",
            "group": "operations",
            "product": "Microsoft Sentinel Health",
            "sourceGuide": "docs/sentinel-health.md",
            "tables": ["LAQueryLogs"],
        },
        {
            "filename": "sentinel_watchlists_H4_stale_watchlists.yaml",
            "id": det_uuid("hunting-query:docs/watchlists.md:stale-watchlists"),
            "name": "Sentinel Watchlists - Stale watchlists not updated in 30 days",
            "description": "Identifies Microsoft Sentinel watchlists that have not been updated in over 30 days so detections relying on enrichment stay accurate. Source guide: docs/watchlists.md.",
            "requiredDataConnectors": [{"connectorId": "MicrosoftSentinelWatchlists", "dataTypes": ["Watchlist"]}],
            "tactics": ["DefenseEvasion"],
            "relevantTechniques": ["T1562"],
            "query": (
                "// Which watchlists have not been touched in 30 days?\n"
                "// ASSUMPTION: lists expected to change more often, like leavers, deserve a shorter window.\n"
                "Watchlist\n"
                "| where TimeGenerated > ago(60d)\n"
                "| summarize Items = count(), LastUpdate = max(LastUpdatedTimeUTC) by WatchlistAlias\n"
                "| where LastUpdate < ago(30d)"
            ),
            "entityMappings": [
                {"entityType": "CloudApplication", "fieldMappings": [{"identifier": "Name", "columnName": "WatchlistAlias"}]}
            ],
            "version": "1.0.0",
            "group": "operations",
            "product": "Microsoft Sentinel Watchlists",
            "sourceGuide": "docs/watchlists.md",
            "tables": ["Watchlist"],
        },
        {
            "filename": "sentinel_cost_H5_daily_ingestion_anomalies.yaml",
            "id": det_uuid("hunting-query:queries/cost/04-daily-trend-and-anomalies.kql"),
            "name": "Sentinel Cost - Daily billable GB ingestion trend and spike anomalies",
            "description": "Detects sudden daily billable ingestion spikes over 30 days using series_decompose_anomalies on Usage. Source guide: queries/cost/04-daily-trend-and-anomalies.kql.",
            "requiredDataConnectors": [{"connectorId": "AzureMonitor", "dataTypes": ["Usage"]}],
            "tactics": ["Impact"],
            "relevantTechniques": ["T1496"],
            "query": cost_anomaly_kql,
            "entityMappings": [],
            "version": "1.0.0",
            "group": "operations",
            "product": "Microsoft Sentinel Cost",
            "sourceGuide": "queries/cost/04-daily-trend-and-anomalies.kql",
            "tables": ["Usage"],
        },
    ]
    queries.extend(operational_hunts)
    return queries


def make_workbook_text_item(name: str, md: str) -> dict[str, Any]:
    return {
        "type": 1,
        "content": {"json": md},
        "name": name,
    }


def make_workbook_kql_item(
    name: str,
    title: str,
    query: str,
    visualization: str = "table",
    size: int = 0,
    query_type: int = 0,
) -> dict[str, Any]:
    return {
        "type": 3,
        "content": {
            "version": "KqlItem/1.0",
            "query": query.strip(),
            "size": size,
            "title": title,
            "queryType": query_type,
            "resourceType": "microsoft.operationalinsights/workspaces",
            "visualization": visualization,
        },
        "name": name,
    }


def build_workbooks() -> list[dict[str, Any]]:
    # Workbook 1: Ingestion Health & Table Freshness (from queries/validation/ + docs/sentinel-health.md)
    health_all = (ROOT / "queries/validation/health-all-tables.kql").read_text(encoding="utf-8").strip()
    val_identity = (ROOT / "queries/validation/identity.kql").read_text(encoding="utf-8").strip()
    val_endpoint = (ROOT / "queries/validation/endpoint.kql").read_text(encoding="utf-8").strip()
    val_email = (ROOT / "queries/validation/email-collab.kql").read_text(encoding="utf-8").strip()
    val_azure = (ROOT / "queries/validation/azure.kql").read_text(encoding="utf-8").strip()
    val_servers = (ROOT / "queries/validation/servers.kql").read_text(encoding="utf-8").strip()

    connector_health_kql = (
        "SentinelHealth\n"
        "| where TimeGenerated > ago(7d)\n"
        "| where SentinelResourceType == 'DataConnector'\n"
        "| summarize Events = count(), Failures = countif(Status == 'Failure'), Latest = arg_max(TimeGenerated, Status)\n"
        "    by Connector = SentinelResourceName\n"
        "| order by Failures desc"
    )
    rule_audit_kql = (
        "SentinelAudit\n"
        "| where TimeGenerated > ago(14d)\n"
        "| where SentinelResourceType == 'AlertRule'\n"
        "| where OperationName has_any ('Delete', 'Disable', 'Update')\n"
        "| project TimeGenerated, Rule = SentinelResourceName, OperationName, Description\n"
        "| order by TimeGenerated desc"
    )
    watchlist_kql = (
        "Watchlist\n"
        "| where TimeGenerated > ago(60d)\n"
        "| summarize Items = count(), LastUpdate = max(LastUpdatedTimeUTC) by WatchlistAlias\n"
        "| extend DaysSinceUpdate = round((now() - LastUpdate) / 1d, 1)\n"
        "| order by DaysSinceUpdate desc"
    )

    wb1_json = {
        "version": "Notebook/1.0",
        "items": [
            make_workbook_text_item(
                "header-health",
                (
                    "## Microsoft Security Logging Guide: Ingestion Health and Table Freshness\n\n"
                    "Monitors whether documented Microsoft Sentinel Analytics tables are landing, "
                    "tracks connector health in `SentinelHealth`, audits rule changes in `SentinelAudit`, "
                    "and surfaces stale watchlists. Built from `queries/validation/` and `docs/sentinel-health.md`."
                ),
            ),
            make_workbook_kql_item("master-table-freshness", "All documented Sentinel tables: freshness and 7-day volume", health_all, "table", 2),
            make_workbook_kql_item("connector-health-7d", "SentinelHealth: data connector status and failures (7 days)", connector_health_kql, "table", 1),
            make_workbook_kql_item("rule-audit-14d", "SentinelAudit: analytics rule changes (14 days)", rule_audit_kql, "table", 1),
            make_workbook_kql_item("watchlist-freshness", "Watchlist staleness check (60 days)", watchlist_kql, "table", 1),
            make_workbook_kql_item("group-identity", "Group check: Identity tables", val_identity, "table", 1),
            make_workbook_kql_item("group-endpoint", "Group check: Endpoint tables", val_endpoint, "table", 1),
            make_workbook_kql_item("group-email", "Group check: Email and collaboration tables", val_email, "table", 1),
            make_workbook_kql_item("group-azure", "Group check: Azure workloads and networking tables", val_azure, "table", 1),
            make_workbook_kql_item("group-servers", "Group check: Server tables", val_servers, "table", 1),
        ],
        "isLocked": False,
        "fallbackResourceIds": ["Azure Monitor"],
        "fromTemplateId": "sentinel-MicrosoftSecurityLoggingGuide-IngestionHealth",
    }

    # Workbook 2: Cost Estimation & Volume Monitoring (from queries/cost/01..06.kql)
    c01 = (ROOT / "queries/cost/01-gb-per-table.kql").read_text(encoding="utf-8").strip()
    c02 = (ROOT / "queries/cost/02-gb-per-solution.kql").read_text(encoding="utf-8").strip()
    c03 = (ROOT / "queries/cost/03-gb-per-dcr.kql").read_text(encoding="utf-8").strip()
    c04 = (ROOT / "queries/cost/04-daily-trend-and-anomalies.kql").read_text(encoding="utf-8").strip()
    c05_raw = (ROOT / "queries/cost/05-top-noisy-events-and-hosts.kql").read_text(encoding="utf-8").strip()
    # Split query 05 into its 3 standalone KQL queries (5a, 5b, 5c) so each workbook tile runs cleanly
    c05_parts = [p.strip() for p in c05_raw.split(";") if p.strip()]
    c06 = (ROOT / "queries/cost/06-commitment-tier-sizing.kql").read_text(encoding="utf-8").strip()

    wb2_items = [
        make_workbook_text_item(
            "header-cost",
            (
                "## Microsoft Security Logging Guide: Cost Estimation and Volume Monitoring\n\n"
                "Measures billable versus free GB per table and solution, detects daily ingestion spikes, "
                "identifies top noisy event IDs and hosts for DCR filtering, and calculates daily GB percentiles "
                "for commitment tier sizing. Built from `queries/cost/` and `docs/cost-estimation.md`."
            ),
        ),
        make_workbook_kql_item("cost-commitment-sizing", "Commitment tier sizing (30-day daily billable GB percentiles)", c06, "table", 1),
        make_workbook_kql_item("cost-daily-anomalies", "Daily billable GB trend and anomaly flags (30 days)", c04, "table", 1),
        make_workbook_kql_item("cost-gb-per-table", "Billable vs free GB per table (30 days)", c01, "table", 2),
        make_workbook_kql_item("cost-gb-per-solution", "Billable GB by Sentinel solution and table (30 days)", c02, "table", 1),
        make_workbook_kql_item("cost-gb-per-resource", "Estimated billable GB by Azure resource and source (7 days)", c03, "table", 2),
    ]
    c05_titles = [
        "Top noisy Windows SecurityEvent IDs (7 days)",
        "Top noisy accounts in SecurityEvent (7 days)",
        "Top noisy AzureDiagnostics categories and resources (7 days)",
    ]
    for idx, part in enumerate(c05_parts):
        title = c05_titles[idx] if idx < len(c05_titles) else f"Noisy source breakdown {idx + 1}"
        wb2_items.append(make_workbook_kql_item(f"cost-noisy-{idx + 1}", title, part, "table", 1))

    wb2_json = {
        "version": "Notebook/1.0",
        "items": wb2_items,
        "isLocked": False,
        "fallbackResourceIds": ["Azure Monitor"],
        "fromTemplateId": "sentinel-MicrosoftSecurityLoggingGuide-CostMonitoring",
    }

    return [
        {
            "filename": "IngestionHealthAndTableFreshness.json",
            "contentId": "MSLG_IngestionHealthAndTableFreshness",
            "displayName": "Microsoft Security Logging Guide - Ingestion Health and Table Freshness",
            "description": "Monitors table freshness, 7-day volume, SentinelHealth connector drift, SentinelAudit rule changes and watchlist staleness across all documented product groups.",
            "paramName": "workbook1-name",
            "version": "1.0.0",
            "json": wb1_json,
        },
        {
            "filename": "CostEstimationAndVolumeMonitoring.json",
            "contentId": "MSLG_CostEstimationAndVolumeMonitoring",
            "displayName": "Microsoft Security Logging Guide - Cost Estimation and Volume Monitoring",
            "description": "Measures billable vs free GB per table and solution, detects daily ingestion anomalies, pinpoints noisy sources for DCR filtering and sizes Sentinel commitment tiers.",
            "paramName": "workbook2-name",
            "version": "1.0.0",
            "json": wb2_json,
        },
    ]


def build_xdr_custom_detections(raw_detections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build Defender XDR custom detection rule definitions for all 15 detections on XDR tables.

    Every rule uses Timestamp (not TimeGenerated) and projects Timestamp + ReportId
    (plus DeviceId for Defender for Endpoint Device* tables), matching Microsoft Defender XDR
    custom detection schema requirements.
    """
    # Hand-crafted exact Defender XDR KQL and entity mappings for the 15 XDR-table detections
    # so every rule satisfies Defender XDR's strict required columns (Timestamp, ReportId, DeviceId)
    # without breaking query semantics.
    xdr_specs: dict[tuple[str, str], dict[str, Any]] = {
        ("endpoint/defender-for-endpoint/README.md", "C1"): {
            "frequency": "PT1H",
            "lookbackPeriod": "PT2H",
            "entityMappings": [
                {"entityType": "Device", "identifier": "DeviceId", "columnName": "DeviceId"},
            ],
            "recommendedActions": "Isolate the endpoint if the spawned script or destination IP is unauthorised, inspect the Office document source and review recent network connections.",
            "query": (
                "// Defender XDR custom detection: Office app spawned a script interpreter, then the device called out\n"
                "let office_apps = dynamic([\"winword.exe\", \"excel.exe\", \"powerpnt.exe\", \"outlook.exe\", \"msaccess.exe\"]);\n"
                "let interpreters = dynamic([\"powershell.exe\", \"cmd.exe\", \"wscript.exe\", \"cscript.exe\", \"mshta.exe\"]);\n"
                "let spawns = DeviceProcessEvents\n"
                "| where Timestamp > ago(2h)\n"
                "| where InitiatingProcessFileName in~ (office_apps)\n"
                "| where FileName in~ (interpreters)\n"
                "| project DeviceId, FirstSeen = Timestamp, Parent = InitiatingProcessFileName,\n"
                "          Interpreter = FileName, Cmd = ProcessCommandLine;\n"
                "DeviceNetworkEvents\n"
                "| where Timestamp > ago(1h)\n"
                "| where RemoteIPType == \"Public\"\n"
                "| join kind=inner spawns on DeviceId\n"
                "| where Timestamp > FirstSeen\n"
                "| summarize Timestamp = max(Timestamp), ReportId = any(ReportId),\n"
                "            Connections = count(), DestIPs = make_set(RemoteIP, 5), Ports = make_set(RemotePort, 5)\n"
                "    by DeviceId, DeviceName, Parent, Interpreter, Cmd"
            ),
        },
        ("endpoint/defender-for-endpoint/README.md", "C2"): {
            "frequency": "PT1H",
            "lookbackPeriod": "PT1H",
            "entityMappings": [
                {"entityType": "Device", "identifier": "DeviceId", "columnName": "DeviceId"},
                {"entityType": "File", "identifier": "SHA1", "columnName": "SHA1"},
            ],
            "recommendedActions": "Quarantine the matched file, add the hash to Defender XDR custom indicators if confirmed malicious, and inspect parent process lineage.",
            "query": (
                "// Defender XDR custom detection: process SHA1 matches an organisation threat-intel hash list\n"
                "// Replace the placeholder SHA1 list with your external feed or Defender XDR custom indicators.\n"
                "let blocked_hashes = dynamic([\"0000000000000000000000000000000000000000\"]);\n"
                "DeviceProcessEvents\n"
                "| where Timestamp > ago(1h)\n"
                "| where tolower(SHA1) in (blocked_hashes)\n"
                "| project Timestamp, ReportId, DeviceId, DeviceName, AccountName, FileName,\n"
                "          FolderPath, ProcessCommandLine, InitiatingProcessFileName, SHA1"
            ),
        },
        ("endpoint/defender-for-endpoint/README.md", "C3"): {
            "frequency": "P1D",
            "lookbackPeriod": "P1D",
            "entityMappings": [
                {"entityType": "Device", "identifier": "DeviceId", "columnName": "DeviceId"},
            ],
            "recommendedActions": "Inspect the initiating process binary and destination IP reputation; exclude benign telemetry or monitoring agents after baselining.",
            "query": (
                "// Defender XDR custom detection: steady low-rate outbound connections typical of C2 beaconing\n"
                "// ASSUMPTION: thresholds are a starting point. Tune against a week of your own traffic.\n"
                "DeviceNetworkEvents\n"
                "| where Timestamp > ago(24h)\n"
                "| where RemoteIPType == \"Public\"\n"
                "| summarize Attempts = count(), LatestTs = max(Timestamp), SampleReportId = any(ReportId)\n"
                "    by DeviceId, DeviceName, InitiatingProcessFileName, RemoteIP, bin(Timestamp, 10m)\n"
                "| summarize QuietBins = countif(Attempts between (1 .. 5)), Total = sum(Attempts),\n"
                "            Timestamp = max(LatestTs), ReportId = any(SampleReportId)\n"
                "    by DeviceId, DeviceName, InitiatingProcessFileName, RemoteIP\n"
                "| where QuietBins >= 20\n"
                "| project Timestamp, ReportId, DeviceId, DeviceName, InitiatingProcessFileName, RemoteIP, Total, QuietBins"
            ),
        },
        ("email-collab/defender-for-office-365/README.md", "C1"): {
            "frequency": "PT1H",
            "lookbackPeriod": "PT1H",
            "entityMappings": [
                {"entityType": "Mailbox", "identifier": "RecipientEmailAddress", "columnName": "RecipientEmailAddress"},
                {"entityType": "MailMessage", "identifier": "NetworkMessageId", "columnName": "NetworkMessageId"},
            ],
            "recommendedActions": "Check whether the malicious message remains in the recipient mailbox, hard-delete it manually via Threat Explorer, and check for clicks or replies.",
            "query": (
                "// Defender XDR custom detection: ZAP or manual post-delivery remediation failed on delivered mail\n"
                "// ASSUMPTION: pin ActionResult values against your tenant first via distinct ActionType, ActionResult.\n"
                "EmailPostDeliveryEvents\n"
                "| where Timestamp > ago(1h)\n"
                "| where ActionType in (\"Phish ZAP\", \"Malware ZAP\", \"Manual remediation\")\n"
                "| where tostring(ActionResult) !~ \"Success\"\n"
                "| project Timestamp, ReportId, NetworkMessageId, RecipientEmailAddress, SenderFromAddress,\n"
                "          ActionType, ActionTrigger, ActionResult, DeliveryLocation, ThreatTypes"
            ),
        },
        ("email-collab/defender-for-office-365/README.md", "C2"): {
            "frequency": "PT1H",
            "lookbackPeriod": "PT1H",
            "entityMappings": [
                {"entityType": "User", "identifier": "AccountUpn", "columnName": "AccountUpn"},
                {"entityType": "MailMessage", "identifier": "NetworkMessageId", "columnName": "NetworkMessageId"},
            ],
            "recommendedActions": "Treat the account as potentially compromised: inspect sign-ins and endpoint activity after the click, and revoke sessions if credentials were entered.",
            "query": (
                "// Defender XDR custom detection: click allowed or user continued past a phishing Safe Links warning\n"
                "UrlClickEvents\n"
                "| where Timestamp > ago(1h)\n"
                "| where ActionType == \"ClickAllowed\" or IsClickedThrough != 0\n"
                "| where ThreatTypes has \"Phish\"\n"
                "| summarize Timestamp = min(Timestamp), Latest = max(Timestamp)\n"
                "    by ReportId, AccountUpn, Url, NetworkMessageId, IPAddress, Workload\n"
                "| project Timestamp, ReportId, AccountUpn, Url, NetworkMessageId, IPAddress, Workload, Latest"
            ),
        },
        ("email-collab/defender-for-office-365/README.md", "C3"): {
            "frequency": "P1D",
            "lookbackPeriod": "P3D",
            "entityMappings": [
                {"entityType": "User", "identifier": "AccountUpn", "columnName": "SampleAccountUpn"},
            ],
            "recommendedActions": "Review all users who clicked the domain before Defender flipped its verdict to Blocked, and hunt for subsequent sign-ins or endpoint downloads.",
            "query": (
                "// Defender XDR custom detection: earlier allowed clicks on a URL domain Defender now blocks\n"
                "UrlClickEvents\n"
                "| where Timestamp > ago(3d)\n"
                "| extend UrlDomain = tolower(parse_url(Url).Host)\n"
                "| summarize Timestamp = max(Timestamp), ReportId = any(ReportId),\n"
                "            FirstClick = min(Timestamp), Users = dcount(AccountUpn),\n"
                "            SampleAccountUpn = any(AccountUpn),\n"
                "            Allowed = countif(ActionType == \"ClickAllowed\" or IsClickedThrough != 0),\n"
                "            Blocked = countif(ActionType == \"Blocked\")\n"
                "    by UrlDomain\n"
                "| where Allowed > 0 and Blocked > 0\n"
                "| project Timestamp, ReportId, UrlDomain, SampleAccountUpn, FirstClick, Users, Allowed, Blocked"
            ),
        },
        ("identity/defender-for-identity/README.md", "C1"): {
            "frequency": "PT1H",
            "lookbackPeriod": "P1D",
            "entityMappings": [
                {"entityType": "Device", "identifier": "DeviceName", "columnName": "DestinationDeviceName"},
            ],
            "recommendedActions": "Check Defender for Identity sensor health on the quiet domain controller and confirm whether IdentityLogonEvents also stopped.",
            "query": (
                "// Defender XDR custom detection: domain controller that normally reports has gone quiet in IdentityDirectoryEvents\n"
                "// ASSUMPTION: every healthy DC emits IdentityDirectoryEvents regularly. Baseline quiet sites first.\n"
                "IdentityDirectoryEvents\n"
                "| where Timestamp > ago(24h)\n"
                "| summarize Rows = count(), Timestamp = max(Timestamp), ReportId = any(ReportId)\n"
                "    by DestinationDeviceName\n"
                "| where Timestamp < ago(2h)\n"
                "| project Timestamp, ReportId, DestinationDeviceName, Rows,\n"
                "          HoursQuiet = round((now() - Timestamp) / 1h, 1)"
            ),
        },
        ("identity/defender-for-identity/README.md", "C2"): {
            "frequency": "PT1H",
            "lookbackPeriod": "P1D",
            "entityMappings": [
                {"entityType": "User", "identifier": "AccountUpn", "columnName": "ActorUpn"},
            ],
            "recommendedActions": "Verify whether the Tier 0 group addition was authorised under change control; remove the dormant account and audit the initiating administrator if unapproved.",
            "query": (
                "// Defender XDR custom detection: account with no recent logons added to a Tier 0 AD group\n"
                "// ASSUMPTION: confirm ActionType and AdditionalFields property names in your tenant.\n"
                "let tier0_groups = dynamic([\"Domain Admins\", \"Enterprise Admins\", \"Schema Admins\", \"Account Operators\", \"Administrators\"]);\n"
                "IdentityDirectoryEvents\n"
                "| where Timestamp > ago(1h)\n"
                "| where ActionType has_cs \"Group\"\n"
                "| extend GroupName = tostring(parse_json(AdditionalFields).TARGET_OBJECT_ORIGINAL_NAME)\n"
                "| extend AddedAccount = tolower(tostring(parse_json(AdditionalFields).TARGET_ACCOUNT_NAME))\n"
                "| where GroupName in~ (tier0_groups) and isnotempty(AddedAccount)\n"
                "| join kind=leftouter (\n"
                "    IdentityLogonEvents\n"
                "    | where Timestamp > ago(30d)\n"
                "    | extend AccountName = tolower(AccountName)\n"
                "    | summarize LastLogon = max(Timestamp) by AccountName\n"
                ") on $left.AddedAccount == $right.AccountName\n"
                "| where isempty(LastLogon) or LastLogon < ago(30d)\n"
                "| project Timestamp, ReportId, AddedAccount, GroupName, Actor = AccountName, ActorUpn = AccountUpn, LastLogon"
            ),
        },
        ("cloud-apps/defender-for-cloud-apps/README.md", "C1"): {
            "frequency": "PT1H",
            "lookbackPeriod": "PT1H",
            "entityMappings": [
                {"entityType": "User", "identifier": "AccountObjectId", "columnName": "AccountObjectId"},
            ],
            "recommendedActions": "Inspect the downloaded objects and source IP/session; revoke Entra ID sessions if data exfiltration is suspected.",
            "query": (
                "// Defender XDR custom detection: hard threshold on cloud app downloads by one account in an hour\n"
                "// ASSUMPTION: download ActionType values vary by SaaS connector; validate against 7 days of CloudAppEvents.\n"
                "let hourly_downloads = 300;\n"
                "CloudAppEvents\n"
                "| where Timestamp > ago(1h)\n"
                "| where ActionType has_cs \"ownload\" or ActivityType has_cs \"ownload\"\n"
                "| summarize Timestamp = max(Timestamp), ReportId = any(ReportId),\n"
                "            Downloads = count(), Objects = dcount(ObjectId), Apps = make_set(Application, 5)\n"
                "    by AccountObjectId, bin(Timestamp, 1h)\n"
                "| where Downloads > hourly_downloads or Objects > 200\n"
                "| project Timestamp, ReportId, AccountObjectId, Downloads, Objects, Apps"
            ),
        },
        ("cloud-apps/defender-for-cloud-apps/README.md", "C2"): {
            "frequency": "PT1H",
            "lookbackPeriod": "PT1H",
            "entityMappings": [
                {"entityType": "User", "identifier": "AccountObjectId", "columnName": "AccountObjectId"},
            ],
            "recommendedActions": "Confirm whether the bulk deletions in non-Microsoft SaaS apps are legitimate maintenance; suspend the account and check backup recovery if malicious.",
            "query": (
                "// Defender XDR custom detection: burst of delete events in non-Microsoft SaaS apps\n"
                "// ASSUMPTION: pin exact Application strings against your connected apps before enabling.\n"
                "let hourly_deletes = 100;\n"
                "let m365_apps = dynamic([\"Microsoft SharePoint Online\", \"Microsoft OneDrive for Business\", \"Microsoft Office 365\"]);\n"
                "CloudAppEvents\n"
                "| where Timestamp > ago(1h)\n"
                "| where ActionType has_cs \"elete\" or ActivityType has_cs \"elete\"\n"
                "| where Application !in (m365_apps)\n"
                "| summarize Timestamp = max(Timestamp), ReportId = any(ReportId),\n"
                "            Deletes = count(), Objects = dcount(ObjectId), Apps = make_set(Application, 5)\n"
                "    by AccountObjectId, bin(Timestamp, 1h)\n"
                "| where Deletes > hourly_deletes\n"
                "| project Timestamp, ReportId, AccountObjectId, Deletes, Objects, Apps"
            ),
        },
        ("cloud-apps/defender-for-cloud-apps/README.md", "C3"): {
            "frequency": "PT1H",
            "lookbackPeriod": "PT1H",
            "entityMappings": [
                {"entityType": "User", "identifier": "AccountObjectId", "columnName": "AccountObjectId"},
            ],
            "recommendedActions": "Audit the guest account's access permissions and downloaded files, and confirm with the business sponsor.",
            "query": (
                "// Defender XDR custom detection: bulk downloads by an external or guest user\n"
                "// ASSUMPTION: verify IsExternalUser coverage across your connected SaaS apps.\n"
                "let hourly_downloads = 100;\n"
                "CloudAppEvents\n"
                "| where Timestamp > ago(1h)\n"
                "| where IsExternalUser == true\n"
                "| where ActionType has_cs \"ownload\" or ActivityType has_cs \"ownload\"\n"
                "| summarize Timestamp = max(Timestamp), ReportId = any(ReportId),\n"
                "            Downloads = count(), Apps = make_set(Application, 5), FirstSeen = min(Timestamp)\n"
                "    by AccountObjectId, AccountDisplayName\n"
                "| where Downloads > hourly_downloads\n"
                "| project Timestamp, ReportId, FirstSeen, AccountObjectId, AccountDisplayName, Downloads, Apps"
            ),
        },
        ("data-security/information-protection/README.md", "C3"): {
            "frequency": "PT1H",
            "lookbackPeriod": "PT1H",
            "entityMappings": [
                {"entityType": "Device", "identifier": "DeviceId", "columnName": "DeviceId"},
                {"entityType": "User", "identifier": "AccountUpn", "columnName": "InitiatingProcessAccountUpn"},
            ],
            "recommendedActions": "Review the staged files and destination media or network share, and coordinate with the data owner and Purview compliance team.",
            "query": (
                "// Defender XDR custom detection: labelled or encrypted files copied to staging or removable paths\n"
                "// ASSUMPTION: replace \"Highly Confidential\" with your organisation's top sensitivity label display name.\n"
                "DeviceFileEvents\n"
                "| where Timestamp > ago(1h)\n"
                "| where SensitivityLabel has \"Highly Confidential\" or IsAzureInfoProtectionApplied == true\n"
                "| where ActionType in (\"FileCreated\", \"FileRenamed\")\n"
                "| where FolderPath matches regex @\"(?i)^([d-z]:\\\\|\\\\\\\\.*\\\\|.*\\\\(temp|public|downloads|staging)\\\\)\"\n"
                "| summarize FileCount = count(), SampleFiles = make_set(FileName, 10),\n"
                "            Timestamp = max(Timestamp), ReportId = any(ReportId)\n"
                "    by DeviceId, DeviceName, InitiatingProcessAccountUpn, SensitivityLabel\n"
                "| where FileCount >= 10\n"
                "| project Timestamp, ReportId, DeviceId, DeviceName, InitiatingProcessAccountUpn, SensitivityLabel, FileCount, SampleFiles"
            ),
        },
        ("data-security/insider-risk/README.md", "C3"): {
            "frequency": "PT1H",
            "lookbackPeriod": "PT1H",
            "entityMappings": [
                {"entityType": "Device", "identifier": "DeviceId", "columnName": "DeviceId"},
            ],
            "recommendedActions": "Review matched DLP policies on the unmanaged device and coordinate with Purview Insider Risk Management before taking containment actions.",
            "query": (
                "// Defender XDR custom detection: repeated blocked or bypassed DLP matches on unmanaged devices\n"
                "// ASSUMPTION: DlpPolicyEnforcementMode 2 = Warn, 3 = Warn and bypass, 4 = Block.\n"
                "DataSecurityEvents\n"
                "| where Timestamp > ago(1h)\n"
                "| where IsManagedDevice == false\n"
                "| where DlpPolicyEnforcementMode in (2, 3, 4)\n"
                "| summarize Events = count(), Policies = make_set(DlpPolicyMatchInfo, 10),\n"
                "            Timestamp = max(Timestamp), ReportId = any(ReportId)\n"
                "    by DeviceName, DeviceId, DlpPolicyEnforcementMode\n"
                "| where Events >= 3\n"
                "| project Timestamp, ReportId, DeviceId, DeviceName, DlpPolicyEnforcementMode, Events, Policies"
            ),
        },
        ("data-security/purview-dlp/README.md", "C3"): {
            "frequency": "PT1H",
            "lookbackPeriod": "PT1H",
            "entityMappings": [
                {"entityType": "User", "identifier": "AccountUpn", "columnName": "AccountUpn"},
            ],
            "recommendedActions": "Review the aggregated DLP behaviours for the account in the Defender portal and escalate to Purview DLP or Insider Risk if intentional exfiltration is confirmed.",
            "query": (
                "// Defender XDR custom detection: repeated DLP behaviours for one account in 1 hour\n"
                "// ASSUMPTION: confirm ServiceSource == \"Data Loss Prevention\" in BehaviorInfo in your tenant.\n"
                "BehaviorInfo\n"
                "| where Timestamp > ago(1h)\n"
                "| where ServiceSource == \"Data Loss Prevention\"\n"
                "| join kind=inner (\n"
                "    BehaviorEntities\n"
                "    | where Timestamp > ago(1h)\n"
                "    | where isnotempty(AccountUpn)\n"
                ") on BehaviorId\n"
                "| summarize BehaviorCount = dcount(BehaviorId), Titles = make_set(Title, 10),\n"
                "            Timestamp = max(Timestamp), ReportId = any(BehaviorId)\n"
                "    by AccountUpn\n"
                "| where BehaviorCount >= 5\n"
                "| project Timestamp, ReportId, AccountUpn, BehaviorCount, Titles"
            ),
        },
        ("business-apps/copilot-studio/README.md", "C4"): {
            "frequency": "P1D",
            "lookbackPeriod": "P1D",
            "entityMappings": [
                {"entityType": "CloudApplication", "identifier": "ApplicationId", "columnName": "AgentId"},
            ],
            "recommendedActions": "Verify with the agent owner whether unauthenticated access is intentional, enforce Entra ID authentication and review connected tools and permissions.",
            "query": (
                "// Defender XDR custom detection: active published Copilot Studio agents with weak authentication posture\n"
                "// ASSUMPTION: inspect one AgentsInfo row to confirm Platform and authentication fields in your tenant.\n"
                "AgentsInfo\n"
                "| summarize arg_max(Timestamp, *) by AgentId\n"
                "| where LifecycleStatus == \"Active\" and PublishedStatus == \"Published\"\n"
                "| where Platform has \"Copilot Studio\"\n"
                "| where tostring(ToolsAuthenticationType) has_any (\"None\", \"NoAuthentication\", \"Anonymous\")\n"
                "    or tostring(RawAgentInfo) has_any (\"NoAuthentication\", \"Anonymous\")\n"
                "| extend ReportId = tostring(AgentId)\n"
                "| project Timestamp, ReportId, AgentId, AgentName, Platform, EntraAgentId, ToolsAuthenticationType, Permissions"
            ),
        },
    }

    xdr_rules: list[dict[str, Any]] = []
    for d in raw_detections:
        m = re.match(r"^(C\d+)\.", d["h3"])
        cid_tag = m.group(1) if m else ""
        key = (d["file"], cid_tag)
        if key not in xdr_specs:
            continue
        spec = xdr_specs[key]
        title = clean_title(d["h3"])
        short_product = d["product"].replace("Microsoft ", "").strip()
        display_name = f"{short_product} - {title}"
        tables = extract_tables(spec["query"])
        severity = parse_severity(d["h3"])
        tactics, techs = extract_mitre(d["post"] + "\n" + d["pre"] + "\n" + d["h3"] + "\n" + spec["query"])
        desc_parts = []
        if d["pre"] and not d["pre"].startswith("|"):
            desc_parts.append(clean_prose(d["pre"]))
        if d["post"]:
            desc_parts.append(clean_prose(d["post"]))
        if not desc_parts:
            desc_parts.append(f"Defender XDR custom detection for {d['product']}: {title}.")
        desc_parts.append(f"Source guide: {d['file']} ({cid_tag}).")

        filename = f"{slugify(d['product_slug'], 32)}_{cid_tag}_{slugify(title, 40)}.yaml"
        xdr_rules.append({
            "filename": filename,
            "id": det_uuid(f"xdr-custom-detection:{d['file']}:{cid_tag}"),
            "displayName": display_name,
            "description": " ".join(desc_parts),
            "severity": severity,
            "frequency": spec["frequency"],
            "lookbackPeriod": spec["lookbackPeriod"],
            "sourceGuide": d["file"],
            "requiredTables": tables,
            "tactics": tactics,
            "relevantTechniques": techs,
            "entityMappings": spec["entityMappings"],
            "recommendedActions": spec["recommendedActions"],
            "query": spec["query"],
            "product": d["product"],
        })
    return xdr_rules


def build_xdr_hunting_queries(raw_hunts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    xdr_hunts: list[dict[str, Any]] = []
    idx_map: dict[str, int] = {}
    for h in raw_hunts:
        tables = extract_tables(h["code"])
        if not any(t in XDR_ALL_TABLES for t in tables):
            continue
        slug = h["product_slug"]
        idx_map[slug] = idx_map.get(slug, 0) + 1
        idx = idx_map[slug]
        code = h["code"]
        # Ensure Defender XDR advanced hunting uses Timestamp
        if re.search(r"\bTimeGenerated\b", code):
            code = re.sub(r"\bTimeGenerated\b", "Timestamp", code)
        title = ""
        first_comment = next((l.strip()[2:].strip() for l in code.splitlines() if l.strip().startswith("//") and not l.strip().startswith("// ASSUMPTION")), "")
        if first_comment:
            title = re.sub(r"^(?:HUNT|Hunt)\s*[-:]\s*", "", first_comment).strip()
        if not title and h["pre"]:
            m = re.search(r"\*\*([^*]+)\*\*", h["pre"].splitlines()[-1])
            if m:
                title = m.group(1).strip().rstrip(".")
        if not title:
            title = f"{h['product']} advanced hunting query {idx}"
        title = title.replace("`", "")
        fname = f"{slugify(slug, 28)}_H{idx}_{slugify(title, 36)}.kql"
        xdr_hunts.append({
            "filename": fname,
            "title": f"{h['product'].replace('Microsoft ', '').strip()} - {title}",
            "tables": tables,
            "sourceGuide": h["file"],
            "query": code,
        })

    # Include pre-streaming cost preview from queries/cost/07-xdr-streaming-cost-preview.kql
    cost_xdr = (ROOT / "queries/cost/07-xdr-streaming-cost-preview.kql").read_text(encoding="utf-8").strip()
    xdr_hunts.append({
        "filename": "xdr_streaming_cost_preview.kql",
        "title": "Defender XDR - Pre-streaming GB/day cost preview",
        "tables": ["DeviceProcessEvents", "DeviceNetworkEvents", "DeviceFileEvents", "EmailEvents", "IdentityLogonEvents", "CloudAppEvents"],
        "sourceGuide": "queries/cost/07-xdr-streaming-cost-preview.kql",
        "query": cost_xdr,
    })
    return xdr_hunts


def split_techniques(techs: list[str]) -> tuple[list[str], list[str]]:
    parents: list[str] = []
    subs: list[str] = []
    for t in techs:
        if "." in t:
            base = t.split(".")[0]
            if base not in parents:
                parents.append(base)
            if t not in subs:
                subs.append(t)
        else:
            if t not in parents:
                parents.append(t)
    return parents, subs


def trigger_op_arm(op: str) -> str:
    return {
        "gt": "GreaterThan",
        "lt": "LessThan",
        "eq": "Equal",
        "ne": "NotEqual",
    }.get(op, "GreaterThan")


def build_main_template(
    analytic_rules: list[dict[str, Any]],
    hunting_queries: list[dict[str, Any]],
    workbooks: list[dict[str, Any]],
) -> dict[str, Any]:
    variables: dict[str, Any] = {
        "_solutionName": SOLUTION_DISPLAY_NAME,
        "_solutionVersion": SOLUTION_VERSION,
        "solutionId": SOLUTION_ID,
        "_solutionId": "[variables('solutionId')]",
        "workspaceResourceId": "[resourceId('Microsoft.OperationalInsights/workspaces', parameters('workspace'))]",
        "_solutioncontentProductId": (
            "[concat(take(variables('_solutionId'),50),'-','sl','-',"
            "uniqueString(concat(variables('_solutionId'),'-','Solution','-',variables('_solutionId'),'-',variables('_solutionVersion'))))]"
        ),
    }

    package_deps: list[dict[str, Any]] = []
    resources: list[dict[str, Any]] = []

    # 1. Solution ContentPackage resource (V3 anchor)
    package_resource: dict[str, Any] = {
        "type": "Microsoft.OperationalInsights/workspaces/providers/contentPackages",
        "apiVersion": "2023-04-01-preview",
        "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/', variables('_solutionId'))]",
        "location": "[parameters('workspace-location')]",
        "properties": {
            "version": SOLUTION_VERSION,
            "kind": "Solution",
            "contentSchemaVersion": "3.0.0",
            "displayName": SOLUTION_DISPLAY_NAME,
            "publisherDisplayName": AUTHOR_NAME,
            "descriptionHtml": (
                f"<p>Community-maintained Microsoft Sentinel solution packaged from the "
                f"<a href=\"{REPO_URL}\">Microsoft security logging guide</a>. Includes "
                f"<strong>{len(analytic_rules)} analytic rule templates</strong>, "
                f"<strong>{len(hunting_queries)} hunting queries</strong> and "
                f"<strong>{len(workbooks)} workbooks</strong> covering all 38 documented Microsoft security log sources, "
                f"ingestion health monitoring and cost estimation.</p>"
            ),
            "contentKind": "Solution",
            "contentProductId": "[variables('_solutioncontentProductId')]",
            "id": "[variables('_solutioncontentProductId')]",
            "contentId": "[variables('_solutionId')]",
            "parentId": "[variables('_solutionId')]",
            "source": {
                "kind": "Solution",
                "name": SOLUTION_DISPLAY_NAME,
                "sourceId": "[variables('_solutionId')]",
            },
            "author": {"name": AUTHOR_NAME},
            "support": {
                "name": AUTHOR_NAME,
                "tier": "Community",
                "link": SUPPORT_LINK,
            },
            "dependencies": {
                "operator": "AND",
                "criteria": package_deps,
            },
            "firstPublishDate": FIRST_PUBLISH_DATE,
            "providers": ["Microsoft", "Community"],
            "categories": {
                "domains": [
                    "Security - Threat Protection",
                    "Security - SIEM",
                    "Identity",
                ]
            },
        },
    }
    resources.append(package_resource)

    pkg_depends = [
        "[extensionResourceId(resourceId('Microsoft.OperationalInsights/workspaces', parameters('workspace')), 'Microsoft.SecurityInsights/contentPackages', variables('_solutionId'))]"
    ]

    # 2. Analytic Rules contentTemplates
    for idx, rule in enumerate(analytic_rules, 1):
        obj_key = f"analyticRuleObject{idx}"
        cid = rule["id"]
        ver = rule["version"]
        variables[obj_key] = {
            f"analyticRuleVersion{idx}": ver,
            f"_analyticRulecontentId{idx}": cid,
            f"analyticRuleId{idx}": f"[resourceId('Microsoft.OperationalInsights/workspaces/providers/alertRules', parameters('workspace'), 'Microsoft.SecurityInsights', '{cid}')]",
            f"analyticRuleTemplateSpecName{idx}": f"[concat(parameters('workspace'),'/Microsoft.SecurityInsights/',concat(parameters('workspace'),'-ar-',uniqueString('{cid}')))]",
            f"_analyticRulecontentProductId{idx}": f"[concat(take(variables('_solutionId'),50),'-','ar','-',uniqueString(concat(variables('_solutionId'),'-','AnalyticsRule','-','{cid}','-','{ver}')))]",
        }
        package_deps.append({
            "kind": "AnalyticsRule",
            "contentId": f"[variables('{obj_key}')._analyticRulecontentId{idx}]",
            "version": f"[variables('{obj_key}').analyticRuleVersion{idx}]",
        })

        parents, subs = split_techniques(rule["relevantTechniques"])
        alert_props: dict[str, Any] = {
            "description": rule["description"],
            "displayName": rule["name"],
            "enabled": False,
            "query": rule["query"],
            "queryFrequency": yaml_dur_to_iso(rule["queryFrequency"]),
            "queryPeriod": yaml_dur_to_iso(rule["queryPeriod"]),
            "severity": rule["severity"],
            "suppressionDuration": "PT1H",
            "suppressionEnabled": False,
            "triggerOperator": trigger_op_arm(rule["triggerOperator"]),
            "triggerThreshold": rule["triggerThreshold"],
            "requiredDataConnectors": rule["requiredDataConnectors"],
            "tactics": rule["tactics"],
        }
        if parents:
            alert_props["techniques"] = parents
        if subs:
            alert_props["subTechniques"] = subs
        if rule["entityMappings"]:
            alert_props["entityMappings"] = rule["entityMappings"]

        resources.append({
            "type": "Microsoft.OperationalInsights/workspaces/providers/contentTemplates",
            "apiVersion": "2023-04-01-preview",
            "name": f"[variables('{obj_key}').analyticRuleTemplateSpecName{idx}]",
            "location": "[parameters('workspace-location')]",
            "dependsOn": pkg_depends,
            "condition": "[parameters('DeployAnalyticsRule')]",
            "properties": {
                "description": f"{rule['name']} Analytic Rule template version {ver}",
                "mainTemplate": {
                    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
                    "contentVersion": f"[variables('{obj_key}').analyticRuleVersion{idx}]",
                    "parameters": {},
                    "variables": {},
                    "resources": [
                        {
                            "type": "Microsoft.SecurityInsights/AlertRuleTemplates",
                            "name": f"[variables('{obj_key}')._analyticRulecontentId{idx}]",
                            "apiVersion": "2023-02-01-preview",
                            "kind": "Scheduled",
                            "location": "[parameters('workspace-location')]",
                            "properties": alert_props,
                        },
                        {
                            "type": "Microsoft.OperationalInsights/workspaces/providers/metadata",
                            "apiVersion": "2022-01-01-preview",
                            "name": f"[concat(parameters('workspace'),'/Microsoft.SecurityInsights/',concat('AnalyticsRule-', last(split(variables('{obj_key}').analyticRuleId{idx},'/'))))]",
                            "properties": {
                                "description": f"{SOLUTION_DISPLAY_NAME} Analytics Rule {idx}",
                                "parentId": f"[variables('{obj_key}').analyticRuleId{idx}]",
                                "contentId": f"[variables('{obj_key}')._analyticRulecontentId{idx}]",
                                "kind": "AnalyticsRule",
                                "version": f"[variables('{obj_key}').analyticRuleVersion{idx}]",
                                "source": {
                                    "kind": "Solution",
                                    "name": SOLUTION_DISPLAY_NAME,
                                    "sourceId": "[variables('_solutionId')]",
                                },
                                "author": {"name": AUTHOR_NAME},
                                "support": {
                                    "name": AUTHOR_NAME,
                                    "tier": "Community",
                                    "link": SUPPORT_LINK,
                                },
                            },
                        },
                    ],
                },
                "packageKind": "Solution",
                "packageVersion": "[variables('_solutionVersion')]",
                "packageName": "[variables('_solutionName')]",
                "packageId": "[variables('_solutionId')]",
                "contentSchemaVersion": "3.0.0",
                "contentId": f"[variables('{obj_key}')._analyticRulecontentId{idx}]",
                "contentKind": "AnalyticsRule",
                "displayName": rule["name"],
                "contentProductId": f"[variables('{obj_key}')._analyticRulecontentProductId{idx}]",
                "id": f"[variables('{obj_key}')._analyticRulecontentProductId{idx}]",
                "version": f"[variables('{obj_key}').analyticRuleVersion{idx}]",
            },
        })

    # 3. Hunting Queries contentTemplates
    for idx, hq in enumerate(hunting_queries, 1):
        obj_key = f"huntingQueryObject{idx}"
        cid = hq["id"]
        ver = hq["version"]
        variables[obj_key] = {
            f"huntingQueryVersion{idx}": ver,
            f"_huntingQuerycontentId{idx}": cid,
            f"huntingQueryTemplateSpecName{idx}": f"[concat(parameters('workspace'),'/Microsoft.SecurityInsights/',concat(parameters('workspace'),'-hq-',uniqueString('{cid}')))]",
            f"_huntingQuerycontentProductId{idx}": f"[concat(take(variables('_solutionId'),50),'-','hq','-',uniqueString(concat(variables('_solutionId'),'-','HuntingQuery','-','{cid}','-','{ver}')))]",
        }
        package_deps.append({
            "kind": "HuntingQuery",
            "contentId": f"[variables('{obj_key}')._huntingQuerycontentId{idx}]",
            "version": f"[variables('{obj_key}').huntingQueryVersion{idx}]",
        })

        tags = [
            {"name": "description", "value": hq["description"]},
            {"name": "tactics", "value": ",".join(hq["tactics"])},
        ]
        if hq["relevantTechniques"]:
            tags.append({"name": "techniques", "value": ",".join(hq["relevantTechniques"])})

        resources.append({
            "type": "Microsoft.OperationalInsights/workspaces/providers/contentTemplates",
            "apiVersion": "2023-04-01-preview",
            "name": f"[variables('{obj_key}').huntingQueryTemplateSpecName{idx}]",
            "location": "[parameters('workspace-location')]",
            "dependsOn": pkg_depends,
            "condition": "[parameters('DeployHuntingQuery')]",
            "properties": {
                "description": f"{hq['name']} Hunting Query template version {ver}",
                "mainTemplate": {
                    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
                    "contentVersion": f"[variables('{obj_key}').huntingQueryVersion{idx}]",
                    "parameters": {},
                    "variables": {},
                    "resources": [
                        {
                            "type": "Microsoft.OperationalInsights/savedSearches",
                            "apiVersion": "2025-07-01",
                            "name": f"MSLG_Hunting_Query_{idx}",
                            "location": "[parameters('workspace-location')]",
                            "properties": {
                                "eTag": "*",
                                "displayName": hq["name"],
                                "category": "Hunting Queries",
                                "query": hq["query"],
                                "version": 2,
                                "tags": tags,
                            },
                        },
                        {
                            "type": "Microsoft.OperationalInsights/workspaces/providers/metadata",
                            "apiVersion": "2022-01-01-preview",
                            "name": f"[concat(parameters('workspace'),'/Microsoft.SecurityInsights/',concat('HuntingQuery-', last(split(resourceId('Microsoft.OperationalInsights/savedSearches', variables('{obj_key}')._huntingQuerycontentId{idx}),'/'))))]",
                            "properties": {
                                "description": f"{SOLUTION_DISPLAY_NAME} Hunting Query {idx}",
                                "parentId": f"[resourceId('Microsoft.OperationalInsights/savedSearches', variables('{obj_key}')._huntingQuerycontentId{idx})]",
                                "contentId": f"[variables('{obj_key}')._huntingQuerycontentId{idx}]",
                                "kind": "HuntingQuery",
                                "version": f"[variables('{obj_key}').huntingQueryVersion{idx}]",
                                "source": {
                                    "kind": "Solution",
                                    "name": SOLUTION_DISPLAY_NAME,
                                    "sourceId": "[variables('_solutionId')]",
                                },
                                "author": {"name": AUTHOR_NAME},
                                "support": {
                                    "name": AUTHOR_NAME,
                                    "tier": "Community",
                                    "link": SUPPORT_LINK,
                                },
                            },
                        },
                    ],
                },
                "packageKind": "Solution",
                "packageVersion": "[variables('_solutionVersion')]",
                "packageName": "[variables('_solutionName')]",
                "packageId": "[variables('_solutionId')]",
                "contentSchemaVersion": "3.0.0",
                "contentId": f"[variables('{obj_key}')._huntingQuerycontentId{idx}]",
                "contentKind": "HuntingQuery",
                "displayName": hq["name"],
                "contentProductId": f"[variables('{obj_key}')._huntingQuerycontentProductId{idx}]",
                "id": f"[variables('{obj_key}')._huntingQuerycontentProductId{idx}]",
                "version": f"[variables('{obj_key}').huntingQueryVersion{idx}]",
            },
        })

    # 4. Workbooks contentTemplates
    for idx, wb in enumerate(workbooks, 1):
        cid = wb["contentId"]
        ver = wb["version"]
        variables[f"workbookVersion{idx}"] = ver
        variables[f"workbookContentId{idx}"] = cid
        variables[f"_workbookContentId{idx}"] = f"[variables('workbookContentId{idx}')]"
        variables[f"workbookId{idx}"] = f"[resourceId('Microsoft.Insights/workbooks', variables('workbookContentId{idx}'))]"
        variables[f"workbookTemplateSpecName{idx}"] = (
            f"[concat(parameters('workspace'),'/Microsoft.SecurityInsights/',"
            f"concat(parameters('workspace'),'-wb-',uniqueString(variables('_workbookContentId{idx}'))))]"
        )
        variables[f"_workbookcontentProductId{idx}"] = (
            f"[concat(take(variables('_solutionId'),50),'-','wb','-',"
            f"uniqueString(concat(variables('_solutionId'),'-','Workbook','-',variables('_workbookContentId{idx}'),'-',variables('workbookVersion{idx}'))))]"
        )
        package_deps.append({
            "kind": "Workbook",
            "contentId": f"[variables('_workbookContentId{idx}')]",
            "version": f"[variables('workbookVersion{idx}')]",
        })

        resources.append({
            "type": "Microsoft.OperationalInsights/workspaces/providers/contentTemplates",
            "apiVersion": "2023-04-01-preview",
            "name": f"[variables('workbookTemplateSpecName{idx}')]",
            "location": "[parameters('workspace-location')]",
            "dependsOn": pkg_depends,
            "condition": "[parameters('DeployWorkbook')]",
            "properties": {
                "description": f"{wb['displayName']} Workbook template version {ver}",
                "mainTemplate": {
                    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
                    "contentVersion": f"[variables('workbookVersion{idx}')]",
                    "parameters": {},
                    "variables": {},
                    "resources": [
                        {
                            "type": "Microsoft.Insights/workbooks",
                            "name": f"[variables('workbookContentId{idx}')]",
                            "location": "[parameters('workspace-location')]",
                            "kind": "shared",
                            "apiVersion": "2021-08-01",
                            "metadata": {"description": wb["description"]},
                            "properties": {
                                "displayName": f"[parameters('{wb['paramName']}')]",
                                "serializedData": json.dumps(wb["json"], separators=(",", ":")),
                                "version": "1.0",
                                "sourceId": "[variables('workspaceResourceId')]",
                                "category": "sentinel",
                            },
                        },
                        {
                            "type": "Microsoft.OperationalInsights/workspaces/providers/metadata",
                            "apiVersion": "2022-01-01-preview",
                            "name": f"[concat(parameters('workspace'),'/Microsoft.SecurityInsights/',concat('Workbook-', last(split(variables('workbookId{idx}'),'/'))))]",
                            "properties": {
                                "description": wb["description"],
                                "parentId": f"[variables('workbookId{idx}')]",
                                "contentId": f"[variables('_workbookContentId{idx}')]",
                                "kind": "Workbook",
                                "version": f"[variables('workbookVersion{idx}')]",
                                "source": {
                                    "kind": "Solution",
                                    "name": SOLUTION_DISPLAY_NAME,
                                    "sourceId": "[variables('_solutionId')]",
                                },
                                "author": {"name": AUTHOR_NAME},
                                "support": {
                                    "name": AUTHOR_NAME,
                                    "tier": "Community",
                                    "link": SUPPORT_LINK,
                                },
                            },
                        },
                    ],
                },
                "packageKind": "Solution",
                "packageVersion": "[variables('_solutionVersion')]",
                "packageName": "[variables('_solutionName')]",
                "packageId": "[variables('_solutionId')]",
                "contentSchemaVersion": "3.0.0",
                "contentId": f"[variables('_workbookContentId{idx}')]",
                "contentKind": "Workbook",
                "displayName": f"[parameters('{wb['paramName']}')]",
                "contentProductId": f"[variables('_workbookcontentProductId{idx}')]",
                "id": f"[variables('_workbookcontentProductId{idx}')]",
                "version": f"[variables('workbookVersion{idx}')]",
            },
        })

    template: dict[str, Any] = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "metadata": {
            "author": AUTHOR_NAME,
            "comments": (
                f"Microsoft Sentinel Content Hub V3 solution generated from {REPO_URL}. "
                f"Deploys {len(analytic_rules)} analytic rule templates, {len(hunting_queries)} hunting queries "
                f"and {len(workbooks)} workbooks into an existing Log Analytics workspace."
            ),
        },
        "parameters": {
            "location": {
                "type": "string",
                "minLength": 1,
                "defaultValue": "[resourceGroup().location]",
                "metadata": {
                    "description": "Fallback deployment location (derived from resource group). Resources deploy to workspace-location."
                },
            },
            "workspace": {
                "type": "string",
                "minLength": 1,
                "metadata": {
                    "description": "Name of the existing Log Analytics workspace where Microsoft Sentinel is enabled."
                },
            },
            "workspace-location": {
                "type": "string",
                "minLength": 1,
                "defaultValue": "[resourceGroup().location]",
                "metadata": {
                    "description": "Azure region of the existing Log Analytics workspace."
                },
            },
            "workbook1-name": {
                "type": "string",
                "minLength": 1,
                "defaultValue": workbooks[0]["displayName"],
                "metadata": {
                    "description": "Display name for the Ingestion Health and Table Freshness workbook."
                },
            },
            "workbook2-name": {
                "type": "string",
                "minLength": 1,
                "defaultValue": workbooks[1]["displayName"],
                "metadata": {
                    "description": "Display name for the Cost Estimation and Volume Monitoring workbook."
                },
            },
            "DeployAnalyticsRule": {
                "type": "bool",
                "defaultValue": True,
                "metadata": {
                    "description": "Deploy Microsoft Sentinel analytic rule templates from the solution."
                },
            },
            "DeployHuntingQuery": {
                "type": "bool",
                "defaultValue": True,
                "metadata": {
                    "description": "Deploy Microsoft Sentinel hunting query templates from the solution."
                },
            },
            "DeployWorkbook": {
                "type": "bool",
                "defaultValue": True,
                "metadata": {
                    "description": "Deploy Microsoft Sentinel workbook templates from the solution."
                },
            },
        },
        "variables": variables,
        "resources": resources,
        "outputs": {
            "solutionId": {
                "type": "string",
                "value": "[variables('_solutionId')]",
            },
            "workspaceName": {
                "type": "string",
                "value": "[parameters('workspace')]",
            },
            "workspaceLocation": {
                "type": "string",
                "value": "[parameters('workspace-location')]",
            },
        },
    }
    return template


def build_create_ui_definition(
    analytic_rules: list[dict[str, Any]],
    hunting_queries: list[dict[str, Any]],
    workbooks: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "$schema": "https://schema.management.azure.com/schemas/0.1.2-preview/CreateUIDefinition.MultiVm.json#",
        "handler": "Microsoft.Azure.CreateUIDef",
        "version": "0.1.2-preview",
        "parameters": {
            "config": {
                "isWizard": False,
                "basics": {
                    "description": (
                        f"Deploys the **{SOLUTION_DISPLAY_NAME}** Microsoft Sentinel Content Hub V3 solution "
                        f"into an existing Sentinel-enabled Log Analytics workspace.\n\n"
                        f"**Analytic Rules:** {len(analytic_rules)}, "
                        f"**Hunting Queries:** {len(hunting_queries)}, "
                        f"**Workbooks:** {len(workbooks)}\n\n"
                        f"[View guide and source KQL]({REPO_URL})"
                    ),
                    "subscription": {
                        "resourceProviders": [
                            "Microsoft.OperationsManagement/solutions",
                            "Microsoft.OperationalInsights/workspaces/providers/alertRules",
                            "Microsoft.Insights/workbooks",
                        ]
                    },
                    "location": {
                        "metadata": {
                            "hidden": "Location is derived from the selected Log Analytics workspace."
                        },
                        "visible": False,
                    },
                    "resourceGroup": {
                        "allowExisting": True,
                    },
                },
            },
            "basics": [
                {
                    "name": "getLAWorkspace",
                    "type": "Microsoft.Solutions.ArmApiControl",
                    "toolTip": "Lists Log Analytics workspaces in the selected resource group.",
                    "condition": "[greater(length(resourceGroup().name),0)]",
                    "request": {
                        "method": "GET",
                        "path": "[concat(subscription().id,'/providers/Microsoft.OperationalInsights/workspaces?api-version=2020-08-01')]",
                    },
                },
                {
                    "name": "workspace",
                    "type": "Microsoft.Common.DropDown",
                    "label": "Workspace",
                    "placeholder": "Select a Log Analytics workspace",
                    "toolTip": "Select the Log Analytics workspace where Microsoft Sentinel is enabled.",
                    "constraints": {
                        "allowedValues": "[map(filter(basics('getLAWorkspace').value, (filter) => contains(toLower(filter.id), toLower(resourceGroup().name))), (item) => parse(concat('{\"label\":\"', item.name, '\",\"value\":\"', item.name, '\"}')))]",
                        "required": True,
                    },
                    "visible": True,
                },
            ],
            "steps": [
                {
                    "name": "contentSelection",
                    "label": "Content selection",
                    "elements": [
                        {
                            "name": "DeployAnalyticsRule",
                            "type": "Microsoft.Common.CheckBox",
                            "label": f"Deploy Analytic Rule templates ({len(analytic_rules)})",
                            "defaultValue": True,
                            "toolTip": "Installs all custom detection rule templates into Microsoft Sentinel Analytics Rule Templates (disabled by default until you enable and tune them).",
                        },
                        {
                            "name": "DeployHuntingQuery",
                            "type": "Microsoft.Common.CheckBox",
                            "label": f"Deploy Hunting Queries ({len(hunting_queries)})",
                            "defaultValue": True,
                            "toolTip": "Installs hunting queries from the product guides and operational packs.",
                        },
                        {
                            "name": "DeployWorkbook",
                            "type": "Microsoft.Common.CheckBox",
                            "label": f"Deploy Workbooks ({len(workbooks)})",
                            "defaultValue": True,
                            "toolTip": "Installs the Ingestion Health and Cost Estimation workbook templates.",
                        },
                    ],
                },
                {
                    "name": "workbooks",
                    "label": "Workbooks",
                    "elements": [
                        {
                            "name": "workbook1-name",
                            "type": "Microsoft.Common.TextBox",
                            "label": "Ingestion Health workbook name",
                            "defaultValue": workbooks[0]["displayName"],
                            "toolTip": "Display name for the Ingestion Health and Table Freshness workbook.",
                            "constraints": {"required": True},
                        },
                        {
                            "name": "workbook2-name",
                            "type": "Microsoft.Common.TextBox",
                            "label": "Cost Estimation workbook name",
                            "defaultValue": workbooks[1]["displayName"],
                            "toolTip": "Display name for the Cost Estimation and Volume Monitoring workbook.",
                            "constraints": {"required": True},
                        },
                    ],
                },
            ],
            "outputs": {
                "workspace": "[basics('workspace')]",
                "workspace-location": "[first(map(filter(basics('getLAWorkspace').value, (filter) => and(contains(toLower(filter.id), toLower(resourceGroup().name)), equals(filter.name, basics('workspace')))), (item) => item.location))]",
                "location": "[location()]",
                "workbook1-name": "[steps('workbooks').'workbook1-name']",
                "workbook2-name": "[steps('workbooks').'workbook2-name']",
                "DeployAnalyticsRule": "[steps('contentSelection').DeployAnalyticsRule]",
                "DeployHuntingQuery": "[steps('contentSelection').DeployHuntingQuery]",
                "DeployWorkbook": "[steps('contentSelection').DeployWorkbook]",
            },
        },
    }


def write_json(path: Path, data: Any, indent: int = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=indent, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    raw_detections, raw_hunts = extract_guide_kql()
    analytic_rules = build_sentinel_analytic_rules(raw_detections)
    hunting_queries = build_sentinel_hunting_queries(raw_hunts)
    workbooks = build_workbooks()
    xdr_rules = build_xdr_custom_detections(raw_detections)
    xdr_hunts = build_xdr_hunting_queries(raw_hunts)

    # Clean generated subdirectories cleanly so renamed files never linger
    for sub in ("Analytic Rules", "Hunting Queries", "Workbooks", "Data", "Package"):
        target = SOLUTION_DIR / sub
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)

    for sub in ("rules", "hunting"):
        target = XDR_DIR / sub
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)

    # Write Analytic Rules YAML
    ar_paths: list[str] = []
    for rule in analytic_rules:
        rel_path = f"Analytic Rules/{rule['filename']}"
        ar_paths.append(rel_path)
        (SOLUTION_DIR / rel_path).write_text(render_analytic_rule_yaml(rule), encoding="utf-8")

    # Write Hunting Queries YAML
    hq_paths: list[str] = []
    for hq in hunting_queries:
        rel_path = f"Hunting Queries/{hq['filename']}"
        hq_paths.append(rel_path)
        (SOLUTION_DIR / rel_path).write_text(render_hunting_query_yaml(hq), encoding="utf-8")

    # Write Workbooks JSON
    wb_paths: list[str] = []
    for wb in workbooks:
        rel_path = f"Workbooks/{wb['filename']}"
        wb_paths.append(rel_path)
        write_json(SOLUTION_DIR / rel_path, wb["json"])

    # Write SolutionMetadata.json
    metadata = {
        "publisherId": PUBLISHER_ID,
        "offerId": OFFER_ID,
        "firstPublishDate": FIRST_PUBLISH_DATE,
        "providers": ["Microsoft", "Community"],
        "categories": {
            "domains": [
                "Security - Threat Protection",
                "Security - SIEM",
                "Identity",
            ]
        },
        "support": {
            "name": AUTHOR_NAME,
            "tier": "Community",
            "link": SUPPORT_LINK,
        },
        "version": SOLUTION_VERSION,
    }
    write_json(SOLUTION_DIR / "SolutionMetadata.json", metadata)

    # Write Data/Solution_MicrosoftSecurityLoggingGuide.json (V3 packaging input)
    solution_data = {
        "Name": SOLUTION_DISPLAY_NAME,
        "Author": AUTHOR_NAME,
        "Description": (
            f"Community Microsoft Sentinel Content Hub V3 solution generated from the "
            f"[Microsoft security logging guide]({REPO_URL}). Packages {len(analytic_rules)} analytic rule templates, "
            f"{len(hunting_queries)} hunting queries and {len(workbooks)} operational workbooks."
        ),
        "Analytic Rules": ar_paths,
        "Hunting Queries": hq_paths,
        "Workbooks": wb_paths,
        "BasePath": f"solution/Solutions/{SOLUTION_NAME}",
        "Metadata": "SolutionMetadata.json",
        "TemplateSpec": True,
        "Version": SOLUTION_VERSION,
    }
    write_json(SOLUTION_DIR / "Data" / f"Solution_{SOLUTION_NAME}.json", solution_data)

    # Write ReleaseNotes.md
    release_notes = (
        f"# Release notes\n\n"
        f"| **Version** | **Date modified (YYYY-MM-DD)** | **Change history** |\n"
        f"|---|---|---|\n"
        f"| {SOLUTION_VERSION} | {FIRST_PUBLISH_DATE} | Initial Content Hub V3 solution release packaging "
        f"{len(analytic_rules)} analytic rule templates, {len(hunting_queries)} hunting queries and "
        f"{len(workbooks)} workbooks from the Microsoft security logging guide. |\n"
    )
    (SOLUTION_DIR / "ReleaseNotes.md").write_text(release_notes, encoding="utf-8")

    # Write Package/mainTemplate.json and Package/createUiDefinition.json
    main_template = build_main_template(analytic_rules, hunting_queries, workbooks)
    create_ui = build_create_ui_definition(analytic_rules, hunting_queries, workbooks)
    write_json(SOLUTION_DIR / "Package" / "mainTemplate.json", main_template, indent=2)
    write_json(SOLUTION_DIR / "Package" / "createUiDefinition.json", create_ui, indent=2)

    # Write Defender XDR custom detections and hunting queries
    for xr in xdr_rules:
        (XDR_DIR / "rules" / xr["filename"]).write_text(render_xdr_rule_yaml(xr), encoding="utf-8")
    for xh in xdr_hunts:
        (XDR_DIR / "hunting" / xh["filename"]).write_text(xh["query"].rstrip() + "\n", encoding="utf-8")

    mt_size_kb = (SOLUTION_DIR / "Package" / "mainTemplate.json").stat().st_size / 1024
    print(
        f"Built {SOLUTION_DISPLAY_NAME} v{SOLUTION_VERSION}:\n"
        f"  Analytic Rules:       {len(analytic_rules)}\n"
        f"  Hunting Queries:      {len(hunting_queries)}\n"
        f"  Workbooks:            {len(workbooks)}\n"
        f"  mainTemplate.json:    {mt_size_kb:.1f} KB ({len(main_template['resources'])} resources)\n"
        f"  Defender XDR rules:   {len(xdr_rules)}\n"
        f"  Defender XDR hunts:   {len(xdr_hunts)}"
    )


if __name__ == "__main__":
    main()
