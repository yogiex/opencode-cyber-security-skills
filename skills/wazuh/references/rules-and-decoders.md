---
name: "Rule dan Decoder Wazuh"
description: "Sintaks rule dan decoder Wazuh 4.x, rentang ID kustom, batasan overwrite, frequency/timeframe/ignore/noalert, decoder parent dan sibling, decoder JSON, serta loop pengujian dengan wazuh-logtest dan syarat restart manager."
tags: [wazuh, rules, decoders, local_rules, xml, overwrite, frequency, timeframe, noalert, wazuh-logtest, sibling, json-decoder, cdb]
---

# Rule dan Decoder Wazuh

## Di Mana Menulis

| Berkas | Tujuan |
|---|---|
| `/var/ossec/etc/rules/local_rules.xml` | Rule kustom; tempat utama untuk tuning hasil triage |
| `/var/ossec/etc/decoders/local_decoder.xml` | Decoder kustom |
| `/var/ossec/etc/lists/` | CDB list (whitelist, IoC) |
| `/var/ossec/ruleset/rules/`, `/var/ossec/ruleset/decoders/` | Ruleset bawaan — **jangan diedit**, tertimpa saat upgrade |

File tambahan boleh dibuat di `etc/rules/` atau `etc/decoders/`; direktori itu sudah termasuk dalam `<ruleset>`.

## Rule

```xml
<group name="local,syslog,sshd,">
  <rule id="100200" level="10" frequency="6" timeframe="120">
    <if_matched_sid>5710</if_matched_sid>
    <same_source_ip />
    <description>sshd: brute force terdeteksi ($(firedtimes) percobaan dalam 120 detik)</description>
    <mitre>
      <id>T1110</id>
    </mitre>
    <group>authentication_failures,pci_dss_10.2.4,</group>
  </rule>
</group>
```

| Elemen | Aturan |
|---|---|
| `id` | Kustom **100000–120000**; di bawah itu milik ruleset bawaan |
| `level` | 0–16; level di bawah `log_alert_level` (default 3) tidak menjadi alert |
| `frequency` | 2–9999, jumlah kecocokan sebelum alert |
| `timeframe` | 1–99999 detik, jendela penghitungan |
| `ignore` | 1–999999 detik, menekan rule setelah terpicu |
| `overwrite` | `yes`/`no`; hanya untuk rule bawaan yang disalin ke file kustom |
| `noalert` | `1`/`0`; alert ditekan tetapi event tetap dievaluasi rule lain |
| `if_sid` | Rule induk harus terpicu lebih dulu |
| `if_matched_sid` | Seperti `if_sid`, tetapi dalam `timeframe` |
| `if_group` / `if_matched_group` | Berdasarkan grup rule induk |
| `field` | `name="..."` + pola regex pada field hasil decoder |
| `same_*` / `different_*` | Korelasi field: `same_source_ip`, `same_user`, `same_field`, dst. |
| `time` / `weekday` | Memakai jam lokal **server**, bukan timestamp event |

### Tuning Rule Bawaan dengan `overwrite`

```xml
<group name="syslog,sshd,">
  <rule id="5710" level="12" overwrite="yes">
    <description>sshd: login attempt with non-existent user (level dinaikkan)</description>
  </rule>
</group>
```

**Batas penting:** `overwrite="yes"` **mengabaikan** `if_sid`, `if_group`, `if_level`, `if_matched_sid`, dan `if_matched_group` — nilai asli rule tetap dipakai. Bila butuh percabangan berbeda, buat rule anak baru dengan ID 100xxx dan `if_sid` ke rule asli. Jangan lupa menyertakan kembali `<description>` dan `<group>` karena rule hasil overwrite menggantikan definisi asli.

### Yang Terjadi pada Berbagai Level

| Perubahan | Efek |
|---|---|
| Turunkan `level` ke 0–2 | Alert hilang sama sekali (di bawah `log_alert_level`) |
| `noalert="1"` | Alert hilang, tetapi event masih dievaluasi rule lain |
| `ignore` | Alert pertama muncul, berikutnya ditekan dalam jendela waktu |
| Tambah `frequency`/`timeframe` | Mengubah rule tunggal menjadi korelasi; uji dengan banyak event dalam satu sesi logtest |

## Decoder

```xml
<!-- Parent: menangkap program dan menyiapkan konteks -->
<decoder name="myapp">
  <program_name>^myapp</program_name>
</decoder>

<!-- Child: mengekstrak field -->
<decoder name="myapp">
  <parent>myapp</parent>
  <regex>user '(\w+)' from '(\d+.\d+.\d+.\d+)'</regex>
  <order>dstuser, srcip</order>
</decoder>
```

