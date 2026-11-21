#!/usr/bin/env python3
"""Validate Microsoft Sentinel Content Hub V3 solution files, ARM templates,
Defender XDR custom detection rules, and KQL queries across the repository.

Checks:
1. SolutionMetadata.json and Data/Solution_*.json manifest integrity and versions.
2. Analytic Rules YAML schema (UUIDs, severity, requiredDataConnectors,
   queryFrequency <= queryPeriod <= 14d, tactics, techniques, entityMappings
   with column presence verification, kind).
3. Hunting Queries YAML schema (UUIDs, requiredDataConnectors, tactics,
   entityMappings).
4. Workbooks JSON schema (Notebook/1.0, KQL tiles).
5. Package/mainTemplate.json and Package/createUiDefinition.json (valid ARM JSON,
   required workspace/location parameters, contentPackages/contentTemplates
   completeness, balanced ARM expressions, resource count < 800, size < 4 MB,
   createUiDefinition outputs match mainTemplate parameters, no hardcoded IDs
   or secrets).
6. Defender XDR custom detections (Timestamp, ReportId, DeviceId for MDE
   Device* tables, valid frequencies, entityMappings, no TimeGenerated).
7. KQL syntax sanity across all YAML rules, workbooks, defender-xdr files and
   queries/**/*.kql (balanced parentheses/brackets/braces/strings, non-empty).
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
SOLUTION_NAME = "MicrosoftSecurityLoggingGuide"
SOLUTION_DIR = ROOT / "solution" / "Solutions" / SOLUTION_NAME
XDR_DIR = ROOT / "defender-xdr"

VALID_SEVERITIES = {"High", "Medium", "Low", "Informational"}
VALID_TRIGGER_OPS = {"gt", "lt", "eq", "ne"}
VALID_TACTICS = {
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
    "ImpairProcessControl",
    "InhibitResponseFunction",
    "PreAttack",
}

VALID_SENTINEL_ENTITIES: dict[str, set[str]] = {
    "Account": {"FullName", "Name", "UPNSuffix", "Sid", "AadUserId", "ObjectGuid", "NTDomain", "DnsDomain", "PUID"},
    "Host": {"HostName", "FullName", "DnsDomain", "NTDomain", "NetBiosName", "AzureID", "OMSAgentID", "OSFamily"},
    "IP": {"Address"},
    "URL": {"Url"},
    "DNS": {"DomainName"},
    "AzureResource": {"ResourceId"},
    "File": {"Name", "Directory"},
    "FileHash": {"Algorithm", "Value"},
    "Process": {"ProcessId", "CommandLine"},
    "CloudApplication": {"AppId", "Name", "InstanceName"},
    "MailMessage": {"Recipient", "Sender", "NetworkMessageId", "Subject", "DeliveryAction", "DeliveryLocation"},
    "Mailbox": {"MailboxPrimaryAddress", "DisplayName", "Upn", "ExternalDirectoryObjectId"},
    "SecurityGroup": {"DistinguishedName", "SID", "ObjectGuid"},
}

VALID_XDR_FREQUENCIES = {"NRT", "PT1H", "PT3H", "PT12H", "P1D"}
VALID_XDR_ENTITIES = {"Device", "User", "Mailbox", "MailMessage", "File", "CloudApplication", "IP"}
MDE_TABLES = {
    "DeviceEvents",
    "DeviceProcessEvents",
    "DeviceNetworkEvents",
    "DeviceFileEvents",
    "DeviceRegistryEvents",
    "DeviceLogonEvents",
    "DeviceImageLoadEvents",
    "DeviceInfo",
}

# Patterns that must never appear in committed ARM templates or rules
SECRET_PATTERNS = [
    (re.compile(r"/subscriptions/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I), "hardcoded Azure subscription ID"),
    (re.compile(r"DefaultEndpointsProtocol=https;AccountName=", re.I), "storage connection string"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key material"),
    (re.compile(r"\b(?:ghp|gho|github_pat)_[A-Za-z0-9_]{20,}\b"), "GitHub token"),
]


class Validator:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.stats: dict[str, int] = {}

    def error(self, ctx: str, msg: str) -> None:
        self.errors.append(f"ERROR [{ctx}]: {msg}")

    def warn(self, ctx: str, msg: str) -> None:
        self.warnings.append(f"WARN  [{ctx}]: {msg}")

    def load_yaml(self, path: Path) -> Any:
        text = path.read_text(encoding="utf-8")
        if yaml is not None:
            return yaml.safe_load(text)
        if shutil.which("yq"):
            out = subprocess.check_output(["yq", "-o=json", ".", str(path)], text=True)
            return json.loads(out)
        raise RuntimeError("Neither PyYAML nor yq is available to parse YAML files.")

    def check_uuid(self, ctx: str, val: Any) -> bool:
        if not isinstance(val, str):
            self.error(ctx, f"id must be a GUID string, got {type(val).__name__}")
            return False
        try:
            uuid.UUID(val)
            return True
        except ValueError:
            self.error(ctx, f"invalid GUID: {val!r}")
            return False

    def parse_yaml_duration_minutes(self, val: Any) -> int | None:
        if not isinstance(val, str):
            return None
        m = re.match(r"^(\d+)([mhd])$", val.strip())
        if not m:
            return None
        n, unit = int(m.group(1)), m.group(2)
        return n * {"m": 1, "h": 60, "d": 1440}[unit]

    def check_kql_syntax(self, ctx: str, query: str) -> None:
        if not isinstance(query, str) or not query.strip():
            self.error(ctx, "KQL query is empty")
            return
        # Remove // comments while preserving string literals
        paren = 0
        bracket = 0
        brace = 0
        i = 0
        n = len(query)
        in_str: str | None = None
        verbatim = False
        while i < n:
            ch = query[i]
            nxt = query[i + 1] if i + 1 < n else ""
            if in_str is None:
                # Line comment
                if ch == "/" and nxt == "/":
                    nl = query.find("\n", i)
                    i = n if nl == -1 else nl + 1
                    continue
                # Verbatim string @"..." or @'...'
                if ch == "@" and nxt in ('"', "'"):
                    in_str = nxt
                    verbatim = True
                    i += 2
                    continue
                if ch in ('"', "'"):
                    in_str = ch
                    verbatim = False
                    i += 1
                    continue
                if ch == "(":
                    paren += 1
                elif ch == ")":
                    paren -= 1
                    if paren < 0:
                        self.error(ctx, "unmatched closing ')' in KQL")
                        return
                elif ch == "[":
                    bracket += 1
                elif ch == "]":
                    bracket -= 1
                    if bracket < 0:
                        self.error(ctx, "unmatched closing ']' in KQL")
                        return
                elif ch == "{":
                    brace += 1
                elif ch == "}":
                    brace -= 1
                    if brace < 0:
                        self.error(ctx, "unmatched closing '}' in KQL")
                        return
            else:
                if verbatim:
                    if ch == in_str:
                        if nxt == in_str:
                            i += 2
                            continue
                        in_str = None
                        verbatim = False
                else:
                    if ch == "\\" and i + 1 < n:
                        i += 2
                        continue
                    if ch == in_str:
                        in_str = None
            i += 1

        if in_str is not None:
            self.error(ctx, f"unterminated {in_str} string literal in KQL")
        if paren != 0:
            self.error(ctx, f"unbalanced parentheses in KQL (delta={paren})")
        if bracket != 0:
            self.error(ctx, f"unbalanced brackets in KQL (delta={bracket})")
        if brace != 0:
            self.error(ctx, f"unbalanced braces in KQL (delta={brace})")

        non_comment = [l.strip() for l in query.splitlines() if l.strip() and not l.strip().startswith("//")]
        if not non_comment:
            self.error(ctx, "KQL query contains only comments")
        elif non_comment[0].startswith("|"):
            self.error(ctx, "KQL query starts with a leading pipe '|'")

    def check_secrets(self, ctx: str, text: str) -> None:
        for pat, label in SECRET_PATTERNS:
            if pat.search(text):
                self.error(ctx, f"potential {label} detected")

    def check_arm_expression(self, ctx: str, expr: str) -> None:
        if not (expr.startswith("[") and expr.endswith("]")):
            return
        if expr.startswith("[["):
            return
        body = expr[1:-1]
        paren = 0
        in_str = False
        i = 0
        while i < len(body):
            ch = body[i]
            if in_str:
                if ch == "'":
                    if i + 1 < len(body) and body[i + 1] == "'":
                        i += 2
                        continue
                    in_str = False
            else:
                if ch == "'":
                    in_str = True
                elif ch == "(":
                    paren += 1
                elif ch == ")":
                    paren -= 1
                    if paren < 0:
                        self.error(ctx, f"unbalanced ')' in ARM expression: {expr[:100]}")
                        return
            i += 1
        if in_str:
            self.error(ctx, f"unterminated string in ARM expression: {expr[:100]}")
        if paren != 0:
            self.error(ctx, f"unbalanced parentheses in ARM expression: {expr[:100]}")

    def validate_entity_mappings(self, ctx: str, mappings: Any, query: str) -> None:
        if mappings is None:
            return
        if not isinstance(mappings, list):
            self.error(ctx, "entityMappings must be a list")
            return
        if len(mappings) > 10:
            self.error(ctx, f"entityMappings exceeds max of 10 ({len(mappings)})")
        nc = "\n".join(l for l in query.splitlines() if not l.strip().startswith("//"))
        for idx, em in enumerate(mappings):
            etype = em.get("entityType")
            if etype not in VALID_SENTINEL_ENTITIES:
                self.error(ctx, f"entityMappings[{idx}] invalid entityType: {etype!r}")
                continue
            fms = em.get("fieldMappings")
            if not isinstance(fms, list) or not fms:
                self.error(ctx, f"entityMappings[{idx}] must have non-empty fieldMappings")
                continue
            if len(fms) > 3:
                self.error(ctx, f"entityMappings[{idx}] exceeds max 3 fieldMappings")
            for fm in fms:
                ident = fm.get("identifier")
                col = fm.get("columnName")
                if ident not in VALID_SENTINEL_ENTITIES[etype]:
                    self.error(ctx, f"entityMappings[{idx}] invalid identifier {ident!r} for {etype}")
                if not col or not isinstance(col, str):
                    self.error(ctx, f"entityMappings[{idx}] missing columnName")
                elif not re.search(rf"\b{re.escape(col)}\b", nc) and "| project " in nc:
                    self.error(ctx, f"entityMappings[{idx}] columnName {col!r} not found in query")

    def validate_solution(self) -> None:
        data_file = SOLUTION_DIR / "Data" / f"Solution_{SOLUTION_NAME}.json"
        meta_file = SOLUTION_DIR / "SolutionMetadata.json"
        mt_file = SOLUTION_DIR / "Package" / "mainTemplate.json"
        ui_file = SOLUTION_DIR / "Package" / "createUiDefinition.json"

        for f in (data_file, meta_file, mt_file, ui_file):
            if not f.exists():
                self.error(str(f.relative_to(ROOT)), "required solution file missing")
                return

        data = json.loads(data_file.read_text(encoding="utf-8"))
        meta = json.loads(meta_file.read_text(encoding="utf-8"))

        if data.get("Version") != meta.get("version"):
            self.error("SolutionVersion", f"Data Version ({data.get('Version')}) != SolutionMetadata version ({meta.get('version')})")

        for req in ("publisherId", "offerId", "firstPublishDate", "providers", "categories", "support", "version"):
            if req not in meta:
                self.error("SolutionMetadata.json", f"missing required key {req!r}")

        seen_ids: set[str] = set()

        # Validate Analytic Rules
        ar_files = sorted((SOLUTION_DIR / "Analytic Rules").glob("*.yaml"))
        manifest_ar = set(data.get("Analytic Rules", []))
        disk_ar = {f"Analytic Rules/{p.name}" for p in ar_files}
        if manifest_ar != disk_ar:
            self.error("Manifest", f"Analytic Rules mismatch: manifest={len(manifest_ar)} vs disk={len(disk_ar)}")

        for p in ar_files:
            ctx = str(p.relative_to(ROOT))
            self.check_secrets(ctx, p.read_text(encoding="utf-8"))
            doc = self.load_yaml(p)
            if not isinstance(doc, dict):
                self.error(ctx, "YAML root must be a mapping")
                continue
            for key in ("id", "name", "description", "severity", "requiredDataConnectors", "queryFrequency", "queryPeriod", "triggerOperator", "triggerThreshold", "tactics", "query", "version", "kind"):
                if key not in doc:
                    self.error(ctx, f"missing required field {key!r}")
            if self.check_uuid(ctx, doc.get("id")):
                if doc["id"] in seen_ids:
                    self.error(ctx, f"duplicate GUID: {doc['id']}")
                seen_ids.add(doc["id"])
            if doc.get("severity") not in VALID_SEVERITIES:
                self.error(ctx, f"invalid severity: {doc.get('severity')!r}")
            if doc.get("kind") != "Scheduled":
                self.error(ctx, f"invalid kind: {doc.get('kind')!r}")
            if doc.get("triggerOperator") not in VALID_TRIGGER_OPS:
                self.error(ctx, f"invalid triggerOperator: {doc.get('triggerOperator')!r}")
            if not isinstance(doc.get("triggerThreshold"), int) or doc["triggerThreshold"] < 0:
                self.error(ctx, f"invalid triggerThreshold: {doc.get('triggerThreshold')!r}")

            freq_m = self.parse_yaml_duration_minutes(doc.get("queryFrequency"))
            per_m = self.parse_yaml_duration_minutes(doc.get("queryPeriod"))
            if freq_m is None:
                self.error(ctx, f"invalid queryFrequency: {doc.get('queryFrequency')!r}")
            if per_m is None:
                self.error(ctx, f"invalid queryPeriod: {doc.get('queryPeriod')!r}")
            elif freq_m is not None:
                if per_m < freq_m:
                    self.error(ctx, f"queryPeriod ({doc['queryPeriod']}) < queryFrequency ({doc['queryFrequency']})")
                if per_m > 14 * 1440:
                    self.error(ctx, f"queryPeriod ({doc['queryPeriod']}) exceeds Sentinel 14d limit")

            rdc = doc.get("requiredDataConnectors")
            if not isinstance(rdc, list) or not rdc:
                self.error(ctx, "requiredDataConnectors must be a non-empty list")
            else:
                for c in rdc:
                    if not c.get("connectorId") or not c.get("dataTypes"):
                        self.error(ctx, f"invalid requiredDataConnectors entry: {c!r}")

            tactics = doc.get("tactics", [])
            if not isinstance(tactics, list) or not tactics:
                self.error(ctx, "tactics must be a non-empty list")
            for t in tactics:
                if t not in VALID_TACTICS:
                    self.error(ctx, f"invalid MITRE tactic: {t!r}")

            for tech in doc.get("relevantTechniques", []) or []:
                if not re.match(r"^T\d{4}(?:\.\d{3})?$", str(tech)):
                    self.error(ctx, f"invalid MITRE technique: {tech!r}")

            q = doc.get("query", "")
            self.check_kql_syntax(ctx, q)
            self.validate_entity_mappings(ctx, doc.get("entityMappings"), q)

        self.stats["analytic_rules"] = len(ar_files)

        # Validate Hunting Queries
        hq_files = sorted((SOLUTION_DIR / "Hunting Queries").glob("*.yaml"))
        manifest_hq = set(data.get("Hunting Queries", []))
        disk_hq = {f"Hunting Queries/{p.name}" for p in hq_files}
        if manifest_hq != disk_hq:
            self.error("Manifest", f"Hunting Queries mismatch: manifest={len(manifest_hq)} vs disk={len(disk_hq)}")

        for p in hq_files:
            ctx = str(p.relative_to(ROOT))
            self.check_secrets(ctx, p.read_text(encoding="utf-8"))
            doc = self.load_yaml(p)
            for key in ("id", "name", "description", "requiredDataConnectors", "tactics", "query", "version"):
                if key not in doc:
                    self.error(ctx, f"missing required field {key!r}")
            if self.check_uuid(ctx, doc.get("id")):
                if doc["id"] in seen_ids:
                    self.error(ctx, f"duplicate GUID: {doc['id']}")
                seen_ids.add(doc["id"])
            for t in doc.get("tactics", []) or []:
                if t not in VALID_TACTICS:
                    self.error(ctx, f"invalid MITRE tactic: {t!r}")
            q = doc.get("query", "")
            self.check_kql_syntax(ctx, q)
            self.validate_entity_mappings(ctx, doc.get("entityMappings"), q)

        self.stats["hunting_queries"] = len(hq_files)

        # Validate Workbooks
        wb_files = sorted((SOLUTION_DIR / "Workbooks").glob("*.json"))
        manifest_wb = set(data.get("Workbooks", []))
        disk_wb = {f"Workbooks/{p.name}" for p in wb_files}
        if manifest_wb != disk_wb:
            self.error("Manifest", f"Workbooks mismatch: manifest={len(manifest_wb)} vs disk={len(disk_wb)}")

        for p in wb_files:
            ctx = str(p.relative_to(ROOT))
            wb = json.loads(p.read_text(encoding="utf-8"))
            if wb.get("version") != "Notebook/1.0":
                self.error(ctx, f"expected Notebook/1.0, got {wb.get('version')!r}")
            items = wb.get("items", [])
            if not isinstance(items, list) or not items:
                self.error(ctx, "workbook must contain items")
            for idx, item in enumerate(items):
                if item.get("type") == 3:
                    q = item.get("content", {}).get("query", "")
                    self.check_kql_syntax(f"{ctx}:item[{idx}]", q)

        self.stats["workbooks"] = len(wb_files)

        # Validate ARM mainTemplate.json and createUiDefinition.json
        mt_text = mt_file.read_text(encoding="utf-8")
        self.check_secrets("Package/mainTemplate.json", mt_text)
        mt_size = mt_file.stat().st_size
        if mt_size >= 4 * 1024 * 1024:
            self.error("Package/mainTemplate.json", f"exceeds Azure ARM 4 MB template limit ({mt_size} bytes)")

        mt = json.loads(mt_text)
        if not str(mt.get("$schema", "")).startswith("https://schema.management.azure.com/schemas/"):
            self.error("Package/mainTemplate.json", f"invalid ARM $schema: {mt.get('$schema')!r}")
        for req_param in ("workspace", "workspace-location", "location"):
            if req_param not in mt.get("parameters", {}):
                self.error("Package/mainTemplate.json", f"missing required parameter {req_param!r}")
        for pname, pdef in mt.get("parameters", {}).items():
            if pdef.get("defaultValue") == "" and pdef.get("minLength", 0) > 0:
                self.error("Package/mainTemplate.json", f"parameter {pname!r} has empty defaultValue with minLength > 0")

        resources = mt.get("resources", [])
        if len(resources) > 800:
            self.error("Package/mainTemplate.json", f"exceeds Azure ARM 800 resource limit ({len(resources)})")

        pkg_count = sum(1 for r in resources if r.get("type") == "Microsoft.OperationalInsights/workspaces/providers/contentPackages")
        ar_tpl = sum(1 for r in resources if r.get("properties", {}).get("contentKind") == "AnalyticsRule")
        hq_tpl = sum(1 for r in resources if r.get("properties", {}).get("contentKind") == "HuntingQuery")
        wb_tpl = sum(1 for r in resources if r.get("properties", {}).get("contentKind") == "Workbook")

        if pkg_count != 1:
            self.error("Package/mainTemplate.json", f"expected 1 contentPackages resource, found {pkg_count}")
        if ar_tpl != len(ar_files):
            self.error("Package/mainTemplate.json", f"AnalyticsRule templates ({ar_tpl}) != YAML files ({len(ar_files)})")
        if hq_tpl != len(hq_files):
            self.error("Package/mainTemplate.json", f"HuntingQuery templates ({hq_tpl}) != YAML files ({len(hq_files)})")
        if wb_tpl != len(wb_files):
            self.error("Package/mainTemplate.json", f"Workbook templates ({wb_tpl}) != JSON files ({len(wb_files)})")

        # Recursively check ARM expressions in mainTemplate
        def walk_arm(obj: Any, path: str) -> None:
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k in ("query", "serializedData", "description", "descriptionHtml"):
                        continue
                    walk_arm(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for idx, v in enumerate(obj):
                    walk_arm(v, f"{path}[{idx}]")
            elif isinstance(obj, str) and obj.startswith("[") and obj.endswith("]"):
                self.check_arm_expression(path, obj)

        walk_arm(mt, "mainTemplate")

        # Validate createUiDefinition.json
        ui_text = ui_file.read_text(encoding="utf-8")
        self.check_secrets("Package/createUiDefinition.json", ui_text)
        ui = json.loads(ui_text)
        if ui.get("handler") != "Microsoft.Azure.CreateUIDef":
            self.error("Package/createUiDefinition.json", f"invalid handler: {ui.get('handler')!r}")
        ui_outputs = set(ui.get("parameters", {}).get("outputs", {}).keys())
        mt_params = set(mt.get("parameters", {}).keys())
        missing_in_ui = mt_params - ui_outputs
        extra_in_ui = ui_outputs - mt_params
        if missing_in_ui:
            self.error("Package/createUiDefinition.json", f"missing outputs for mainTemplate parameters: {sorted(missing_in_ui)}")
        if extra_in_ui:
            self.error("Package/createUiDefinition.json", f"outputs not present in mainTemplate parameters: {sorted(extra_in_ui)}")

        self.stats["arm_resources"] = len(resources)
        self.stats["arm_size_kb"] = int(round(mt_size / 1024))

    def validate_defender_xdr(self) -> None:
        rules_dir = XDR_DIR / "rules"
        hunts_dir = XDR_DIR / "hunting"
        if not rules_dir.exists():
            self.error("defender-xdr", "rules directory missing")
            return

        seen_ids: set[str] = set()
        rule_files = sorted(rules_dir.glob("*.yaml"))
        if not rule_files:
            self.error("defender-xdr/rules", "no Defender XDR rule definitions found")

        for p in rule_files:
            ctx = str(p.relative_to(ROOT))
            self.check_secrets(ctx, p.read_text(encoding="utf-8"))
            doc = self.load_yaml(p)
            for key in ("id", "displayName", "description", "severity", "frequency", "requiredTables", "tactics", "entityMappings", "query"):
                if key not in doc:
                    self.error(ctx, f"missing required field {key!r}")
            if self.check_uuid(ctx, doc.get("id")):
                if doc["id"] in seen_ids:
                    self.error(ctx, f"duplicate GUID: {doc['id']}")
                seen_ids.add(doc["id"])
            if doc.get("severity") not in VALID_SEVERITIES:
                self.error(ctx, f"invalid severity: {doc.get('severity')!r}")
            if doc.get("frequency") not in VALID_XDR_FREQUENCIES:
                self.error(ctx, f"invalid Defender XDR frequency: {doc.get('frequency')!r}")
            for t in doc.get("tactics", []) or []:
                if t not in VALID_TACTICS:
                    self.error(ctx, f"invalid MITRE tactic: {t!r}")

            q = doc.get("query", "")
            self.check_kql_syntax(ctx, q)
            nc = "\n".join(l for l in q.splitlines() if not l.strip().startswith("//"))
            if re.search(r"\bTimeGenerated\b", nc):
                self.error(ctx, "Defender XDR custom detection query must use Timestamp, not TimeGenerated")
            if not re.search(r"\bTimestamp\b", nc):
                self.error(ctx, "Defender XDR custom detection query must project Timestamp")
            if not re.search(r"\bReportId\b", nc):
                self.error(ctx, "Defender XDR custom detection query must project ReportId")
            tables = set(doc.get("requiredTables", []) or [])
            if tables & MDE_TABLES and not re.search(r"\bDeviceId\b", nc):
                self.error(ctx, "Defender for Endpoint Device* custom detection must project DeviceId")

            ems = doc.get("entityMappings", [])
            if not isinstance(ems, list) or not ems:
                self.error(ctx, "entityMappings must be non-empty")
            for idx, em in enumerate(ems):
                if em.get("entityType") not in VALID_XDR_ENTITIES:
                    self.error(ctx, f"entityMappings[{idx}] invalid entityType: {em.get('entityType')!r}")
                col = em.get("columnName", "")
                if not col or not re.search(rf"\b{re.escape(col)}\b", nc):
                    self.error(ctx, f"entityMappings[{idx}] columnName {col!r} not found in query")

        self.stats["xdr_rules"] = len(rule_files)

        hunt_files = sorted(hunts_dir.glob("*.kql")) if hunts_dir.exists() else []
        for p in hunt_files:
            ctx = str(p.relative_to(ROOT))
            q = p.read_text(encoding="utf-8")
            self.check_kql_syntax(ctx, q)
            nc = "\n".join(l for l in q.splitlines() if not l.strip().startswith("//"))
            if re.search(r"\bTimeGenerated\b", nc):
                self.error(ctx, "Defender XDR hunting query should use Timestamp, not TimeGenerated")
        self.stats["xdr_hunts"] = len(hunt_files)

    def validate_repo_kql_files(self) -> None:
        kql_files = sorted((ROOT / "queries").rglob("*.kql"))
        for p in kql_files:
            ctx = str(p.relative_to(ROOT))
            text = p.read_text(encoding="utf-8")
            self.check_secrets(ctx, text)
            self.check_kql_syntax(ctx, text)
        self.stats["query_pack_kql"] = len(kql_files)


def main() -> int:
    v = Validator()
    v.validate_solution()
    v.validate_defender_xdr()
    v.validate_repo_kql_files()

    for w in v.warnings:
        print(w)
    if v.errors:
        print(f"\nSentinel validation FAILED with {len(v.errors)} error(s):", file=sys.stderr)
        for e in v.errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print(
        "Sentinel validation PASSED:\n"
        f"  Analytic Rules YAML:  {v.stats.get('analytic_rules', 0)}\n"
        f"  Hunting Queries YAML: {v.stats.get('hunting_queries', 0)}\n"
        f"  Workbooks JSON:       {v.stats.get('workbooks', 0)}\n"
        f"  ARM template:         {v.stats.get('arm_resources', 0)} resources ({v.stats.get('arm_size_kb', 0)} KB)\n"
        f"  Defender XDR rules:   {v.stats.get('xdr_rules', 0)}\n"
        f"  Defender XDR hunts:   {v.stats.get('xdr_hunts', 0)}\n"
        f"  Query pack .kql:      {v.stats.get('query_pack_kql', 0)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
