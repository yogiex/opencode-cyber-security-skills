---
name: "Cloud, Virtual, and Wireless Network Protection"
description: "Pertahanan lingkungan non-tradisional: tanggung jawab bersama cloud, kontrol identitas dan eksposur, desain VPC, baseline container/Kubernetes, risiko SDN/NFV dan virtualisasi, serta keamanan wireless enterprise."
tags: [cloud, aws, azure, gcp, iam, security-group, kubernetes, container, sdn, nfv, wireless, wpa3]
---

# Cloud, Virtual, and Wireless Network Protection

Di lingkungan ini, "jaringan" sering tidak terlihat: tidak ada kabel yang dicabut, tidak ada switch yang diubah. Defender harus berpindah dari mengelola perangkat ke mengelola **identitas, kebijakan, dan eksposur**.

## 1. Tanggung jawab bersama

| Lapisan | Penyedia | Pelanggan |
|---|---|---|
| Fasilitas, hardware, hypervisor | ya | — |
| Jaringan virtual, API kontrol | ya | konfigurasi |
| Identitas dan akses | menyediakan alat | **kebijakan** |
| Data, konfigurasi, patch guest | — | **penuh** |

Kesalahan paling umum: menganggap "cloud aman" atau "cloud milik penyedia". Kebocoran hampir selalu berasal dari konfigurasi pelanggan.

## 2. Identitas lebih dulu

- **IAM** adalah perimeter baru: role, policy, dan kredensial menentukan akses.
- Hindari kunci akses statis jangka panjang; gunakan role dan kredensial sementara.
- **Least privilege** pada policy; audit yang memberi `*` pada resource atau action.
- **MFA** untuk akun admin dan akses konsol.
- Pisahkan akun/proyek per lingkungan (produksi vs non-produksi).

## 3. Eksposur publik

- **Storage** (S3 bucket, blob, GCS): cek kebijakan publik, ACL, dan snapshot publik.
- **Metadata service**: paksa IMDSv2; SSRF ke metadata adalah jalur kredensial klasik.
- **Snapshot dan image** bisa memuat data sensitif dan sering terlewat.
- **Manajemen dan CI/CD** yang terbuka ke internet adalah target bernilai tinggi.

## 4. Jaringan di cloud

| Kontrol | Karakter | Catatan |
|---|---|---|
| Security group | stateful, per resource | bukan pengganti identitas; aturan `0.0.0.0/0` perlu alasan |
| NACL | stateless, per subnet | urutan aturan penting, mudah salah |
| Network firewall appliance | terpusat | biaya dan bottleneck |
| VPC peering / transit gateway | konektivitas | perlu kebijakan eksplisit antar-VPC |

Desain minimum: subnet publik hanya untuk load balancer; aplikasi dan data di subnet privat; egress melalui NAT/proxy dengan logging; route table diaudit.

## 5. Container dan Kubernetes (baseline)

- **RBAC** ketat; hindari `cluster-admin` untuk workload.
- **Network policy** sebagai default deny antar-namespace.
- **Image**: registry tepercaya, scanning, tanda tangan/verifikasi, tanpa `latest` di produksi.
- **Secrets** dikelola (KMS/secret manager), bukan di env atau repo.
- **Admission control** untuk mencegah pod privileged dan hostPath sembarangan.
- **Runtime** monitoring dan logging terpusat.

Untuk arsitektur Kubernetes mendalam, gunakan `lf-cks`; di sini cukup baseline operasional.

## 6. SDN, NFV, dan virtualisasi

- **Kontroler terpusat** adalah titik kegagalan dan target bernilai tinggi; batasi akses dan audit perubahannya.
- **Policy drift** mudah terjadi karena perubahan bisa dilakukan lewat API tanpa jejak fisik.
- **VLAN trunk ke hypervisor** dapat mengekspos segmen ke VM yang salah; batasi trunk dan VLAN yang diizinkan.
- **VM sprawl** dan snapshot lama memperluas permukaan; inventaris dan masa berlaku wajib.
- **Hypervisor** diperbarui dan di-hardening; akses manajemen dipisahkan dari jaringan produksi.

## 7. Wireless enterprise

- **WPA3-Enterprise** atau WPA2-Enterprise dengan 802.1X; hindari PSK untuk jaringan korporat.
- **Sertifikat server** divalidasi klien; tanpa itu, evil twin mudah berhasil.
- **Guest network** terisolasi penuh, tanpa akses ke internal.
- **Manajemen perangkat** (controller, AP) di VLAN manajemen, tidak terjangkau user.
- **Rogue AP/WIPS** sebagai sinyal, bukan jaminan; lakukan site survey berkala.
- **Coverage** yang bocor ke luar gedung adalah risiko fisik — sesuaikan daya dan antena.

## 8. Logging dan visibilitas

- Aktifkan **audit log** (CloudTrail/Activity Log/Audit Logs) ke penyimpanan terpisah yang tidak bisa dihapus oleh akun yang diaudit.
- **VPC flow logs** untuk analisis koneksi, bukan pengganti log aplikasi.
- **CSPM** untuk menemukan salah konfigurasi; hasilnya harus punya pemilik dan SLA.
- **Baseline cloud** diperiksa berkala, bukan sekali saat migrasi.

## 9. Kesalahan umum

1. **Security group `0.0.0.0/0`** pada port manajemen "sementara".
2. **Bucket publik** karena kebijakan default yang tidak diperiksa.
3. **IMDSv1** masih aktif dan aplikasi rentan SSRF.
4. **Kunci akses statis** di repo atau image.
5. **Kubernetes tanpa network policy** — semua pod bisa saling bicara.
6. **Guest Wi-Fi** satu subnet dengan jaringan kantor.
7. **Audit log** disimpan di akun yang sama dan bisa dihapus penyerang.

## Best Practices

- Perlakukan identitas sebagai perimeter utama.
- Audit eksposur publik secara berkala, termasuk snapshot dan image.
- Tulis kebijakan cloud sebagai kode dan uji di pipeline.
- Baseline container/Kubernetes secukupnya; rujuk `lf-cks` untuk kedalaman.
- Wireless korporat selalu enterprise-grade, dengan validasi sertifikat.
