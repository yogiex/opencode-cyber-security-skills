---
name: wazuh
description: Menjalankan triage alert SOC di Wazuh open source 4.x (all-in-one: manager, indexer, dashboard, agent) — menarik alert dan bukti dari indexer serta Wazuh API, memberi verdict TP/FP/Benign/Unknown, memprioritaskan, mengeskalasi atau menutup dengan alasan terverifikasi, lalu mengusulkan tuning rule. Pakai saat antrean alert Wazuh harus ditriase, bukan untuk instalasi dari nol, hunting proaktif, atau SIEM lain.
license: MIT
compatibility: opencode
metadata:
  audience: soc-analyst, tier-1, tier-2, detection-engineer
  workflow: triage
  source: wazuh-documentation
  version: "1.0.0"
  keywords: "wazuh, soc, triage, alert, siem, xdr, indexer, wazuh api, syscheck, sca, active response, local_rules, decoders, cdb, wazuh-logtest, alerts.json"
---

# Wazuh — Triage Alert SOC

Wazuh open source adalah platform XDR/SIEM self-hosted: **agent** mengirim telemetri, **manager** men-decode dan mencocokkan ruleset, **indexer** menyimpan alert, **dashboard** menampilkannya. Skill ini tentang **triage alert di deployment all-in-one** — dari satu alert di antrean sampai verdict yang bisa dipertanggungjawabkan, atau eskalasi yang membawa bukti.

Triage bukan membaca dashboard sampai yakin. Triage adalah mengumpulkan bukti dengan urutan termurah lebih dulu, lalu memutuskan dengan kriteria yang bisa ditulis ulang orang lain. Skill ini tidak mengajarkan instalasi Wazuh, hunting proaktif, atau lifecycle incident response penuh.

## Kapan Digunakan

Gunakan ketika:

- ada antrean alert Wazuh dan perlu diputuskan mana nyata, mana noise;
- satu alert butuh konteks (proses, port, paket, perubahan file, hasil SCA, kerentanan) sebelum dinilai;
- perlu verdict dan alasan yang bisa direproduksi analis shift berikutnya;
- alert berulang tiap hari dan perlu keputusan: eskalasi, tutup, atau ajukan tuning;
- perlu menarik alert secara terprogram dari indexer atau Wazuh API;
- perlu laporan shift/handover berbasis bukti.

Jangan gunakan untuk:

- hunting proaktif tanpa alert, SPL/KQL, atau ELK — gunakan `offsec-th-200` atau `offsec-soc-200`;
- containment, eradikasi, komunikasi krisis lintas tim — gunakan `ec-ecih` atau `offsec-ir-200`;
- teori triage dan pola pikir analis tanpa tool — gunakan `soc-analyst` atau `comptia-cysa`;
- lifecycle CTI, STIX/TAXII, MISP — gunakan `threat-intelligence`;
- kepatuhan formal dan pemetaan kontrol — gunakan `nist-800-53` atau `security-auditor`;
- instalasi, sertifikat, atau cluster dari nol — skill ini hanya membahas konteks yang memengaruhi triage.

## Peta Alur Triage

```text
[Antrean alert]  dashboard (Discover) atau indexer / API
        |
        v
[1] Alert mentah   rule.id, rule.level, agent.id, data.*, full_log, timestamp
        |
        v
[2] Konteks agent  status, OS, syscollector (proses/port/paket),
        |          syscheck (FIM), SCA, kerentanan
        v
[3] Korelasi       event lain dari agent/IP/user sama pada window sama
        |
        v
[4] Verdict        TP / FP / Benign / Unknown  + alasan tertulis
        |
        v
[5] Prioritas      level x kekritisan aset x keyakinan bukti
        |
        v
[6] Aksi           tutup / monitor / eskalasi / containment / ajukan tuning
        |
        v
[7] Dokumentasi    laporan triase + handover shift
```

## Decision Frame

Jawab aturan ini secara eksplisit sebelum menyimpulkan apa pun.

