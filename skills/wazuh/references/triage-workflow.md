---
name: "Alur Kerja Triage Wazuh"
description: "Siklus triage alert Wazuh per tier L1/L2/L3, timebox dan SLA berdasarkan level, urutan pengerjaan, kriteria eskalasi, definisi selesai, handover shift, dan metrik yang diukur."
tags: [wazuh, triage, workflow, tier, l1, l2, l3, sla, timebox, eskalasi, handover, metrik, soc]
---

# Alur Kerja Triage Wazuh

## Prinsip

1. Alert adalah klaim, bukan fakta: "rule X cocok pada log Y" belum berarti "serangan terjadi".
2. Keputusan diambil dengan bukti, dalam batas waktu, dan bisa direproduksi.
3. Antrean dikerjakan berdasarkan prioritas, bukan urutan kedatangan.
4. Yang tidak selesai harus diserahkan dengan konteks lengkap.

## Tier

| Tier | Wewenang | Menangani | Tidak boleh |
|---|---|---|---|
| **L1** | Triage dan verdict awal | Alert level 3–11, konteks dasar, penutupan FP yang jelas | Containment, mengubah ruleset, menutup alert level ≥ 12 |
| **L2** | Investigasi mendalam | Alert level 12+, korelasi lintas agent, validasi IoC, usulan tuning | Containment pada host produksi tanpa persetujuan |
| **L3 / IR** | Respons dan perubahan | Containment, forensik, perubahan rule, koordinasi lintas tim | — |

Batas tier adalah batas wewenang, bukan batas kemampuan: L1 yang menemukan indikasi serius langsung mengeskalasi, bukan menyelesaikan sendiri.

## Timebox dan SLA

| Level | Prioritas | Timebox triage awal | Target verdict | Catatan |
|---|---|---|---|---|
| 0–2 | — | — | — | Tidak menjadi alert; jangan dibuat antrean |
| 3–5 | P4 | — | 1 hari kerja | Hanya bila menyentuh aset/akun kritikal |
| 6–7 | P3 | 15 menit | 1 hari kerja | Mayoritas noise; jangan habiskan waktu |
| 8–9 | P3 | 15 menit | 4 jam | Butuh verifikasi baseline |
| 10–11 | P2 | 20 menit | 4 jam | Integritas file/berkas sistem |
| 12–13 | P1 | 10 menit | 30 menit | Siapkan eskalasi bersamaan |
| 14–16 | P0 | Segera | Segera | Eskalasi paralel, containment bila perlu |

Timebox dihitung dari alert **masuk antrean**, bukan dari saat analis membukanya. Bila habis: verdict `Unknown`, catat bukti yang sudah diambil, eskalasi.

## Urutan Pengerjaan Satu Alert

1. **Baca alert.** `rule.id`, `rule.level`, `rule.description`, `agent.name`, `location`, `timestamp`, `full_log`.
2. **Tentukan kelas alert.** SSH/auth, Windows auth, FIM, malware, web, SCA/CVE, USB, lainnya. Kelas menentukan playbook di [common-alert-playbooks.md](./common-alert-playbooks.md).
3. **Ambil konteks agent.** Status, OS, apakah agent baru, apakah aset kritikal.
4. **Ambil bukti sesuai kelas.** Urutan dan checklist di [evidence-collection.md](./evidence-collection.md).
5. **Korelasi.** Event lain dari agent/IP/user sama pada window yang wajar (`±5` menit untuk brute force, `±1` jam untuk FIM).
6. **Verdict + alasan.** Pakai [verdict-and-severity.md](./verdict-and-severity.md).
7. **Aksi.** Tutup, monitor, eskalasi, atau usulkan tuning.
8. **Dokumentasi.** Isi template laporan; bila belum selesai, isi handover.

## Kriteria Eskalasi

Eskalasi ke L2/IR bila salah satu benar:

- `rule.level >= 12`;
- aset masuk daftar kritikal (database, domain controller, jump host, server pembayaran);
- indikasi persistence (service baru, scheduled task, kunci SSH, akun baru);
- indikasi lateral movement (login lintas host, SMB/RDP/WinRM tak wajar);
- indikasi eksfiltrasi (volume keluar besar, koneksi ke luar pada jam tidak wajar);
- kredensial atau data sensitif terlibat;
- alert berulang yang tidak bisa dijelaskan setelah 2 kali triage;
- butuh tindakan di luar wewenang (containment, blokir, perubahan rule).

Isi eskalasi minimal: ringkasan satu paragraf, rule + level, agent + aset, timeline singkat, bukti yang sudah diperiksa, dugaan saat ini, tindakan yang sudah dilakukan, tindakan yang diminta, dan tenggat.

## Definisi Selesai

Sebuah alert boleh ditutup bila:

- verdict ditetapkan (`TP`/`FP`/`Benign`/`Unknown` dengan eskalasi);
- alasan tertulis memuat minimal dua sumber bukti, atau alasan eksplisit mengapa hanya satu;
- tindakan yang diambil dicatat (termasuk "tidak ada tindakan" beserta alasannya);
- bila menghasilkan usulan tuning, usulan itu tercatat di pelacak FP dengan bukti sampel;
- bila terkait insiden, ID tiket/insiden dicantumkan.

Alert `Unknown` yang dieskalasi juga dianggap selesai untuk L1; statusnya berpindah ke pemilik eskalasi.

## Handover Shift

Isi handover (template di [shift-handover-template.md](../assets/shift-handover-template.md)):

| Bagian | Wajib |
|---|---|
| Antrean tersisa | Jumlah per level dan rule terbanyak |
| Alert terbuka | ID alert, rule, agent, alasan belum selesai, langkah berikutnya |
| Menunggu eskalasi | Siapa pemiliknya, sejak kapan, apa yang diminta |
| Perubahan hari ini | Rule/CDB/AR yang diubah dan siapa yang menyetujui |
| Catatan telemetri | Agent mati, modul nonaktif, indeks bermasalah |
| Risiko | Hal yang mungkin memburuk dalam 8–12 jam ke depan |

Handover yang buruk lebih berbahaya daripada backlog: analis berikutnya mengulang pekerjaan dan kehilangan konteks.

## Metrik yang Layak Diukur

| Metrik | Definisi | Dipakai untuk |
|---|---|---|
| Backlog age | Usia alert tertua yang belum ditriase | Menentukan perlu tambahan shift atau tuning |
| MTTA | Waktu alert → triage pertama | Kesehatan proses |
| Rasio FP | FP / total triase per rule | Kandidat tuning |
| Rasio Unknown | Unknown / total | Indikasi playbook atau data kurang |
| Repeat alert | Alert sama berulang tanpa perubahan | Tuning belum tuntas |
| Coverage | Persentase alert yang punya verdict + alasan | Kualitas dokumentasi |

## Best Practices

- Kerjakan alert secara berkelompok per rule/agent: satu pola yang sama tidak perlu diselidiki 30 kali.
- Jangan menutup alert untuk "membersihkan dashboard"; backlog yang jujur lebih baik daripada angka yang bagus.
- Catat jam mulai dan selesai triage bila SLA diukur; perkiraan setelah kejadian tidak dapat diaudit.
- Bagikan pola baru ke seluruh shift (rule, agent, alasan FP) agar tidak ditriase ulang besok.
