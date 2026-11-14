#!/usr/bin/env python3
"""Penarik alert Wazuh dari indexer dan pembentuk antrean/laporan triase.

Hanya memakai pustaka standar Python 3.8+.

Konfigurasi lewat variabel lingkungan:
  WAZUH_INDEXER_URL   default https://127.0.0.1:9200
  WAZUH_INDEXER_USER  wajib (default admin pada deployment installer Wazuh)
  WAZUH_INDEXER_PASS  wajib
  WAZUH_INDEXER_VERIFY 1 (default) atau 0 untuk sertifikat self-signed
  WAZUH_ALERTS_INDEX  default wazuh-alerts-*

Contoh:
  python wazuh_triage.py queue --since 24h --min-level 8
  python wazuh_triage.py timeline --agent 003 --since 6h
  python wazuh_triage.py report --alert 1684401234.12345 --out triage-003.md
  python wazuh_triage.py queue --since 24h --dry-run

--dry-run mencetak kueri yang akan dijalankan tanpa menghubungi indexer, sehingga
aman dipakai untuk menyusun kueri terlebih dahulu.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_URL = "https://127.0.0.1:9200"
DEFAULT_INDEX = "wazuh-alerts-*"
TEMPLATE_RELATIVE = os.path.join("..", "assets", "triage-report-template.md")
SCHEMA_RELATIVE = os.path.join("..", "assets", "triage-report.schema.json")


class TriageError(RuntimeError):
    pass


# -- util ------------------------------------------------------------------
def parse_duration(value: str) -> timedelta:
    match = re.fullmatch(r"\s*(\d+)\s*([smhdw])\s*", value)
    if not match:
        raise TriageError(
            f"Durasi tidak dikenal: {value!r}. Gunakan bentuk seperti 30m, 24h, 7d."
        )
    amount = int(match.group(1))
    unit = match.group(2)
    return {
        "s": timedelta(seconds=amount),
        "m": timedelta(minutes=amount),
        "h": timedelta(hours=amount),
        "d": timedelta(days=amount),
        "w": timedelta(weeks=amount),
    }[unit]


def iso_utc(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Indexer:
    def __init__(self, url: str, user: Optional[str], password: Optional[str], verify: bool, timeout: int = 30) -> None:
        self.url = url.rstrip("/")
        self.user = user
        self.password = password
        self.verify = verify
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.user is not None and self.password is not None:
            raw = f"{self.user}:{self.password}".encode("utf-8")
            headers["Authorization"] = "Basic " + base64.b64encode(raw).decode("ascii")
        return headers

    def _context(self) -> Optional[ssl.SSLContext]:
        if self.verify:
            return None
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def search(self, index: str, body: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.url}/{urllib.parse.quote(index, safe='*,-_.')}/_search"
        data = json.dumps(body).encode("utf-8")
        request = urllib.request.Request(url, data=data, headers=self._headers(), method="POST")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout, context=self._context()) as resp:
                return json.loads(resp.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:400]
            raise TriageError(f"Indexer HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise TriageError(f"Tidak dapat menghubungi {self.url}: {exc.reason}") from exc


def _hits(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    return ((response.get("hits") or {}).get("hits")) or []


def _source(hit: Dict[str, Any]) -> Dict[str, Any]:
    return hit.get("_source") or {}


def _dig(obj: Any, dotted: str) -> Any:
    current = obj
    for part in dotted.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


# -- kueri -----------------------------------------------------------------
def build_queue_query(since: datetime, min_level: int, agent: Optional[str], rule: Optional[str], size: int) -> Dict[str, Any]:
    filters: List[Dict[str, Any]] = [
        {"range": {"@timestamp": {"gte": iso_utc(since)}}},
        {"range": {"rule.level": {"gte": min_level}}},
    ]
    if agent:
        filters.append({"term": {"agent.id": agent}})
    if rule:
        filters.append({"term": {"rule.id": rule}})

    return {
        "size": 0,
        "query": {"bool": {"filter": filters}},
        "aggs": {
            "per_rule": {
                "terms": {"field": "rule.id", "size": size},
                "aggs": {
                    "level": {"max": {"field": "rule.level"}},
                    "agents": {"cardinality": {"field": "agent.id"}},
                    "sample": {"top_hits": {"size": 1, "_source": ["rule.description", "agent.name"]}},
                },
            }
        },
    }


def build_timeline_query(since: datetime, agent: Optional[str], min_level: int, size: int) -> Dict[str, Any]:
    filters: List[Dict[str, Any]] = [
        {"range": {"@timestamp": {"gte": iso_utc(since)}}},
        {"range": {"rule.level": {"gte": min_level}}},
    ]
    if agent:
        filters.append({"term": {"agent.id": agent}})
    return {
        "size": size,
        "sort": [{"timestamp": {"order": "asc"}}],
        "query": {"bool": {"filter": filters}},
        "_source": ["timestamp", "rule.id", "rule.level", "rule.description", "agent.id", "agent.name", "location", "data.srcip"],
    }


def build_report_query(alert_id: str) -> Dict[str, Any]:
    return {"size": 1, "query": {"ids": {"values": [alert_id]}}}


# -- keluaran --------------------------------------------------------------
def print_queue(response: Dict[str, Any], since: datetime, min_level: int) -> None:
    buckets = ((response.get("aggregations") or {}).get("per_rule") or {}).get("buckets") or []
    if not buckets:
        print("(tidak ada alert pada rentang dan filter ini)")
        return

    print(f"Antrean triase — sejak {iso_utc(since)}, level >= {min_level}")
    print()
    print(f"{'Rule':<8}{'Level':<7}{'Jumlah':<8}{'Agent':<8}Deskripsi")
    print("-" * 96)
    for bucket in buckets:
        hits = (((bucket.get("sample") or {}).get("hits") or {}).get("hits")) or []
        source = _source(hits[0]) if hits else {}
        description = _dig(source, "rule.description") or "?"
        level = (bucket.get("level") or {}).get("value")
        level_text = str(int(level)) if isinstance(level, (int, float)) else "?"
        agents = (bucket.get("agents") or {}).get("value", "?")
        print(f"{bucket.get('key', '?'):<8}{level_text:<7}{bucket.get('doc_count', 0):<8}{agents:<8}{description[:60]}")
    print()
    print("Langkah berikutnya: untuk tiap baris, buka sampel alert lalu jalankan "
          "`timeline --agent <id>` dan `report --alert <_id>`.")


def print_timeline(response: Dict[str, Any]) -> None:
    hits = _hits(response)
    if not hits:
        print("(tidak ada event pada rentang ini)")
        return
    for hit in hits:
        source = _source(hit)
        timestamp = source.get("timestamp") or hit.get("sort", [None])[0] or "?"
        rule = source.get("rule") or {}
        agent = source.get("agent") or {}
        srcip = _dig(source, "data.srcip")
        parts = [
            str(timestamp),
            f"agent={agent.get('id', '?')}/{agent.get('name', '?')}",
            f"rule={rule.get('id', '?')}",
            f"level={rule.get('level', '?')}",
        ]
        if srcip:
            parts.append(f"srcip={srcip}")
        parts.append(str(rule.get("description", ""))[:70])
        print("  ".join(parts))


def build_report_markdown(alert_id: str, source: Dict[str, Any], template_text: Optional[str]) -> Dict[str, Any]:
    rule = source.get("rule") or {}
    agent = source.get("agent") or {}
    mitre = rule.get("mitre") or {}
    mitre_ids = mitre.get("id") or []
    if isinstance(mitre_ids, str):
        mitre_ids = [mitre_ids]

    report = {
        "alert_id": alert_id,
        "rule_id": str(rule.get("id", "")),
        "rule_level": int(rule.get("level", 0) or 0),
        "rule_description": rule.get("description", ""),
        "agent_id": str(agent.get("id", "")),
        "agent_name": agent.get("name", ""),
        "timestamp": source.get("timestamp", ""),
        "location": source.get("location", ""),
        "decoder": _dig(source, "decoder.name") or "",
        "mitre": mitre_ids,
        "full_log": source.get("full_log", ""),
        "verdict": "Unknown",
        "priority": "",
        "evidence": [],
        "actions": [],
    }

    if template_text:
        rendered = template_text
        for key, value in (
            ("{{alert_id}}", report["alert_id"]),
            ("{{rule_id}}", report["rule_id"]),
            ("{{rule_level}}", str(report["rule_level"])),
            ("{{rule_description}}", report["rule_description"]),
            ("{{agent_id}}", report["agent_id"]),
            ("{{agent_name}}", report["agent_name"]),
            ("{{timestamp}}", report["timestamp"]),
            ("{{location}}", report["location"]),
            ("{{decoder}}", report["decoder"]),
            ("{{mitre}}", ", ".join(mitre_ids) if mitre_ids else "rule tidak memetakan ATT&CK"),
            ("{{full_log}}", report["full_log"]),
        ):
            rendered = rendered.replace(key, str(value))
        report["markdown"] = rendered
    else:
        report["markdown"] = (
            f"# Triage — {report['rule_id']} pada {report['agent_name']}\n\n"
            f"- Alert: {report['alert_id']}\n- Agent: {report['agent_id']}\n"
            f"- Waktu: {report['timestamp']}\n- Verdict: {report['verdict']}\n"
        )
    return report


def validate_report(report: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    problems: List[str] = []
    for required in schema.get("required", []):
        if required not in report:
            problems.append(f"field wajib hilang: {required}")

    type_map = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "array": list,
        "object": dict,
        "boolean": bool,
    }
    for key, spec in (schema.get("properties") or {}).items():
        if key not in report:
            continue
        expected = spec.get("type")
        if expected in type_map and not isinstance(report[key], type_map[expected]):
            problems.append(f"tipe field salah: {key} harus {expected}")
    return problems


# -- CLI -------------------------------------------------------------------
def add_common_sub_flags(parser: argparse.ArgumentParser) -> None:
    """Izinkan --dry-run/--json juga ditulis setelah subcommand."""
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Cetak kueri tanpa menghubungi indexer.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Keluarkan JSON mentah.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Antrean, timeline, dan laporan triase dari indexer Wazuh.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--url", default=os.environ.get("WAZUH_INDEXER_URL", DEFAULT_URL))
    parser.add_argument("--user", default=os.environ.get("WAZUH_INDEXER_USER"))
    parser.add_argument("--password", default=os.environ.get("WAZUH_INDEXER_PASS"))
    parser.add_argument(
        "--verify",
        choices=["on", "off"],
        default="on" if os.environ.get("WAZUH_INDEXER_VERIFY", "1") not in ("0", "false", "off") else "off",
    )
    parser.add_argument("--index", default=os.environ.get("WAZUH_ALERTS_INDEX", DEFAULT_INDEX))
    parser.add_argument("--dry-run", action="store_true", help="Cetak kueri tanpa menghubungi indexer.")
    parser.add_argument("--json", action="store_true", help="Keluarkan JSON mentah.")

    sub = parser.add_subparsers(dest="command", required=True)

    p_queue = sub.add_parser("queue", help="Antrean alert dikelompokkan per rule.")
    add_common_sub_flags(p_queue)
    p_queue.add_argument("--since", default="24h")
    p_queue.add_argument("--min-level", type=int, default=8)
    p_queue.add_argument("--agent")
    p_queue.add_argument("--rule")
    p_queue.add_argument("--size", type=int, default=25)

    p_timeline = sub.add_parser("timeline", help="Timeline event satu agent.")
    add_common_sub_flags(p_timeline)
    p_timeline.add_argument("--since", default="6h")
    p_timeline.add_argument("--agent")
    p_timeline.add_argument("--min-level", type=int, default=0)
    p_timeline.add_argument("--size", type=int, default=100)

    p_report = sub.add_parser("report", help="Bentuk laporan triase untuk satu alert.")
    add_common_sub_flags(p_report)
    p_report.add_argument("--alert", required=True, help="ID dokumen alert (_id).")
    p_report.add_argument("--out", help="Simpan markdown ke berkas.")
    p_report.add_argument("--out-json", help="Simpan JSON tervalidasi ke berkas.")

    return parser


def _indexer_from_args(args: argparse.Namespace) -> Indexer:
    if args.user is None or args.password is None:
        raise TriageError(
            "WAZUH_INDEXER_USER dan WAZUH_INDEXER_PASS wajib diisi untuk menghubungi indexer."
        )
    return Indexer(args.url, args.user, args.password, args.verify == "on")


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    since = datetime.now(timezone.utc) - parse_duration(getattr(args, "since", "0s"))

    try:
        if args.command == "queue":
            body = build_queue_query(since, args.min_level, args.agent, args.rule, args.size)
            if args.dry_run:
                print(json.dumps(body, indent=2, ensure_ascii=False))
                return 0
            response = _indexer_from_args(args).search(args.index, body)
            if args.json:
                print(json.dumps(response, indent=2, ensure_ascii=False))
            else:
                print_queue(response, since, args.min_level)

        elif args.command == "timeline":
            body = build_timeline_query(since, args.agent, args.min_level, args.size)
            if args.dry_run:
                print(json.dumps(body, indent=2, ensure_ascii=False))
                return 0
            response = _indexer_from_args(args).search(args.index, body)
            if args.json:
                print(json.dumps(response, indent=2, ensure_ascii=False))
            else:
                print_timeline(response)

        elif args.command == "report":
            body = build_report_query(args.alert)
            if args.dry_run:
                print(json.dumps(body, indent=2, ensure_ascii=False))
                return 0
            response = _indexer_from_args(args).search(args.index, body)
            hits = _hits(response)
            if not hits:
                raise TriageError(f"Alert {args.alert} tidak ditemukan pada indeks {args.index}.")

            template_text = _read_optional(os.path.join(os.path.dirname(__file__), TEMPLATE_RELATIVE))
            report = build_report_markdown(args.alert, _source(hits[0]), template_text)

            schema = _load_schema()
            problems = validate_report(report, schema)
            if problems:
                for problem in problems:
                    print(f"PERINGATAN skema: {problem}", file=sys.stderr)

            if args.out:
                _write_text(args.out, report["markdown"])
                print(f"Laporan ditulis ke {args.out}")
            else:
                print(report["markdown"])

            if args.out_json:
                payload = {k: v for k, v in report.items() if k != "markdown"}
                _write_text(args.out_json, json.dumps(payload, indent=2, ensure_ascii=False))
                print(f"JSON ditulis ke {args.out_json}")
            if problems:
                return 1

        else:  # pragma: no cover
            raise TriageError("perintah tidak dikenal")
        return 0

    except TriageError as exc:
        print(f"Kesalahan: {exc}", file=sys.stderr)
        return 2


def _read_optional(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return None


def _load_schema() -> Dict[str, Any]:
    path = os.path.join(os.path.dirname(__file__), SCHEMA_RELATIVE)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return {"required": [], "properties": {}}


def _write_text(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text if text.endswith("\n") else text + "\n")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