1. **Bukti minimum dua sumber.** Verdict sah bila didukung (a) alert dari manager/indexer dan (b) telemetri agent (syscollector, syscheck, SCA, log sumber, atau `full_log` yang bisa diverifikasi). Bila sumber kedua tidak ada — agent mati, modul `disabled`, log tidak dikumpulkan — sebutkan dan turunkan keyakinan; jangan mengarang.
2. **Timebox sebelum menebak.** L1 ±10 menit per alert. Bila habis dan bukti belum cukup: verdict `Unknown` + eskalasi dengan daftar bukti yang sudah dan masih perlu diambil. `FP` tanpa bukti adalah kesalahan termahal.
3. **Tutup hanya dengan alasan terverifikasi.** Minimal: rule ID, agent, rentang waktu, bukti yang diperiksa, dan alasan aktivitas itu tidak berbahaya. "Sudah dicek, aman" bukan alasan.
4. **Eskalasi karena pemicu, bukan perasaan.** Pemicu: `rule.level >= 12`; aset kritikal; indikasi persistence, lateral movement, atau eksfiltrasi; kredensial/data sensitif terlibat; atau butuh tindakan di luar wewenang triager.
5. **Containment hanya untuk dampak yang masih aktif.** Active response untuk memutus dampak (`firewall-drop`/`block-ip`, `disable-account`), bukan menghukum. Wajib: aksi reversible, ada `timeout`, host kritikal di allowlist, ada rencana revert. Bila ragu, eskalasi ke manusia.
6. **Tuning adalah hasil triage, bukan jalan pintas.** Rule diturunkan/di-whitelist hanya setelah ≥ 3 sampel false positive terdokumentasi. Perubahan rule/CDB lewat change request dan dicatat, bukan edit senyap.
7. **Telemetri mati bukan bukti aman.** "Tidak ada alert lain dari host itu" hanya bermakna bila agent `Active`, `logcollector` mengirim log, dan modul terkait aktif. `jsonout_output` atau Filebeat yang mati juga membuat alert tidak pernah sampai ke indexer.

## Level Alert dan Prioritas

Wazuh memberi level 0–16. Level adalah keparahan yang dirancang penulis rule, bukan risiko di lingkungan Anda. `log_alert_level` default **3**, jadi rule level 0–2 tidak menghasilkan alert dan tidak masuk dashboard.

| Level | Arti di Wazuh | Prioritas | Aksi |
|---|---|---|---|
| 0, 2 | Ignored / notifikasi sistem | — | Tidak diindeks; jangan ditriase, kecuali dicari di `archives` saat investigasi |
| 3 | Successful / authorized event | P4 | Hanya bila menyangkut akun atau aset kritikal |
| 4–5 | Error konfigurasi / salah password | P4 | Pantau pola; eskalasi bila berulang pada akun sama |
| 6–7 | Serangan relevansi rendah / kata kunci | P3 | Cek konteks; mayoritas noise |
| 8–9 | First time seen / sumber tidak valid | P3 | Verifikasi sumber dan baseline |
| 10–11 | Multiple error / integrity warning | P2 | Triase pada jam kerja yang sama |
| 12–13 | High importance / pola serangan umum | P1 | Triase segera, siapkan eskalasi |
| 14–15 | Pola serangan / severe attack | P0 | Eskalasi langsung, pertimbangkan containment |
| 16 | Di atas severe (biasanya rule kustom) | P0 | Audit dulu apakah level ini disengaja |

Prioritas akhir = level × kekritisan aset × keyakinan bukti. Aset kritikal menaikkan satu tingkat; bukti lemah menurunkannya sampai bukti tambahan masuk.

## Cara Pakai

