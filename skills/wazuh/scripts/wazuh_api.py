#!/usr/bin/env python3
"""Klien Wazuh API untuk triage alert SOC (read-only secara default).

Hanya memakai pustaka standar Python 3.8+ sehingga dapat dijalankan langsung di
server Wazuh tanpa memasang dependensi tambahan.

Konfigurasi lewat variabel lingkungan:
  WAZUH_API_URL     default https://127.0.0.1:55000
  WAZUH_API_USER    wajib untuk perintah yang memanggil API
  WAZUH_API_PASS    wajib untuk perintah yang memanggil API
  WAZUH_API_VERIFY  1 (default) untuk memverifikasi TLS, 0 untuk sertifikat self-signed

Contoh:
  python wazuh_api.py agents --q "status=active" --limit 50
  python wazuh_api.py agent 003
  python wazuh_api.py logs --search 100200
  python wazuh_api.py restart --apply --yes

Perintah yang mengubah keadaan (restart, active-response) menolak berjalan tanpa
flag --apply dan --yes. Kredensial tidak pernah ditulis ke disk atau ke keluaran.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_URL = "https://127.0.0.1:55000"
DEFAULT_TIMEOUT = 30


class ConfigError(RuntimeError):
    """Kesalahan konfigurasi atau penggunaan, bukan kesalahan API."""


class ApiError(RuntimeError):
    """Respons API non-2xx atau error != 0 yang tidak bisa diabaikan."""

    def __init__(self, message: str, status: Optional[int] = None) -> None:
        super().__init__(message)
        self.status = status


class WazuhApi:
    def __init__(
        self,
        base_url: str,
        user: Optional[str],
        password: Optional[str],
        verify: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.user = user
        self.password = password
        self.verify = verify
        self.timeout = timeout
        self._token: Optional[str] = None

    # -- transport ---------------------------------------------------------
    def _ssl_context(self) -> Optional[ssl.SSLContext]:
        if self.verify:
            return None
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    def _open(self, request: urllib.request.Request) -> Tuple[int, bytes]:
        try:
            with urllib.request.urlopen(
                request, timeout=self.timeout, context=self._ssl_context()
            ) as response:
                return response.getcode(), response.read()
        except urllib.error.HTTPError as exc:
            body = exc.read()
            raise ApiError(_describe_error(exc.code, body), status=exc.code) from exc
        except urllib.error.URLError as exc:
            raise ApiError(
                f"Tidak dapat menghubungi {self.base_url}: {exc.reason}"
            ) from exc

    def authenticate(self, force: bool = False) -> str:
        if self._token and not force:
            return self._token

        if not self.user or not self.password:
            raise ConfigError(
                "WAZUH_API_USER dan WAZUH_API_PASS wajib diisi untuk memanggil API."
            )

        credentials = f"{self.user}:{self.password}".encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/security/user/authenticate?raw=true",
            method="POST",
            headers={
                "Authorization": "Basic "
                + base64.b64encode(credentials).decode("ascii"),
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        _, body = self._open(request)
        token = body.decode("utf-8", "replace").strip()
        if not token:
            raise ApiError("Autentikasi berhasil secara HTTP tetapi token kosong.")
        self._token = token
        return token

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        if params:
            clean = {k: v for k, v in params.items() if v is not None}
            if clean:
                url = f"{url}?{urllib.parse.urlencode(clean)}"

        data = None
        headers = {"Accept": "application/json"}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        for attempt in (0, 1):
            token = self.authenticate(force=bool(attempt))
            headers["Authorization"] = f"Bearer {token}"
            request = urllib.request.Request(
                url, method=method, headers=headers, data=data
            )
            try:
                status, body = self._open(request)
            except ApiError as exc:
                if exc.status == 401 and attempt == 0:
                    continue  # token kedaluwarsa: login ulang sekali
                raise
            return _parse_response(status, body)

        raise ApiError("Gagal terautentikasi ke Wazuh API.")  # pragma: no cover

    # -- perintah ----------------------------------------------------------
    def agents(self, query: Optional[str], limit: int, select: Optional[str]) -> Dict[str, Any]:
        return self.request(
            "GET",
            "/agents",
            params={"q": query, "limit": limit, "select": select, "sort": "id"},
        )

    def agent(self, agent_id: str) -> Dict[str, Any]:
        return self.request("GET", f"/agents/{agent_id}")

    def collect_agent_context(self, agent_id: str) -> Dict[str, Any]:
        """Kumpulkan konteks triage; kegagalan satu bagian tidak menggagalkan semua."""
        sections = {
            "agent": ("GET", f"/agents/{agent_id}", None),
            "os": ("GET", f"/syscollector/{agent_id}/os", None),
            "processes": ("GET", f"/syscollector/{agent_id}/processes", None),
            "ports": ("GET", f"/syscollector/{agent_id}/ports", None),
            "packages": ("GET", f"/syscollector/{agent_id}/packages", None),
            "syscheck_last_scan": ("GET", f"/syscheck/{agent_id}/last_scan", None),
            "sca": ("GET", f"/sca/{agent_id}", None),
        }
        result: Dict[str, Any] = {}
        for name, (method, path, params) in sections.items():
            try:
                result[name] = {"ok": True, "data": self.request(method, path, params)}
            except ApiError as exc:
                result[name] = {"ok": False, "error": str(exc)}
        return result

    def logs(self, search: Optional[str], level: Optional[str], limit: int) -> Dict[str, Any]:
        return self.request(
            "GET",
            "/manager/logs",
            params={"search": search, "level": level, "limit": limit, "sort": "-timestamp"},
        )

    def status(self) -> Dict[str, Any]:
        return self.request("GET", "/manager/status")

    def rules(self, search: Optional[str], limit: int) -> Dict[str, Any]:
        return self.request("GET", "/rules", params={"search": search, "limit": limit})

    def restart(self) -> Dict[str, Any]:
        return self.request("PUT", "/manager/restart")

    def active_response(
        self, command: str, arguments: List[str], agent_id: Optional[str]
    ) -> Dict[str, Any]:
        alert: Dict[str, Any] = {"data": {}}
        if agent_id:
            alert["agent"] = {"id": agent_id}
        payload = {"command": command, "arguments": arguments, "alert": alert}
        return self.request("PUT", "/active-response", payload=payload)


# -- util ------------------------------------------------------------------
def _describe_error(status: int, body: bytes) -> str:
    text = body.decode("utf-8", "replace").strip()
    detail = ""
    try:
        parsed = json.loads(text)
        detail = parsed.get("detail") or parsed.get("message") or ""
        code = parsed.get("error")
        if code and not detail:
            detail = f"error {code}"
    except (ValueError, AttributeError):
        detail = text[:300]

    hints = {
        401: "Token/kredensial tidak valid atau kedaluwarsa (token default 900 detik).",
        403: "Token valid tetapi RBAC kurang, atau IP diblokir.",
        404: "Endpoint tidak ada pada versi ini.",
    }
    hint = hints.get(status, "")
    suffix = f" — {hint}" if hint else ""
    return f"HTTP {status}: {detail or 'tanpa detail'}{suffix}"


def _parse_response(status: int, body: bytes) -> Dict[str, Any]:
    text = body.decode("utf-8", "replace").strip()
    if not text:
        return {"data": {}, "error": 0, "message": "respons kosong"}
    try:
        parsed = json.loads(text)
    except ValueError as exc:
        raise ApiError(f"Respons bukan JSON (HTTP {status}): {text[:200]}") from exc

    error = parsed.get("error", 0)
    if error == 2:
        failed = parsed.get("data", {}).get("total_failed_items", 0)
        print(
            f"PERINGATAN: respons parsial (error=2, {failed} item gagal). "
            "Periksa data.failed_items sebelum menyimpulkan kelengkapan.",
            file=sys.stderr,
        )
    elif error not in (0, None):
        raise ApiError(
            f"API mengembalikan error={error}: {parsed.get('message', '')}".strip()
        )
    return parsed


def _items(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    data = response.get("data") or {}
    items = data.get("affected_items")
    if isinstance(items, list):
        return items
    if isinstance(items, dict):
        return [items]
    return []


def _print_table(rows: List[Dict[str, Any]], columns: List[Tuple[str, str]]) -> None:
    if not rows:
        print("(tidak ada data)")
        return
    widths = {key: len(title) for key, title in columns}
    formatted: List[List[str]] = []
    for row in rows:
        line = []
        for key, _ in columns:
            value = _dig(row, key)
            text = "-" if value in (None, "") else str(value)
            line.append(text)
            widths[key] = max(widths[key], len(text))
        formatted.append(line)

    header = "  ".join(title.ljust(widths[key]) for key, title in columns)
    print(header)
    print("  ".join("-" * widths[key] for key, _ in columns))
    for line in formatted:
        print("  ".join(text.ljust(widths[key]) for text, (key, _) in zip(line, columns)))


def _dig(obj: Any, dotted: str) -> Any:
    current = obj
    for part in dotted.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def _json_or_table(
    response: Dict[str, Any], rows: List[Dict[str, Any]], columns: List[Tuple[str, str]], as_json: bool
) -> None:
    if as_json:
        print(json.dumps(response, indent=2, ensure_ascii=False))
    else:
        _print_table(rows, columns)


# -- CLI -------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Klien Wazuh API untuk triage (read-only kecuali dengan --apply).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--url", default=os.environ.get("WAZUH_API_URL", DEFAULT_URL))
    parser.add_argument("--user", default=os.environ.get("WAZUH_API_USER"))
    parser.add_argument("--password", default=os.environ.get("WAZUH_API_PASS"))
    parser.add_argument(
        "--verify",
        choices=["on", "off"],
        default="on" if os.environ.get("WAZUH_API_VERIFY", "1") not in ("0", "false", "off") else "off",
        help="Verifikasi sertifikat TLS (off untuk self-signed).",
    )
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--json", action="store_true", help="Keluarkan JSON mentah.")
    parser.add_argument("--apply", action="store_true", help="Izinkan perintah yang mengubah keadaan.")
    parser.add_argument("--yes", action="store_true", help="Konfirmasi kedua untuk --apply.")

    sub = parser.add_subparsers(dest="command", required=True)

    p_agents = sub.add_parser("agents", help="Daftar agent.")
    p_agents.add_argument("--q", dest="query", help="Query WQL, mis. status=active;os.name=ubuntu")
    p_agents.add_argument("--limit", type=int, default=50)
    p_agents.add_argument("--select", help="Field yang diambil, mis. id,name,status,ip")

    p_agent = sub.add_parser("agent", help="Konteks satu agent untuk triage.")
    p_agent.add_argument("agent_id")

    p_logs = sub.add_parser("logs", help="Log manager.")
    p_logs.add_argument("--search", help="Cari string pada pesan log.")
    p_logs.add_argument("--level", help="Filter level log.")
    p_logs.add_argument("--limit", type=int, default=50)

    sub.add_parser("status", help="Status manager.")

    p_rules = sub.add_parser("rules", help="Metadata ruleset.")
    p_rules.add_argument("--search")
    p_rules.add_argument("--limit", type=int, default=50)

    sub.add_parser("restart", help="Restart manager (butuh --apply --yes).")

    p_ar = sub.add_parser("active-response", help="Jalankan active response (butuh --apply --yes).")
    p_ar.add_argument("--command", required=True, help="Nama command AR, mis. firewall-drop")
    p_ar.add_argument("--arguments", nargs="*", default=[], help="Argumen tambahan")
    p_ar.add_argument("--agent", help="ID agent untuk alert sintetis")
    p_ar.add_argument(
        "--note",
        default=None,
        help="Konfirmasi bahwa AR sudah disetujui dan akan diverifikasi (wajib).",
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    client = WazuhApi(
        base_url=args.url,
        user=args.user,
        password=args.password,
        verify=args.verify == "on",
        timeout=args.timeout,
    )

    try:
        if args.command == "agents":
            response = client.agents(args.query, args.limit, args.select)
            _json_or_table(
                response,
                _items(response),
                [("id", "ID"), ("name", "Nama"), ("status", "Status"), ("ip", "IP")],
                args.json,
            )

        elif args.command == "agent":
            context = client.collect_agent_context(args.agent_id)
            if args.json:
                print(json.dumps(context, indent=2, ensure_ascii=False))
            else:
                _print_agent_context(args.agent_id, context)
            if not context["agent"]["ok"]:
                print(
                    "CATATAN: data agent tidak dapat diambil; triage tidak bisa dilanjutkan "
                    "tanpa telemetri. Lihat pesan error di atas.",
                    file=sys.stderr,
                )
                return 1

        elif args.command == "logs":
            response = client.logs(args.search, args.level, args.limit)
            _json_or_table(
                response,
                _items(response),
                [("timestamp", "Waktu"), ("level", "Level"), ("tag", "Tag"), ("description", "Pesan")],
                args.json,
            )

        elif args.command == "status":
            response = client.status()
            if args.json:
                print(json.dumps(response, indent=2, ensure_ascii=False))
            else:
                _print_daemons(response)

        elif args.command == "rules":
            response = client.rules(args.search, args.limit)
            _json_or_table(
                response,
                _items(response),
                [("id", "ID"), ("level", "Level"), ("description", "Deskripsi")],
                args.json,
            )

        elif args.command == "restart":
            _require_confirmation(args, "restart manager")
            response = client.restart()
            print("Permintaan restart dikirim.")
            if args.json:
                print(json.dumps(response, indent=2, ensure_ascii=False))

        elif args.command == "active-response":
            _require_confirmation(args, "active response")
            if not args.note:
                raise ConfigError(
                    "active response membutuhkan --note yang menjelaskan persetujuan dan "
                    "rencana verifikasi/rollback."
                )
            print(
                "PERINGATAN: bentuk payload active response dapat berbeda antar versi. "
                "Verifikasi hasilnya di active-responses.log dan pastikan aksi reversible.",
                file=sys.stderr,
            )
            response = client.active_response(args.command, args.arguments, args.agent)
            print("Permintaan active response dikirim.")
            if args.json:
                print(json.dumps(response, indent=2, ensure_ascii=False))

        else:  # pragma: no cover
            parser.error("perintah tidak dikenal")
        return 0

    except ConfigError as exc:
        print(f"Kesalahan konfigurasi: {exc}", file=sys.stderr)
        return 2
    except ApiError as exc:
        print(f"Kesalahan API: {exc}", file=sys.stderr)
        return 1


def _require_confirmation(args: argparse.Namespace, action: str) -> None:
    if not (args.apply and args.yes):
        raise ConfigError(
            f"{action} mengubah keadaan. Jalankan ulang dengan --apply --yes setelah "
            "mendapat persetujuan."
        )


def _print_agent_context(agent_id: str, context: Dict[str, Any]) -> None:
    agent = context["agent"]
    if agent["ok"]:
        row = (_items(agent["data"]) or [{}])[0]
        print(f"Agent {agent_id}: {row.get('name', '?')} — status {row.get('status', '?')}")
        print(f"  IP: {row.get('ip', '?')}  OS: {_dig(row, 'os.name') or '?'} {_dig(row, 'os.version') or ''}")
    else:
        print(f"Agent {agent_id}: TIDAK DAPAT DIAMBIL — {agent['error']}")

    for key, label in (
        ("processes", "Proses"),
        ("ports", "Port"),
        ("packages", "Paket"),
        ("sca", "SCA"),
    ):
        section = context.get(key) or {}
        if not section.get("ok"):
            print(f"  {label}: tidak tersedia ({section.get('error')})")
            continue
        items = _items(section["data"])
        print(f"  {label}: {len(items)} item")

    scan = context.get("syscheck_last_scan") or {}
    if scan.get("ok"):
        items = _items(scan["data"])
        if items:
            print(f"  FIM terakhir: {items[0].get('end', '?')}")
        else:
            print("  FIM terakhir: tidak ada data scan")
    else:
        print(f"  FIM terakhir: tidak tersedia ({scan.get('error')})")


def _print_daemons(response: Dict[str, Any]) -> None:
    items = _items(response)
    if not items:
        print("(tidak ada data status)")
        return
    row = items[0]
    for name, value in row.items():
        if isinstance(value, dict):
            print(f"{name}: {value.get('status', value)}")
        else:
            print(f"{name}: {value}")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
