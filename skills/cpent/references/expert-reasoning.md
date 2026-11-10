---
name: "Expert Reasoning — Model Berpikir Operator Berpengalaman"
description: "Model mental yang membedakan operator CPENT berpengalaman dari pemula: target sebagai graf, trust boundary, ekonomi eksploitasi, register asumsi, siklus hipotesis, anggaran noise, pustaka pola, triage 60 detik, anti-pattern, dan aturan berhenti."
tags: [reasoning, mental-models, heuristics, triage, attack-graph, decision-making]
---

# Expert Reasoning

Pemula bertanya "tool apa yang dipakai di sini". Operator berpengalaman bertanya "edge mana yang belum saya punya menuju objective, dan apa cara termurah mendapatkannya".

## 1. Target adalah graf, bukan daftar host

Node: host, akun, layanan, sertifikat, segmen, data.
Edge: reachability, kredensial, trust (delegasi, trust domain), konfigurasi (ACL, share, template), dan jalur aplikasi.

Setiap temuan menambah node atau edge. Objective adalah path dari node awal ke crown jewel. Konsekuensinya:

- Host yang "tidak menarik" tetap bernilai jika ia edge (file server, jump host, backup server, CI runner, printer, hypervisor console).
- Kredensial adalah edge shortcut; satu password bisa memangkas tiga hop.
- Port yang terlihat sepele (5985, 88, 389) sering lebih berharga daripada RCE terisolasi.

## 2. Empat pertanyaan sebelum aksi

1. **Objective sebenarnya apa?** Domain admin, data pelanggan, kontrol PLC, atau bukti kedalaman?
2. **Edge mana yang hilang?** Reachability, kredensial, hak, atau bukti?
3. **Apa cara termurah mendapatkannya?** Waktu, noise, dan risiko.
4. **Bukti apa yang harus diambil?** Tentukan sebelum eksekusi, bukan sesudah.

Jika salah satu pertanyaan tidak bisa dijawab, langkah berikutnya adalah bertanya atau enumerasi — bukan mengeksploitasi.

## 3. Ekonomi eksploitasi

| Aksi | Biaya waktu | Noise | Risiko produksi | Nilai tipikal |
|---|---|---|---|---|
| Baca versi/banner | rendah | rendah | rendah | hipotesis |
| Coba kredensial default | rendah | rendah | rendah | akses |
| Enumerasi share/SNMP | rendah | sedang | rendah | kredensial, peta |
| Exploit publik teruji | sedang | tinggi | sedang | shell |
| Kerberoast/AS-REP | sedang | sedang | rendah | hash |
| Relay/coercion | sedang | tinggi | sedang | akses langsung |
| Kernel exploit | sedang | tinggi | tinggi | root lokal |
| DCSync | rendah | sangat tinggi | tinggi | domain |
| Write ke PLC | rendah | tinggi | sangat tinggi | kontrol proses |

Aturannya bukan "selalu yang murah", tapi **nilai dibagi biaya**: jangan membakar noise tinggi untuk edge yang tidak menuju objective.

## 4. Register asumsi

Tulis asumsi yang sedang dipegang, lalu cari cara memfalsifikasinya:

| Asumsi | Keyakinan | Cara memfalsifikasi |
|---|---|---|
| SMB signing tidak wajib | sedang | `nxc smb --gen-relay-list` |
| Ada jalur dua hop | rendah | `ip route`, `arp`, scan dari pivot |
| Versi rentan | sedang | banner, paket, build number |
| Kredensial masih valid | tinggi | login terkontrol, cek lockout policy |
| Target OT read-only | tinggi | konfirmasi RoE, bukan asumsi teknis |

Asumsi yang tidak pernah diuji adalah sumber laporan yang salah.

## 5. Siklus hipotesis

```
Observasi → Hipotesis → Uji termurah → Catat bukti → Perbarui model
```

Anti-pattern: langsung mengeksploitasi tanpa hipotesis. Jika eksploit berhasil tanpa tahu mengapa, kamu tidak bisa mereproduksinya di laporan.

## 6. Anggaran noise

Setiap engagement punya batas toleransi deteksi. Perlakukan seperti anggaran:

- **Hemat**: baca banner, cek default credential, enumerasi share, baca konfigurasi.
- **Menengah**: exploit publik, kerberoast, password spray kecil.
- **Mahal**: relay/coercion, DCSync, exploit yang memicu EDR, write OT.