```bash
# [1] Antrean 24 jam terakhir, level >= 8, dikelompokkan per rule/agent
python scripts/wazuh_triage.py queue --since 24h --min-level 8

# [2] Konteks agent: status, OS, proses, port, paket, FIM, SCA
python scripts/wazuh_api.py agent 003

# [3] Timeline event agent tersebut
python scripts/wazuh_triage.py timeline --agent 003 --since 6h

# [4] Laporan triase (JSON divalidasi skema, Markdown siap ditempel)
python scripts/wazuh_triage.py report --alert <_id> --out triage-003.md

# [5] Bila tuning diusulkan: validasi XML dulu, baru ajukan change request
python scripts/check-ruleset.py /var/ossec/etc/rules/local_rules.xml
```

Tanpa skrip alurnya sama: ambil alert dari **Discover** (index pattern `wazuh-alerts-*`, time field `timestamp`), konteks agent dari **Server management → Endpoints**, atau lewat `https://<manager>:55000` (Tools → API Console).

Langkah manual yang tidak bisa digantikan skrip:

1. **Baca `full_log`.** Rule cocok pada potongan tertentu; sisa baris sering membedakan serangan nyata dari kesalahan konfigurasi.
2. **Cek baseline.** Normal atau tidak untuk host/user itu? Bandingkan 7–30 hari, bukan hanya hari ini.
3. **Buang duplikasi.** Parent rule level 0 + child rule berlevel tinggi + rule korelasi `frequency`/`timeframe` membuat satu kejadian tampak seperti beberapa insiden.
4. **Tulis verdict dan alasan** memakai [triage-report-template.md](./assets/triage-report-template.md).
5. **Serahkan ke shift berikutnya** memakai [shift-handover-template.md](./assets/shift-handover-template.md) bila belum tuntas.

## Capability Map

| Kebutuhan | Referensi |
|---|---|
| Alur alert, field, level, `alerts` vs `archives` | [alert-schema.md](./references/alert-schema.md) |
| Tier, timebox, eskalasi, handover | [triage-workflow.md](./references/triage-workflow.md) |
| Bukti apa yang diambil dan urutannya | [evidence-collection.md](./references/evidence-collection.md) |
| Kueri dashboard dan indexer | [indexer-queries.md](./references/indexer-queries.md) |
| Wazuh API, WQL, RBAC, paginasi | [api-and-automation.md](./references/api-and-automation.md) |
| Verdict, keyakinan bukti, prioritas | [verdict-and-severity.md](./references/verdict-and-severity.md) |
| Playbook per kelas alert | [common-alert-playbooks.md](./references/common-alert-playbooks.md) |
| Sintaks rule/decoder dan loop pengujian | [rules-and-decoders.md](./references/rules-and-decoders.md) |
| FIM, SCA, vulnerability detection | [fim-sca-vulnerability.md](./references/fim-sca-vulnerability.md) |
| False positive dan tuning | [tuning-and-false-positive.md](./references/tuning-and-false-positive.md) |
| Containment dan active response | [active-response.md](./references/active-response.md) |
| Laporan, IoC, ATT&CK, handover | [reporting-and-handover.md](./references/reporting-and-handover.md) |
| Telemetri sehat, alert hilang/duplikat/terlambat | [telemetry-health-and-troubleshooting.md](./references/telemetry-health-and-troubleshooting.md) |
| Sumber resmi dan perbedaan versi | [referensi.md](./references/referensi.md) |

## Referensi

