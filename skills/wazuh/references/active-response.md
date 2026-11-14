---
name: "Active Response Wazuh"
description: "Konfigurasi active response Wazuh 4.x, semantik pemicu yang bersifat OR, kontrak skrip kustom lewat stdin JSON, verifikasi hasil, rollback, dan guardrail agar containment tidak menjadi tindakan destruktif."
tags: [wazuh, active-response, containment, firewall-drop, block-ip, disable-account, command, rules_group, timeout, rollback, ossec.conf]
---

# Active Response Wazuh

## Kapan Containment Masuk Akal

| Kondisi | Containment tepat? |
|---|---|
| Dampak sedang aktif (brute force berjalan, koneksi jahat berulang) | Ya, untuk memutus dampak |
| Alert sudah selesai tapi belum dipahami | Tidak — investigasi dulu |
| Aset kritikal tanpa allowlist | Tidak — risiko memutus layanan |
| Aksi tidak reversible (hapus berkas, matikan host) | Tidak tanpa persetujuan eksplisit |
| Bukti belum dikumpulkan | Tidak — containment bisa menghapus bukti |

Containment bukan hukuman dan bukan pengganti analisis. Tujuannya mempersempit dampak selama investigasi berjalan.

## Konfigurasi

```xml
<command>
  <name>firewall-drop</name>
  <executable>firewall-drop</executable>
  <timeout_allowed>yes</timeout_allowed>
</command>

<active-response>
  <disabled>no</disabled>
  <command>firewall-drop</command>
  <location>local</location>
  <rules_id>5763</rules_id>
  <timeout>600</timeout>
</active-response>
```

| Elemen | Fakta |
|---|---|
| `<command><name>` | Nama logis yang dipakai `<active-response><command>` |
| `<executable>` | Nama skrip **tanpa path**; Linux `/var/ossec/active-response/bin`, Windows `C:\Program Files (x86)\ossec-agent\active-response\bin` |
| `<timeout_allowed>` | `yes` bila skrip mendukung batas waktu |
| `<active-response><disabled>` | Wajib ada pada 4.13+ |
| `<location>` | `local` (agent), `server` (manager), `defined-agent` (+`<agent_id>`), `all` |
| `<rules_id>` / `<rules_group>` / `<level>` | Pemicu; lihat semantik OR di bawah |
| `<timeout>` | Durasi aksi, detik; tanpa ini aksi tidak dibatalkan otomatis |

### Semantik Pemicu Bersifat OR

`level`, `rules_id`, dan `rules_group` **dijumlahkan**, bukan difilter bersama. Menuliskan ketiganya tidak mempersempit; ia memperluas.

`rules_group` dicocokkan sebagai substring, sehingga `authentication` juga cocok dengan `authentication_failed`. Tambahkan koma di akhir (`authentication,`) untuk mencocokkan grup secara utuh.

`repeated_offenders` (daftar menit, maksimal 5 entri) hanya berlaku untuk active response sisi agent dan tidak didukung pada Windows.

## Skrip Kustom

Skrip menerima **JSON di stdin**, bukan argumen posisi:

```json
{
  "wazuh": {
    "active_response": {
      "name": "custom-block",
      "executable": "custom-block",
      "location": "local",
      "agent_id": "003"
    }
  },
  "agent": { "id": "003", "name": "web-01" },
  "source": { "ip": "203.0.113.45" },
  "user": { "name": "admin" },
  "command": "enable"
}
```

Perhatikan:

- `command` bernilai `enable` saat aksi dimulai dan `disable` saat `timeout` habis; skrip harus menangani keduanya.
- Struktur persis dapat berbeda antar versi (mis. penambahan `type` atau `stateful_timeout` pada 5.x); baca contoh skrip bawaan pada versi Anda dan uji di lingkungan non-produksi.
- Keluaran skrip dicatat di `/var/ossec/logs/active-responses.log` (Linux). Tanpa log ini, kegagalan AR tidak terlihat.
- Skrip harus idempoten: menerima `enable` dua kali tidak boleh merusak aturan firewall.

Contoh kerangka aman:

```python
#!/usr/bin/env python3
import json
import sys

req = json.load(sys.stdin)
action = req.get("command")
ip = (req.get("source") or {}).get("ip")

if not ip or not action:
    sys.exit(0)  # tidak ada yang bisa dilakukan; jangan crash

if action == "enable":
    block(ip)
elif action == "disable":
    unblock(ip)
```

## Verifikasi Setelah Aksi

| Yang diperiksa | Cara |
|---|---|
| Apakah aksi berjalan | `active-responses.log` pada agent |
| Apakah efeknya ada | Periksa aturan firewall/hosts.deny, atau status akun |
| Apakah alert berhenti | Kueri indexer pada window sesudahnya |
| Apakah ada efek samping | Layanan yang tiba-tiba tidak bisa diakses, login sah gagal |

Tanpa verifikasi, "sudah diblokir" hanyalah asumsi.

## Rollback

- Selalu tetapkan `timeout` agar aksi berakhir sendiri.
- Siapkan perintah pembalik sebelum menjalankan aksi (`disable-account` → aktifkan kembali; `firewall-drop` → hapus aturan).
- Catat waktu mulai dan rencana rollback di laporan eskalasi.
- Bila aksi mengenai host salah, hentikan, pulihkan, lalu tulis post-mortem singkat.

## Guardrail

| Aturan | Alasan |
|---|---|
| Allowlist host kritikal dan IP manajemen | Mencegah memutus akses ke platform itu sendiri |
| Dry-run di lingkungan uji sebelum produksi | Skrip AR mudah salah membaca JSON |
| Batasi `location` (hindari `all` tanpa alasan) | Mencegah blokir massal |
| Jangan jalankan AR dari skrip ad-hoc | Harus tercatat dan bisa diaudit |
| Satu aksi per alert, bukan berantai | Efek gabungan sulit dilacak |
| Persetujuan manusia untuk aksi non-reversible | Containment yang salah memperbesar insiden |

## Best Practices

- Pilih aksi paling ringan yang memutus dampak: blokir IP lebih ringan daripada mematikan layanan.
- Simpan bukti sebelum containment; setelah host terisolasi, data sulit diambil.
- Catat nama command, nilai `timeout`, dan alasan di laporan triase.
- Tinjau log AR setiap shift; kegagalan senyap adalah risiko yang tidak terlihat di dashboard.
- Uji skrip kustom dengan JSON contoh (termasuk `disable`) sebelum dipasang di produksi.