Habiskan anggaran pada jalur yang paling mungkin menuju objective; sisa anggaran untuk verifikasi.

## 7. Pustaka pola

| Jika melihat… | Pikirkan… |
|---|---|
| 445 terbuka, signing mati, ada coercion | relay ke LDAP → RBCD → DA |
| Akun layanan dengan SPN | Kerberoast; cek password lemah dan hak |
| Template ADCS dengan SAN yang bisa diisi | ESC1 → impersonasi |
| Host unconstrained delegation | coercion → TGT → DCSync |
| `sudo -l` dengan wildcard/NOPASSWD | eskalasi langsung, cek GTFOBins |
| SUID di `/opt` atau script custom | cek fungsi internal, PATH, library |
| Cron root memanggil script writable | tulis payload, tunggu jadwal |
| Docker socket ter-mount | host root |
| Upload + path traversal | webshell di webroot, cek ekstensi |
| SSRF | metadata cloud, layanan internal, Redis/ES tanpa auth |
| LFI | log poisoning, filter chain, session file |
| JWT tanpa verifikasi/`alg:none` | impersonasi, eskalasi role |
| IDOR berurutan | enumerasi objek, dampak data |
| Port 1433/3306/5432 terbuka | kredensial lemah, `xp_cmdshell`/`COPY PROGRAM` |
| 6379/9200/8500 tanpa auth | RCE atau baca data |
| 5985/5986 + kredensial | eksekusi jarak jauh |
| 88 + 389 + 445 | domain controller — target bernilai tinggi |
| 502/102/47808 | OT — read-only dulu |
| Host dual-homed | jembatan segmen, kandidat pivot |
| "Tidak ada port terbuka" | host mati, firewall stateful, atau scan salah arah |

Pola adalah pemicu hipotesis, bukan kesimpulan.

## 8. Triage 60 detik

Setelah scan selesai, urutkan berdasarkan jarak ke objective, bukan berdasarkan kerumitan exploit:

1. **Domain controller / identity** — 88, 389, 636, 445.
2. **Remote execution** — 5985, 5986, 445, 135.
3. **Data** — 1433, 3306, 5432, 445, 2049.
4. **Aplikasi** — 80, 443, 8080, 8443.
5. **Manajemen** — 161, 623, 2375, 6443.
6. **Industri** — 502, 102, 47808.

Untuk tiap baris: versi, autentikasi, jalur yang mungkin, bukti yang dibutuhkan.

## 9. Anti-pattern

- **Exploit-first**: mencari CVE sebelum memahami layanan.
- **Tool dump**: menjalankan scanner tanpa membaca hasilnya.
- **Rabbit hole**: 45 menit tanpa hipotesis baru — berhenti, ganti sudut.
- **Mengabaikan host membosankan**: file server, jump host, backup.
- **Satu sinyal**: menyimpulkan rentan dari banner saja.
- **Noise tanpa tujuan**: scan berulang yang tidak menambah edge.
- **Laporan belakangan**: bukti hilang saat sesi berakhir.

## 10. Aturan berhenti

Berhenti ketika salah satu benar:

- Objective tercapai dan bukti sudah lengkap.
- Nilai marginal < risiko marginal (noise, produksi, waktu).
- Tiga hipotesis berturut-turut gagal — kembali ke enumerasi, bukan menambah tekanan.
- Batas window RoE tercapai.

## 11. Bertanya seperti expert

Sebelum menyentuh target, ajukan pertanyaan yang menentukan bentuk pekerjaan:

- Aset mana yang paling bernilai bagi klien, dan mengapa?
- Deteksi seperti apa yang aktif (EDR, SIEM, SOC 24/7)?
- Apakah ada jam produksi yang tidak boleh diganggu?
- Data apa yang tidak boleh disalin, meski bisa?
- Temuan sebelumnya apa yang sudah diketahui klien?
- Siapa yang harus dihubungi jika host mati?

## Best Practices

- Gambar graf sebelum memilih tool; perbarui setiap kali edge berubah.
- Tulis asumsi dan cara memfalsifikasinya di catatan engagement.
- Belanjakan noise seperti uang: sedikit, terarah, dan dengan alasan.
- Kecepatan datang dari sedikit percobaan yang tepat, bukan banyak percobaan.
- Jika tidak bisa menjelaskan mengapa sebuah langkah berhasil, itu bukan temuan.
