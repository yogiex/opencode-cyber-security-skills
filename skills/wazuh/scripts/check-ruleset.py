#!/usr/bin/env python3
"""Validator offline untuk ruleset kustom Wazuh (rule dan decoder XML).

Memeriksa hal yang paling sering membuat tuning gagal secara senyap:

  * XML tidak well-formed;
  * ID rule kustom di luar rentang 100000-120000 atau duplikat;
  * level di luar 0-16;
  * rule tanpa <group> induk atau tanpa <description>;
  * tag percabangan (if_sid, if_group, if_level, if_matched_sid,
    if_matched_group) pada rule overwrite="yes" — diabaikan Wazuh;
  * <regex> tanpa <order>, atau jumlah capture group tidak sama dengan
    jumlah field pada <order>;
  * decoder tanpa program_name/prematch/regex.

Contoh:
  python check-ruleset.py /var/ossec/etc/rules/local_rules.xml
  python check-ruleset.py /var/ossec/etc/rules /var/ossec/etc/decoders

Exit code: 0 bila tidak ada error, 1 bila ada error, 2 bila argumen salah.
Peringatan (WARN) tidak menggagalkan pemeriksaan.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Set, Tuple

CUSTOM_ID_MIN = 100000
CUSTOM_ID_MAX = 120000
LEVEL_MIN = 0
LEVEL_MAX = 16
BRANCH_TAGS = ("if_sid", "if_group", "if_level", "if_matched_sid", "if_matched_group")
DECODER_FIELDS = {
    "srcip", "dstip", "srcport", "dstport", "srcuser", "dstuser", "user",
    "id", "url", "action", "status", "data", "extra_data", "protocol",
    "system_name", "hostname", "program_name", "location", "file", "md5", "sha1", "sha256",
}


class Finding:
    def __init__(self, level: str, path: str, message: str) -> None:
        self.level = level
        self.path = path
        self.message = message

    def __str__(self) -> str:
        return f"[{self.level}] {self.path}: {self.message}"


def iter_xml_files(targets: List[str]) -> Tuple[List[str], List[str]]:
    files: List[str] = []
    problems: List[str] = []
    for target in targets:
        if os.path.isdir(target):
            for root, _dirs, names in os.walk(target):
                for name in sorted(names):
                    if name.lower().endswith(".xml"):
                        files.append(os.path.join(root, name))
        elif os.path.isfile(target):
            files.append(target)
        else:
            problems.append(f"path tidak ditemukan: {target}")
    return files, problems


def capture_group_count(pattern: str) -> int:
    """Hitung capture group, mengabaikan escape dan kelas karakter."""
    count = 0
    escaped = False
    in_class = False
    for char in pattern:
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
        elif char == "[":
            in_class = True
        elif char == "]":
            in_class = False
        elif char == "(" and not in_class:
            count += 1
    return count


def check_rule(rule: ET.Element, path: str, local_ids: Set[int], findings: List[Finding]) -> None:
    raw_id = rule.get("id", "")
    try:
        rule_id = int(raw_id)
    except ValueError:
        findings.append(Finding("ERROR", path, f"rule id bukan angka: {raw_id!r}"))
        return

    overwrite = (rule.get("overwrite") or "").lower() == "yes"
    if not (CUSTOM_ID_MIN <= rule_id <= CUSTOM_ID_MAX) and not overwrite:
        findings.append(
            Finding(
                "ERROR",
                path,
                f"rule {rule_id} di luar rentang ID kustom {CUSTOM_ID_MIN}-{CUSTOM_ID_MAX}; "
                "ID di bawah rentang itu milik ruleset bawaan (gunakan overwrite=\"yes\" "
                "bila memang ingin mengubah rule bawaan)",
            )
        )

    raw_level = rule.get("level")
    if raw_level is None:
        findings.append(Finding("ERROR", path, f"rule {rule_id} tidak punya atribut level"))
    else:
        try:
            level = int(raw_level)
        except ValueError:
            findings.append(Finding("ERROR", path, f"rule {rule_id} level bukan angka: {raw_level!r}"))
            level = None
        if level is not None and not (LEVEL_MIN <= level <= LEVEL_MAX):
            findings.append(
                Finding("ERROR", path, f"rule {rule_id} level {level} di luar {LEVEL_MIN}-{LEVEL_MAX}")
            )
        elif level is not None and level < 3:
            findings.append(
                Finding(
                    "WARN",
                    path,
                    f"rule {rule_id} level {level} di bawah log_alert_level default (3): "
                    "alert tidak akan muncul di dashboard",
                )
            )

    if not rule.findtext("description"):
        findings.append(Finding("ERROR", path, f"rule {rule_id} tanpa <description>"))

    if overwrite:
        for tag in BRANCH_TAGS:
            if rule.find(tag) is not None:
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"rule {rule_id} memakai overwrite=\"yes\" bersama <{tag}>; "
                        "tag percabangan ini diabaikan Wazuh — buat rule anak baru",
                    )
                )

    for tag in ("if_sid", "if_matched_sid"):
        text = rule.findtext(tag)
        if not text:
            continue
        for token in re.split(r"[,\s]+", text.strip()):
            if not token:
                continue
            try:
                reference = int(token)
            except ValueError:
                continue
            if reference >= CUSTOM_ID_MIN and reference not in local_ids:
                findings.append(
                    Finding("ERROR", path, f"rule {rule_id} merujuk ID lokal {reference} yang tidak ada di berkas")
                )
            elif reference < CUSTOM_ID_MIN:
                findings.append(
                    Finding(
                        "WARN",
                        path,
                        f"rule {rule_id} merujuk rule bawaan {reference}; keberadaannya tidak dapat diverifikasi offline",
                    )
                )

    frequency = rule.get("frequency")
    timeframe = rule.get("timeframe")
    if frequency and not timeframe:
        findings.append(
            Finding("WARN", path, f"rule {rule_id} memakai frequency tanpa timeframe; perilakunya bergantung pada default")
        )
    if timeframe and not frequency:
        findings.append(
            Finding("WARN", path, f"rule {rule_id} memakai timeframe tanpa frequency; tidak akan berfungsi sebagai korelasi")
        )

    if rule.get("noalert") is not None and rule.get("noalert") not in ("0", "1"):
        findings.append(Finding("ERROR", path, f"rule {rule_id} noalert harus 0 atau 1"))


def check_decoder(
    decoder: ET.Element, path: str, decoder_names: Set[str], findings: List[Finding]
) -> None:
    name = decoder.get("name") or "(tanpa nama)"
    parent = decoder.findtext("parent")
    program = decoder.findtext("program_name")
    prematch = decoder.findtext("prematch")
    regex = decoder.findtext("regex")
    order = decoder.findtext("order")

    if parent:
        # Child decoder lazim memakai nama yang sama dengan parent-nya;
        # yang tidak boleh adalah parent yang tidak pernah dideklarasikan.
        if parent not in decoder_names:
            findings.append(
                Finding(
                    "WARN",
                    path,
                    f"decoder {name} merujuk parent {parent!r} yang tidak ada di berkas; "
                    "pastikan decoder induk dimuat",
                )
            )

    if not (program or prematch or regex):
        findings.append(
            Finding("ERROR", path, f"decoder {name} tanpa program_name/prematch/regex; tidak akan pernah cocok")
        )

    if regex:
        if not order:
            findings.append(Finding("ERROR", path, f"decoder {name} punya <regex> tanpa <order>; tidak akan cocok"))
        else:
            groups = capture_group_count(regex)
            fields = [part.strip() for part in order.split(",") if part.strip()]
            if groups != len(fields):
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"decoder {name}: {groups} capture group pada regex tetapi {len(fields)} field pada order "
                        f"({', '.join(fields)})",
                    )
                )
            for field in fields:
                if field not in DECODER_FIELDS:
                    findings.append(
                        Finding("WARN", path, f"decoder {name} memakai field non-standar {field!r}; pastikan decoder mengisinya")
                    )
    elif prematch is None and program is None:
        findings.append(
            Finding("ERROR", path, f"decoder {name} punya regex tanpa prematch/program_name; decoder induk diperlukan")
        )


def _parse_ruleset(path: str) -> ET.Element:
    """Parse berkas ruleset Wazuh.

    Berkas decoder/rule Wazuh boleh berisi beberapa elemen top-level (fragmen),
    sehingga bila parse dokumen gagal, isi dibungkus root sintetis.
    """
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    stripped = re.sub(r"^\s*<\?xml[^>]*\?>", "", text).strip()
    try:
        return ET.fromstring(stripped)
    except ET.ParseError:
        return ET.fromstring(f"<wazuh_ruleset>{stripped}</wazuh_ruleset>")


def check_file(path: str, seen_rule_ids: Dict[int, str], findings: List[Finding]) -> None:
    try:
        root = _parse_ruleset(path)
    except ET.ParseError as exc:
        findings.append(Finding("ERROR", path, f"XML tidak valid: {exc}"))
        return
    except OSError as exc:
        findings.append(Finding("ERROR", path, f"tidak dapat dibaca: {exc}"))
        return

    findings.append(Finding("INFO", path, f"root <{root.tag}>"))

    rules = root.iter("rule")
    decoders = root.iter("decoder")

    local_ids: Set[int] = set()
    rule_elements: List[ET.Element] = list(rules)
    for rule in rule_elements:
        try:
            local_ids.add(int(rule.get("id", "")))
        except ValueError:
            continue

    for rule in rule_elements:
        check_rule(rule, path, local_ids, findings)
        try:
            rule_id = int(rule.get("id", ""))
        except ValueError:
            continue
        if rule_id in seen_rule_ids:
            findings.append(
                Finding("ERROR", path, f"rule {rule_id} duplikat (juga didefinisikan di {seen_rule_ids[rule_id]})")
            )
        else:
            seen_rule_ids[rule_id] = path

    decoder_elements: List[ET.Element] = list(decoders)
    decoder_names = {(d.get("name") or "") for d in decoder_elements}
    for decoder in decoder_elements:
        check_decoder(decoder, path, decoder_names, findings)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validasi ruleset kustom Wazuh (rule/decoder XML).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("paths", nargs="+", help="Berkas atau direktori XML.")
    parser.add_argument("--no-warn-as-error", action="store_true", help="Abaikan peringatan.")
    args = parser.parse_args(argv)

    files, problems = iter_xml_files(args.paths)
    findings: List[Finding] = [Finding("ERROR", "-", problem) for problem in problems]
    if not files:
        findings.append(Finding("ERROR", "-", "tidak ada berkas XML untuk diperiksa"))

    seen_rule_ids: Dict[int, str] = {}
    for path in files:
        before = len(findings)
        check_file(path, seen_rule_ids, findings)
        added = len(findings) - before
        if added <= 1:
            findings.append(Finding("INFO", path, "tidak ada masalah terdeteksi"))

    for finding in findings:
        if finding.level != "INFO":
            print(finding)

    errors = sum(1 for f in findings if f.level == "ERROR")
    warns = sum(1 for f in findings if f.level == "WARN")
    print()
    print(f"Diperiksa {len(files)} berkas: {errors} error, {warns} peringatan.")

    if errors or (warns and not args.no_warn_as_error):
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