| File | Isi |
|---|---|
| [alert-schema.md](./references/alert-schema.md) | Pipeline alert, skema inti vs per-modul, batas visibilitas |
| [triage-workflow.md](./references/triage-workflow.md) | Tier L1/L2/L3, SLA, kriteria eskalasi, definisi selesai |
| [evidence-collection.md](./references/evidence-collection.md) | Checklist bukti per kelas alert dan batas waktunya |
| [indexer-queries.md](./references/indexer-queries.md) | Discover/DQL, DSL OpenSearch, agregasi, retensi |
| [api-and-automation.md](./references/api-and-automation.md) | JWT, endpoint triage, WQL, RBAC, pemakaian skrip |
| [verdict-and-severity.md](./references/verdict-and-severity.md) | Definisi verdict, matriks bukti, formula prioritas |
| [common-alert-playbooks.md](./references/common-alert-playbooks.md) | Playbook SSH, Windows auth, FIM, malware, web, CVE, USB |
| [rules-and-decoders.md](./references/rules-and-decoders.md) | Sintaks XML, batasan `overwrite`, `wazuh-logtest`, restart |
| [fim-sca-vulnerability.md](./references/fim-sca-vulnerability.md) | Konfigurasi dan field alert tiga modul penyumbang bukti |
| [tuning-and-false-positive.md](./references/tuning-and-false-positive.md) | Akar FP, urutan opsi tuning, change request |
| [active-response.md](./references/active-response.md) | Konfigurasi AR, semantik OR, kontrak skrip, rollback |
| [reporting-and-handover.md](./references/reporting-and-handover.md) | Template laporan, ATT&CK, IoC, redaksi, handover |
| [telemetry-health-and-troubleshooting.md](./references/telemetry-health-and-troubleshooting.md) | Kesehatan agent/log/Filebeat/indexer, alert hilang |
| [referensi.md](./references/referensi.md) | Tautan resmi per topik dan matriks 4.x vs 5.x |

## Scripts dan Assets

| File | Isi |
|---|---|
| [scripts/wazuh_api.py](./scripts/wazuh_api.py) | Klien Wazuh API read-only; mutasi hanya dengan `--apply` |
| [scripts/wazuh_triage.py](./scripts/wazuh_triage.py) | Antrean, timeline, laporan dari indexer; `--dry-run` tanpa koneksi |
| [scripts/check-ruleset.py](./scripts/check-ruleset.py) | Validator rule/decoder kustom |
| [assets/triage-report-template.md](./assets/triage-report-template.md) | Laporan triase per alert |
| [assets/shift-handover-template.md](./assets/shift-handover-template.md) | Handover shift |
| [assets/triage-report.schema.json](./assets/triage-report.schema.json) | Skema keluaran JSON laporan |
| [assets/rule-template.xml](./assets/rule-template.xml) | Kerangka rule kustom + contoh `overwrite` |
| [assets/decoder-template.xml](./assets/decoder-template.xml) | Decoder parent, sibling, dan JSON |
| [assets/false-positive-tracker.csv](./assets/false-positive-tracker.csv) | Pelacak FP → usulan tuning |

## Gotchas

1. **Level 0–2 tidak pernah jadi alert.** `log_alert_level` default 3 dan level 0/2 "tidak muncul di dashboard"; menaikkan level untuk debugging adalah perubahan deteksi, bukan triage.
2. **`overwrite="yes"` tidak bisa mengubah percabangan.** `if_sid`, `if_group`, `if_level`, `if_matched_sid`, `if_matched_group` diabaikan diam-diam pada rule overwrite — buat rule anak baru bila butuh ancestry berbeda.
3. **`noalert="1"` bukan mematikan rule.** Alert ditekan, tetapi event tetap dievaluasi rule lain; memakai `level="0"` juga bukan cara mematikan korelasi.
4. **Menyimpan file cukup untuk `wazuh-logtest`, tetapi alert produksi butuh restart manager.** CDB list juga hanya dibangun saat analysisd start; tidak ada reload ruleset terdokumentasi (`wazuh-control reload` = konfigurasi agent).
5. **`wazuh-regex` hanya OSRegex, bukan PCRE2.** Pola yang lolos di logtest bisa berperilaku berbeda saat diuji dengan tool itu; selalu uji lewat `wazuh-logtest`.
6. **Decoder gagal senyap.** `regex` tanpa `order`, atau tanpa `prematch`/`program_name` (sendiri atau induk), tidak akan match tanpa pesan error; decoder juga tidak punya "cucu", dan match pertama menghentikan pencarian decoder lain.
7. **Time field dashboard adalah `timestamp`, bukan `@timestamp`.** Dokumen di indexer punya keduanya; salah memilih membuat filter waktu tampak kosong.
8. **Jam manager UTC, dashboard lokal.** Jangan menyimpulkan urutan kejadian dari jam yang tampil; gunakan `timestamp` untuk timeline.
9. **Agent `Active` belum tentu mengirim log.** Status hanya menandakan agentd hidup; `logcollector` bisa mati, path log salah, atau modul `disabled`.
10. **API default memotong 500 item dan token berumur 900 detik.** Pakai `limit`/`offset`; WQL memakai `;` (AND) dan `,` (OR) yang harus di-URL-encode. `error: 2` pada HTTP 200 berarti hasil parsial, bukan sukses penuh.
11. **Active response bersifat OR.** `level`, `rules_id`, `rules_group` dijumlahkan sebagai pemicu, bukan filter gabungan; `rules_group` tanpa koma akhir cocok sebagai substring (`authentication` juga cocok `authentication_failed`).
12. **SCA hanya mengirim perubahan status.** "Tidak ada alert SCA" bukan berarti semua check lolos; mengubah hash policy memicu alert untuk semua check.
13. **`full_log` bisa memuat kredensial, token, atau PII.** Redaksi sebelum masuk laporan, tiket, atau kanal chat.
14. **Dokumentasi 5.x berbeda dari 4.x.** `master` kini untuk 5.x (path `/var/wazuh-manager`, AR `block-ip`, vulnerability feed via indexer); instruksi di skill ini untuk 4.x — cek `api_version` atau `wazuh-control info` sebelum mengikuti path dari internet.

