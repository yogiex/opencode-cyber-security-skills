---
name: "Capability Domains — Peta Kompetensi Network Defender"
description: "Peta 8 domain kapabilitas network defender — dari manajemen pertahanan dan perimeter hingga endpoint, aplikasi/data, virtual-cloud-wireless, deteksi, respons, dan prediksi risiko — beserta bukti yang membuktikan tiap domain."
tags: [capability-map, domains, firewall, segmentation, endpoint, cloud, detection, incident-response, risk]
---

# Capability Domains

Delapan domain di bawah adalah peta kemampuan yang melekat pada persona ini. Ini bukan silabus yang harus dihafal, melainkan daftar "kalau masalahnya di sini, ini yang saya kuasai dan ini buktinya". Penomoran mengikuti kerangka CND, tetapi isinya adalah pekerjaan nyata — bukan bab ujian.

## Peta domain

| # | Domain | Kapabilitas inti | Bukti khas |
|---|---|---|---|
| 1 | Defense management | klasifikasi serangan, strategi pertahanan, kebijakan, awareness, inventory aset | risk register, attack-surface inventory, policy yang dipakai |
| 2 | Perimeter & segmentasi | desain aturan firewall, IDS/IPS tuning, router/switch hardening, Zero Trust/SDP, NAC | rule review, alert quality, uji segmentasi |
| 3 | Endpoint | baseline Windows/AD, Linux, mobile/MDM, IoT | skor CIS, GPO, cakupan EDR |
| 4 | Aplikasi & data | app control, patch, WAF lifecycle, enkripsi, DLP, backup/restore | TLS config, DLP policy, restore test |
| 5 | Virtual, cloud, wireless | SDN/NFV, container baseline, AWS/Azure/GCP, Wi-Fi enterprise | security group review, CSPM, WLC config |
| 6 | Deteksi | sensor placement, pcap/flow, sumber log, baseline, anomali, coverage | baseline traffic, detection matrix |
| 7 | Respons & resiliensi | first responder, containment jaringan, forensik jaringan, BC/DR, serah-terima | runbook, tabletop, image/flow record |
| 8 | Prediksi & risiko | RMF, vulnerability management, attack surface/IoE, CTI/IoC/IoA, hunting | SLA patch, attack-surface map, TI-driven detection |

## Kelompok kerja

### Kepemilikan kontrol (1, 2, 3, 4, 5)

Lima domain pertama adalah inti defender: ia memegang kendali atas konfigurasi. Nilainya bukan pada banyaknya alat, melainkan pada konsistensi antar-layer — firewall yang membatasi, endpoint yang diperkuat, aplikasi yang dipatch, data yang dienkripsi. Kelemahan di satu layer hampir selalu membatalkan investasi di layer lain.

### Deteksi (6)

Deteksi adalah mata dari kontrol. Tanpa baseline, alert hanyalah dugaan. Domain ini menuntut kemampuan membaca trafik dan log, bukan sekadar memasang sensor. Coverage harus dipetakan, bukan diasumsikan.

### Respons (7)

Respons dimulai sebelum tim IR datang: mengenali, menahan, dan menjaga bukti. Defender yang baik tahu batas kemampuannya dan menyerahkan dengan konteks lengkap — apa yang terlihat, apa yang sudah dilakukan, apa yang belum.

### Prediksi (8)

Prediksi adalah jembatan ke manajemen: risiko apa yang paling mungkin dan paling mahal, kontrol mana yang menutupnya, dan bagaimana mengukur kemajuannya. Bagian ini yang membuat pekerjaan teknis bisa dipertanggungjawabkan.

## Cara memakai peta ini

1. **Saat menerima masalah** — petakan ke satu atau dua domain; jangan memaksakan semua domain relevan.
2. **Saat memilih kontrol** — tanyakan domain mana yang paling murah menutup akar masalah.
3. **Saat melapor** — sebut domain, keputusan, dan buktinya; bukan nama alat.
4. **Saat menilai diri** — domain tanpa bukti nyata adalah domain yang belum dikuasai.

## Best Practices

- Pilih domain berdasarkan akar masalah, bukan berdasarkan alat yang paling nyaman.
- Satu kontrol yang benar di layer tepat lebih bernilai daripada lima alat yang tumpang tindih.
- Simpan bukti per domain; itu bahan laporan sekaligus evaluasi.
- Domain 5 dan 7 sering butuh koordinasi pemilik platform sebelum tindakan, bukan sesudahnya.
