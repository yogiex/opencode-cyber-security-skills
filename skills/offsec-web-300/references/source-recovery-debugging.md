---
name: "Source Recovery & Debugging — Fase Pertama White-Box"
description: "Merekonstruksi source dari artefak terpasang (DLL/EXE, JAR/WAR, class), memetakan route dan entry point dari metadata bytecode, menemukan config dan secret, lalu membuktikan parameter benar-benar terkendali lewat JDWP dan attach dnSpy."
tags: [white-box, decompile, dnSpy, jdwp, ilspy, jadx, cfr, route-mapping, debugging, aspnet, spring, servlet]
---

# Source Recovery & Debugging — Fase Pertama White-Box

Fase pertama white-box bukan "membaca source", melainkan **merekonstruksi source yang tidak diberikan** dari artefak terpasang, lalu memetakan route dari metadata bytecode — bukan dari UI. Setelah route map dan kandidat sink terbentuk, remote debugging dipakai untuk membuktikan satu hal: apakah nilai yang sampai ke sink benar-benar berasal dari request.

Decompiler menghasilkan aproksimasi, bukan source asli. Setiap klaim berhenti di batas yang bisa dibuktikan dengan breakpoint, call stack, dan pasangan request/response.

## 1. Inventaris artefak lebih dulu

Cari binary, bukan file teks:

```bash
unzip -l app.war && jar tf app.jar | grep -E '\.class$|WEB-INF|META-INF'
jd-cli app.jar -od out/                      # atau: jadx -d out app.jar
java -jar cfr.jar app.jar --outputdir out/   # CFR: satu jar sekaligus
ilspycmd -o out app.dll                      # .NET whole-assembly ke C#
ildasm app.dll /text /tokens                 # IL + metadata token
file bin/*.dll                               # managed vs native
```

| Alat | Artefak | Tujuan | Batas yang diakui sumber resmi |
|---|---|---|---|
| dnSpy | `.dll`/`.exe` | decompile **dan** attach debugger, edit assembly | dynamic method tidak bisa di-debug (batas CLR) |
| ILSpy / `ilspycmd` | `.dll`/`.exe`/`.winmd` | decompile whole-project, buka dari proses berjalan (Windows) | — |
| dotPeek | `.dll`/`.exe`/`.winmd` | decompile, export `.csproj`, symbol server | source asli hanya bila PDB tersedia |
| `ildasm` | PE managed | IL + metadata (`/tokens`, `/item`) | hanya file on-disk, bukan GAC; keluaran IL |
| JD-GUI | `.class`/`.jar` | browse GUI cepat | GUI saja, tanpa batch CLI |
| jadx | `.jar`/`.class`/`.aar`/dex | decompile + deobfuscator | butuh Java 11+ 64-bit; "can't decompile 100%" |
| CFR | `.jar`/`.class` | CLI seluruh jar, fitur Java 9–14 | ditulis untuk Java 6; output tetap rekonstruksi |
| Procyon | `.class`/`.jar` | pembanding saat CFR/jadx gagal | — |

## 2. Petakan route dari bytecode

| Framework | Sumber pemetaan | Catatan |
|---|---|---|
| Servlet | `WEB-INF/web.xml`: `<servlet>`, `<servlet-mapping>`, `<filter>`, `<security-constraint>` | urutan filter menentukan auth |
| Servlet annotation | `@WebServlet`, `@WebFilter`, `@Path` | terbaca di metadata sebagai `RuntimeVisibleAnnotations` |
| Spring MVC | `@RequestMapping` class + method **digabung** | Ant pattern, `${...}`, SpEL `#{...}` |
| Struts / JSF | `struts.xml`, `faces-config.xml` | URL hasil navigasi sering tak terlihat |
| ASP.NET Core attribute | `[Route]`, `[HttpGet]`, `[ApiController]` | attribute route tidak tercapai lewat conventional route |
| ASP.NET Core konvensional | `MapControllerRoute`/`MapDefaultControllerRoute` | pola `{controller}/{action}/{id?}` |
| ASP.NET Framework | `web.config` handler/module, `Global.asax`, `RouteConfig` | `.ashx`/`.svc` sering tak tertaut dari UI |
| WCF / ASMX | `.svc` + `[OperationContract]`, `.asmx` + `[WebMethod]` | endpoint SOAP luput dari spider |

Lokasi config dan secret yang diperiksa lebih dulu:

| Berkas | Yang dicari |
|---|---|
| `web.config` | connection string, `<machineKey validationKey/decryptionKey>`, `customErrors` |
| `appsettings*.json` | connection string, signing key, `TypeNameHandling` |
| `WEB-INF/web.xml`, `META-INF/context.xml` | datasource JNDI, `auth-method`, filter |
| `WEB-INF/classes/*.properties`, `*.yml` | password DB, secret JWT, kunci cookie |
| string heap `#US` (IL) | kunci/URL/secret hardcoded di method body |
| ada-tidaknya `*.pdb` | penanda build debug vs release |