## Progressive Disclosure

| Ketika butuh... | Muat berkas ini |
|---|---|
| Memahami dari mana alert berasal dan field apa yang ada | [alert-schema.md](./references/alert-schema.md) |
| Menentukan tier, SLA, dan kapan eskalasi | [triage-workflow.md](./references/triage-workflow.md) |
| Memutuskan bukti apa yang dikumpulkan | [evidence-collection.md](./references/evidence-collection.md) |
| Menulis kueri dashboard atau indexer | [indexer-queries.md](./references/indexer-queries.md) |
| Menarik data lewat API | [api-and-automation.md](./references/api-and-automation.md) |
| Menulis verdict dan prioritas | [verdict-and-severity.md](./references/verdict-and-severity.md) |
| Menghadapi kelas alert tertentu | [common-alert-playbooks.md](./references/common-alert-playbooks.md) |
| Menyusun atau menguji rule/decoder | [rules-and-decoders.md](./references/rules-and-decoders.md) |
| Menafsirkan bukti FIM/SCA/kerentanan | [fim-sca-vulnerability.md](./references/fim-sca-vulnerability.md) |
| Alert berulang dan perlu tuning | [tuning-and-false-positive.md](./references/tuning-and-false-positive.md) |
| Perlu containment | [active-response.md](./references/active-response.md) |
| Menyusun laporan atau handover | [reporting-and-handover.md](./references/reporting-and-handover.md) |
| Alert tidak muncul, duplikat, atau terlambat | [telemetry-health-and-troubleshooting.md](./references/telemetry-health-and-troubleshooting.md) |
| Mencari sumber resmi dan mengecek versi | [referensi.md](./references/referensi.md) |

## Best Practices

- **Bukti dulu, cerita kemudian.** Laporan yang dimulai dari dugaan lalu mencari pembenaran adalah confirmation bias, bukan triage.
- **Satu alert, satu alasan.** Jangan menggabungkan beberapa alert menjadi satu verdict tanpa menyebut mana mewakili mana.
- **Hormati batas wewenang.** Containment pada host produksi, penghapusan agent, dan perubahan ruleset butuh persetujuan pemilik aset.
- **Redaksi sebelum berbagi.** Kredensial, token, dan PII di `full_log` tidak boleh masuk tiket atau laporan.
- **Ukur tuning.** Bandingkan volume alert sebelum dan sesudah, dan pastikan sampel serangan serupa masih tertangkap.
- **Tulis untuk shift berikutnya.** Handover buruk membuat analis mengulang pekerjaan atau melewatkan alert setengah jalan.

## License

MIT
