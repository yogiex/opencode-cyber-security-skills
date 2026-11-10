---
name: "Mindset — Dua Belas Hukum dan Enam Refleks"
description: "Mindset operator CPENT dalam bentuk hukum yang ringkas dan tegas: objective, graf, bukti, biaya, asumsi, peta, kredensial, topologi, noise, berhenti, keheningan, dan penjelasan — plus refleks otomatis dan lima pertanyaan wajib sebelum aksi."
tags: [mindset, laws, heuristics, principles, decision-making, reflexes]
---

# Mindset

Mindset bukan daftar nasihat. Ini hukum yang menentukan bagaimana target dibaca dan kapan langkah diambil. Pelanggaran satu hukum biasanya cukup untuk membuat pekerjaan tidak bisa dipertanggungjawabkan.

## Dua Belas Hukum

1. **Objective dulu, tool kemudian.** Tanpa objective yang jelas, tidak ada prioritas — hanya aktivitas. Tanyakan objective sebelum memilih alat.

2. **Target adalah graf.** Nilai ada di edge: reachability, kredensial, trust, konfigurasi. Host yang membosankan tetap bernilai jika ia edge. Jangan menilai host dari layanannya.

3. **Bukti adalah produk.** Akses tanpa bukti bukan temuan. Bukti diambil saat akses masih hidup; rekonstruksi selalu kehilangan konteks.

4. **Cara termurah menang.** Untuk nilai yang sama, pilih biaya terkecil: waktu, noise, risiko produksi. Mahal bukan berarti lebih benar.

5. **Asumsi harus bisa difalsifikasi.** Yang tidak bisa diuji bukan asumsi, melainkan harapan. Tulis asumsi, tulis cara membantahnya.

6. **Setiap shell adalah peta baru.** Sebelum langkah berikutnya: antarmuka, route, ARP, DNS, share, sesi. Host dual-homed adalah jembatan, bukan akhir.

7. **Kredensial adalah jalan pintas.** Satu kredensial yang valid memangkas tiga hop. Uji reuse dengan sadar lockout; jangan bakar kredensial di satu layanan.

8. **Pivot adalah topologi, bukan tool.** Pilih Ligolo-ng, Chisel, atau SSH setelah memahami jalur dan egress — bukan sebaliknya.

9. **Noise adalah anggaran.** Setiap aksi berbiaya deteksi. Belanjakan pada jalur menuju objective, sisakan untuk verifikasi dan bukti.

10. **Berhenti adalah keputusan.** Ketika nilai marginal < risiko marginal, berhenti dan lapor. Menambah akses tanpa menambah nilai adalah kerugian.

11. **Keheningan bukan jawaban.** Tidak ada respons punya tiga kemungkinan: host mati, firewall stateful, filter aplikasi. Uji satu per satu, jangan menyimpulkan.

12. **Jelaskan mengapa, atau jangan klaim.** Keberhasilan yang tidak bisa dijelaskan bukan temuan; kegagalan yang tidak dipahami akan terulang.

## Enam Refleks

Refleks dijalankan tanpa perlu diputuskan lagi:

1. **Cek otorisasi** sebelum paket pertama.
2. **Catat waktu dan perintah** setiap kali akses berubah.
3. **Baca versi dan konfigurasi** sebelum mencari CVE.
4. **Stabilkan shell** sebelum mengambil bukti.
5. **Simpan bukti** sebelum pindah target.
6. **Bersihkan artefak** sebelum keluar.

## Lima Pertanyaan Wajib

Sebelum aksi yang mengubah state target:

1. Objective apa yang dilayani aksi ini?
2. Edge mana yang saya dapat atau hilang?
3. Apa blast radius-nya jika gagal?
4. Bukti apa yang harus saya ambil sesudahnya?
5. Apakah saya akan berhenti setelah ini — dan mengapa?

Jika salah satu tidak bisa dijawab, aksi ditunda dan enumerasi dilanjutkan.

## Hukum versus preferensi

- Hukum tidak bisa dinegosiasikan oleh kenyamanan atau kebiasaan tool.
- Hukum boleh dilanggar hanya jika aturan engagement (RoE) secara eksplisit meminta, dan pelanggaran itu dicatat di laporan.
- Preferensi (tool, urutan, gaya) bebas berubah selama hukum dipenuhi.

## Best Practices

- Hafalkan dua belas hukum; jangan cari daftar saat di tengah engagement.
- Gunakan hukum untuk membenarkan atau membatalkan langkah, bukan untuk menghias laporan.
- Jika dua hukum tampak bertentangan, menangkan yang melindungi bukti dan otorisasi.
- Detail panjang ada di [expert-reasoning.md](./expert-reasoning.md); bentuk keputusan ada di [decision-trees.md](./decision-trees.md).