## 3. Debugging Java — JDWP

Sub-opsi resmi: `transport`, `server`, `address`, `suspend`, `timeout`, `onthrow`, `onuncaught`.

```bash
java -agentlib:jdwp=transport=dt_socket,server=y,address=127.0.0.1:8000,suspend=n -jar app.jar
jdb -attach 8000                                    # atau IDE: Remote JVM Debug
printf 'JDWP-Handshake' | nc -w 2 127.0.0.1 8000     # cek agent: handshake 14 byte, header 11 byte
```

`suspend=y` adalah default dan menahan VM sebelum main class dimuat — penyebab paling umum "aplikasi hang setelah flag debug ditambahkan". Gunakan `onthrow=<exception>` atau `onuncaught=y` untuk just-in-time debugging. JDWP opsional pada sebagian implementasi JDK, jadi port terbuka bukan jaminan agent aktif.

```java
@WebServlet("/report")
protected void doGet(HttpServletRequest req, HttpServletResponse resp) {
    String name = req.getParameter("name");   // breakpoint di sini
    String cmd = "sh -c 'generate " + name + "'";
    Runtime.getRuntime().exec(cmd);           // sink
}
```

Kirim `?name=CANARY-7731`, saat breakpoint hit bandingkan `name` di Locals dengan nilai request, lalu `step into` ke sink. Call stack harus menunjukkan frame container (`ApplicationFilterChain` → `YourServlet.doGet`); bila frame berasal dari scheduler/internal task, input tidak dikendalikan user.

## 4. Debugging .NET — attach dnSpy

`Debug → Attach to Process`, pilih worker process, aktifkan `Break on module load` untuk menangkap assembly yang dimuat dinamis, lalu breakpoint pada method action. `conditional breakpoint` pada canary unik dan `tracepoint` (mencatat tanpa menghentikan) memetakan parameter tanpa memblokir trafik. `Analyze class and method usage → Find callers` menjawab apakah method pernah dipanggil sebelum Anda menelusurinya.

Menghindari waktu terbuang:

- Buktikan route hidup dengan `curl -i` (200/302/401) sebelum memasang debugger.
- Breakpoint bersyarat pada canary, bukan pada semua request.
- Cek reachability statis sebelum menelusuri cabang `if` yang tidak pernah dieksekusi.
- Untuk endpoint ber-auth, breakpoint pertama sering berhenti di filter — pindahkan setelah otorisasi.

## 5. Bukti yang harus diambil

- Hash dan path artefak (`sha256sum app.dll`), versi alat, perintah decompile.
- Potongan decompiled dengan `file:line`, ditandai sebagai hasil rekonstruksi.
- Nilai parameter, Locals, dan call stack utuh saat breakpoint hit.
- Pasangan request ber-canary ↔ nilai di debugger — bukti parameter terkendali.
- Route map: method, path, parameter, sumber auth, `file:line`, status kandidat/gugur.
- Daftar kandidat gugur beserta alasannya (mis. tidak ter-wire di `web.xml`).

## 6. Jebakan

- **Decompiled ≠ source asli.** `async` menjadi state machine `MoveNext`, lambda menjadi `<>c__DisplayClass`, `switch`/`using` di-lowering, komentar hilang. Jangan kutip nomor baris decompiler sebagai nomor baris build.
- **Release build** menghilangkan PDB/`#line`; inlining mengaburkan alur — jangan simpulkan "tidak ada validasi" dari method yang tampak pendek.
- **Obfuscation** mengganti nama dan bisa mengenkripsi string saat runtime; atribut/route biasanya masih terbaca, secret mungkin baru muncul di memori.
- Jangan simpulkan "tanpa autentikasi" hanya karena tidak ada annotation: auth bisa di filter `web.xml`, middleware, atau interceptor.
- Breakpoint hit ≠ exploitability; JDWP terbuka ≠ RCE tanpa jalur jaringan yang terbukti.
- Jangan klaim secret hardcoded "aktif" sebelum diuji — bisa placeholder atau ditimpa environment.

## 7. Best Practices

- Mulai dari artefak, bukan dari asumsi "source akan diberikan".
- Catat alat dan perintah decompile di laporan; hasil berbeda antar-decompiler.
- Pakai dua decompiler untuk kode yang tampak mencurigakan atau gagal diurai.
- Verifikasi reachability sebelum menelusuri; kode tanpa pemanggil bukan kandidat.
- Simpan canary dan bukti debugger; klaim "parameter terkendali" tanpa itu hanya dugaan.
- Tandai versi alat sebagai bagian dari bukti — hasilnya bergantung versi.

## 8. Rujukan

- [source-review-playbook.md](./source-review-playbook.md) — setelah route ditemukan, telusuri data flow.
- [dotnet-deserialization.md](./dotnet-deserialization.md) — `machineKey` dan ViewState.
- [exploit-development.md](./exploit-development.md) — dari bukti debugger ke script.
- [engagement-playbook.md](./engagement-playbook.md) — bukti dan batas klaim.
