---
name: "Incident Response — Framework, Fase, Bukti"
description: "Penanganan insiden dari sisi analyst: Cyber Kill Chain, Diamond Model, dan MITRE ATT&CK; fase IR dari preparation sampai post-incident; akuisisi bukti dengan chain of custody, hashing, dan write blocker; serta strategi containment per lapisan."
tags: [incident-response, kill-chain, diamond-model, mitre-attack, evidence, chain-of-custody, containment, forensics]
---

# Incident Response — Framework, Fase, Bukti

Analyst sering menjadi orang pertama yang menyebut "ini insiden" atau "ini bukan". Kualitas keputusan itu bergantung pada framework yang dipakai untuk membaca serangan, fase yang sedang berjalan, dan bukti yang diamankan sebelum tindakan apa pun mengubah keadaan.

## 1. Attack methodology frameworks

- **Cyber Kill Chain** — Recon → Weaponization → Delivery → Exploitation → Installation → C2 → Actions.
- **Diamond Model** — Adversary, Capability, Infrastructure, Victim, ditambah meta-features.
- **MITRE ATT&CK** — 15 tactics dan 200+ techniques untuk memetakan TTP.

Framework tidak saling menggantikan. Kill Chain memberi urutan, Diamond Model memberi hubungan antar-elemen, dan ATT&CK memberi kosakata teknik yang bisa dipakai lintas tim.

## 2. IR process

1. **Preparation** — IR plan, playbook, tool, pelatihan, dan tabletop exercise.
2. **Detection and analysis** — triage true/false positive, penyusunan timeline, dan root cause analysis.
3. **Containment** — penilaian scope dan isolasi pada network, host, cloud, atau identity.
4. **Eradication** — hapus malware, patch, reset kredensial, rebuild bila perlu.
5. **Recovery** — restore dari backup dan pantau kemungkinan infeksi ulang.
6. **Post-incident activity** — analisis forensik dan lessons learned.

Dalam praktik, fase-fase ini sering diringkas menjadi empat kelompok: preparation; detection and analysis; containment, eradication, and recovery; post-incident activity. Yang penting bukan jumlah fasenya, melainkan keputusan yang diambil di tiap peralihan.

## 3. Evidence acquisition

- **Chain of custody** — beri tag bukti, catat setiap perpindahan, simpan di tempat terkontrol.
- **Data integrity** — hash SHA256 sebelum dan sesudah analisis; gunakan write blocker saat akuisisi.
- **Preservation** — legal hold dan imaging bit-for-bit.

Bukti yang sudah berubah tidak bisa dikembalikan ke keadaan semula. Ambil yang volatil lebih dulu, lalu yang persisten.

## 4. Containment strategies

| Lapisan | Teknik |
|---|---|
| Network | blokir IP/domain, matikan port, segmentasi |
| Host | isolasi host, nonaktifkan akun, hentikan proses |
| Cloud | nonaktifkan API key, cabut sesi, isolasi instance |
| Identity | reset kredensial, cabut token, aktifkan MFA |

Containment selalu trade-off dengan ketersediaan. Keputusan memutus layanan ada pada pemilik layanan, bukan pada analyst yang menemukan alert.

## Best Practices

- Tentukan kriteria eskalasi sebelum insiden terjadi.
- Siapkan rencana komunikasi per stakeholder.
- Dokumentasikan semuanya — chain of custody adalah bukti, bukan formalitas.
- Lakukan lessons learned setelah setiap insiden untuk perbaikan berkelanjutan.