| Elemen | Aturan |
|---|---|
| `program_name` | Nama program pada header syslog; disarankan regex berjangkar (`^myapp`) |
| `prematch` | Mencocokkan sebelum `regex`; dipakai untuk melewati header |
| `parent` | Decoder induk; decoder tidak boleh punya "cucu" |
| `regex` | **Wajib** disertai `order`; jumlah capture group harus sama dengan jumlah field `order` |
| `order` | Field statis (`srcip`, `dstuser`, `srcuser`, `id`, `url`, `action`, `status`, `data`, `extra_data`) atau nama dinamis |
| `type` | Klasifikasi: `syslog`, `firewall`, `ids`, `web-log`, `windows`, `squid`, `host-information`, `ossec` |
| `plugin_decoder` | `JSON_Decoder`, `PF_Decoder`, `SymantecWS_Decoder`, `SonicWall_Decoder`, `OSSECAlert_Decoder` |

Aturan yang mudah dilanggar:

- `regex` tanpa `order` **tidak akan match**, tanpa pesan error.
- Decoder dengan `regex` harus punya `prematch` atau `program_name` di dirinya sendiri atau induknya.
- Sibling decoder (beberapa `decoder name` sama dengan `parent` sama) berhenti pada match pertama; `prematch` yang terlalu umum "mencuri" event dari decoder lain.
- Decoder JSON otomatis aktif untuk log JSON valid; **array of objects tidak didukung**; gunakan `offset="after_prematch"` untuk JSON yang tertanam di teks.

### Menimpa Decoder Bawaan

Salin berkas decoder bawaan ke `/var/ossec/etc/decoders/`, sunting, lalu kecualikan berkas aslinya:

```xml
<ruleset>
  <decoder_dir>ruleset/decoders</decoder_dir>
  <rule_dir>ruleset/rules</rule_dir>

  <decoder_dir>etc/decoders</decoder_dir>
  <rule_dir>etc/rules</rule_dir>
  <decoder_exclude>ruleset/decoders/0310-ssh_decoders.xml</decoder_exclude>
</ruleset>
```

Konsekuensi: berkas default itu tidak lagi menerima perbaikan dari upstream.

## Loop Pengujian

```bash
# Uji satu atau beberapa log; akhiri dengan Ctrl+D
/var/ossec/bin/wazuh-logtest

# Uji pola regex (hanya OSRegex, bukan PCRE2)
/var/ossec/bin/wazuh-regex 'user "(\w+)"'
```

Tiga fase yang harus dibaca:

1. **Pre-decoding** — `timestamp`, `hostname`, `program_name`.
2. **Decoding** — decoder yang cocok dan field yang dihasilkan (`dstuser`, `srcip`, dst.).
3. **Filtering** — rule yang cocok, `level`, `description`, `groups`, `firedtimes`.

Fakta operasional:

- Menyimpan berkas cukup agar logtest membaca perubahan; **alert produksi baru mengikuti ruleset setelah manager di-restart** (`systemctl restart wazuh-manager`).
- `firedtimes` adalah penghitung per sesi. Untuk menguji rule `frequency`, kirim beberapa log dalam **satu sesi** (token sesi sama); memulai sesi baru me-reset penghitung.
- CDB list dibangun saat analysisd start; setelah mengubah list, restart manager.
- Tidak ada perintah reload ruleset yang terdokumentasi; `wazuh-control reload` memuat ulang konfigurasi agent, bukan ruleset manager.
- `verify-agent-conf` memvalidasi `agent.conf` pada grup di `/var/ossec/etc/shared`, bukan ruleset manager.

## CDB List

```text
# /var/ossec/etc/lists/scanner-whitelist
10.10.5.20:scanner-vuln
203.0.113.7:pentest-2026-11
```

Deklarasikan di `<ruleset>` tanpa ekstensi, lalu pakai di rule:

```xml
<ruleset>
  <list>etc/lists/scanner-whitelist</list>
</ruleset>

<rule id="100210" level="0">
  <if_sid>5710</if_sid>
  <list field="srcip" lookup="address_match_key">etc/lists/scanner-whitelist</list>
  <description>sshd: percobaan login dari scanner internal (dikenali CDB)</description>
</rule>
```

Mode lookup: `match_key` (default), `address_match_key` (CIDR), `not_match_key`, `not_address_match_key`, `match_key_value` + `check_value`.

## Best Practices

- Satu perubahan rule per change request, dengan sampel alert sebelum dan sesudah.
- Uji selalu di `wazuh-logtest`, lalu verifikasi alert nyata di indexer setelah restart — logtest tidak membuktikan alert sampai ke dashboard.
- Jangan memakai `level="0"` untuk "mematikan" rule korelasi; gunakan `ignore` atau pengecualian yang sempit dan terdokumentasi.
- Beri `description` yang bisa dibaca analis: sertakan subjek, aksi, dan nilai penting.
- Simpan aturan tuning di `local_rules.xml` dan catat ID 100xxx di changelog organisasi agar tidak bentrok.
