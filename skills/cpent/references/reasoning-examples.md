---
name: "Reasoning Examples — Junior versus Expert"
description: "Empat skenario lapangan dengan penalaran orang pertama: membaca hasil scan, memilih antara upload dan LFI, menyusun dua hop pivot, dan memutuskan apakah menunggu cracking atau berpindah jalur — masing-masing dengan kontras respons junior."
tags: [reasoning, examples, triage, pivoting, kerberoast, decision-making]
---

# Reasoning Examples

Contoh di bawah menunjukkan **cara berpikir**, bukan jawaban baku. Situasi nyata selalu lebih berisik; yang bisa ditiru adalah urutan pertimbangannya.

## Skenario 1 — Scan bersih tanpa web

**Data:** `10.10.20.15` membuka 135, 445, 3389, 5985. Tidak ada 80/443. Di share `\\10.10.20.10\it$` ditemukan `deploy.ps1` berisi kredensial layanan.

**Junior:** Menjalankan `ms17-010` scanner, lalu brute force RDP.

**Expert:**

1. Kredensial adalah edge termurah. Uji di 5985 (WinRM) dan 445 dulu — jangan sentuh RDP tanpa kebutuhan.
2. Jika kredensial valid dan user itu local admin di host, langkah berikutnya adalah dump lokal + BloodHound, bukan exploit.
3. Jika bukan admin, periksa share lain dan sesi: `nxc smb --shares --sessions`, `net use`.
4. 445 + kredensial → cek SMB signing untuk relay, tetapi relay hanya berguna jika ada target tanpa signing dan coercion.
5. 3389 disimpan sebagai bukti akses interaktif, bukan jalur utama.

**Keputusan:** validasi kredensial di WinRM → enumerasi domain → cari jalur DA. Bukti: `whoami /all`, hostname, sid, dan share yang bisa diakses.

**Pelajaran:** port yang tidak "seksi" (5985) sering menjadi jalan masuk yang tenang.

## Skenario 2 — Upload, LFI, dan IDOR bersamaan

**Data:** Aplikasi PHP punya halaman upload gambar, parameter `page=` yang bisa diarahkan ke file, dan `/api/invoice/1042` yang mengembalikan invoice milik pengguna lain.

**Junior:** Langsung mencoba webshell upload dan payload LFI secara acak.

**Expert:**

1. Tentukan objective: data pelanggan atau eksekusi server. Dua objective, dua jalur berbeda.
2. IDOR sudah membuktikan dampak data dengan biaya noise hampir nol — ambil bukti minimum (satu invoice, bukan seluruh dataset), lalu berhenti.
3. LFI punya biaya lebih rendah daripada upload: coba baca file konfigurasi; jika berhasil, cari kredensial, bukan langsung log poisoning.
4. Upload: uji dulu apakah file non-eksekusi bisa diakses dari webroot; bypass ekstensi hanya jika eksekusi memungkinkan.
5. Setiap jalur punya bukti sendiri: IDOR (request/response), LFI (path + isi file), upload (URL + eksekusi).

**Keputusan:** buktikan IDOR lebih dulu, lanjutkan LFI untuk kredensial, simpan upload sebagai jalur RCE jika dua lainnya tidak memberi akses host.

**Pelajaran:** dampak data sering lebih berharga daripada RCE, dan jauh lebih tenang.

## Skenario 3 — Dua hop menuju database

**Data:** Pivot 1 adalah web server DMZ (`10.10.10.20`, interfaces `10.10.10.20` dan `172.16.5.10`). Di segmen `172.16.5.0/24` ada file server dual-homed ke `192.168.50.0/24`. Target database ada di `192.168.50.30:5432`.

**Junior:** Memasang chisel SOCKS, lalu menjalankan `nmap -sS` melalui proxychains dan bingung karena hasil kosong.

**Expert:**

1. Topologi dulu: dua hop berarti dua tunnel atau satu tunnel bertingkat; pilih berdasarkan tool yang dibutuhkan.
2. Butuh `nmap -sS` dan Impacket → Ligolo-ng TUN di tiap hop, atau satu Ligolo dengan dua agent.
3. Buktikan reachability per hop: dari pivot 1 ke `172.16.5.10:445`, lalu dari file server ke `192.168.50.30:5432`.
4. Jangan scan seluruh `/16`; scan host yang relevan, catat hop dan waktu.
5. Setelah database terlihat, pilih jalur: kredensial dari share, atau PostgreSQL dengan `trust`/kredensial lemah.
6. Bukti pivot: `ip route` sebelum/sesudah dan koneksi sukses ke port target.

**Keputusan:** Ligolo-ng untuk hop 1, agent kedua di file server untuk hop 2, verifikasi dengan `nc -vz` sebelum scan.

**Pelajaran:** tunnel yang benar menghilangkan sebagian besar masalah "tool tidak jalan".

## Skenario 4 — Hash kerberoast dan CA kedua

**Data:** Satu hash Kerberoast AES256 diperoleh. Cracking berjalan lambat. Di sisi lain, `certipy find` menemukan CA dengan template ESC1.

**Junior:** Menunggu hashcat selesai berjam-jam sambil menjalankan scan berulang.

**Expert:**

1. Hitung nilai per jam: hash AES256 dengan password panjang bisa tidak pernah pecah; ADCS ESC1 memberi jalur langsung ke impersonasi.
2. Jangan matikan cracking — pindahkan ke background, lanjutkan jalur ADCS.
3. ESC1 butuh hak enroll dan SAN yang bisa diisi; verifikasi dengan `certipy req -upn administrator@domain`.
4. Risiko: penerbitan sertifikat tercatat (4886/4887). Catat sebagai bagian dampak.
5. Jika ESC1 berhasil, objective tercapai tanpa menunggu hash.

**Keputusan:** jalankan ADCS sebagai jalur utama, cracking sebagai cadangan; hentikan cracking jika tiket/sertifikat sudah memberi akses.

**Pelajaran:** jalur tercepat bukan selalu jalur yang paling dikenal; hitung biaya dan hentikan pekerjaan yang nilai marginalnya rendah.

## Pola yang bisa diambil

| Situasi | Pertanyaan kunci |
|---|---|
| Banyak jalur tersedia | Mana yang paling murah menuju objective? |
| Satu jalur macet | Apakah masalahnya tool, jaringan, atau kredensial? |
| Bukti sudah cukup | Apakah menambah akses menambah nilai? |
| Waktu terbatas | Apa yang harus didokumentasikan lebih dulu? |

## Best Practices

- Tulis alasan keputusan, bukan hanya hasilnya.
- Uji hipotesis termurah lebih dulu, setiap kali.
- Jangan biarkan satu jalur menahan seluruh engagement.
- Bukti yang cukup lebih baik daripada akses yang berlebihan.
