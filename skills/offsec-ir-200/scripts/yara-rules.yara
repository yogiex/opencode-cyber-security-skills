/*
 * OSIR YARA Rules — IR-200 Malware Triage
 * Place in /tmp/yara/ and run:
 *   yara -s /tmp/yara/rules.yara suspicious.exe
 */

rule SuspiciousPowerShell {
    meta:
        description = "Detects suspicious PowerShell usage"
        author = "OSIR Analyst"
        date = "2026-06"
        severity = "medium"
    strings:
        $enc = "-enc" nocase
        $iex = "IEX" nocase
        $download = "DownloadString" nocase
        $hidden = "-WindowStyle Hidden" nocase
        $exec_policy = "-ExecutionPolicy Bypass" nocase
    condition:
        any of ($enc, $iex, $hidden, $exec_policy) and $download
}

rule Mimikatz {
    meta:
        description = "Detects Mimikatz references in memory or disk"
        author = "OSIR Analyst"
        date = "2026-06"
        severity = "critical"
    strings:
        $s1 = "mimikatz"
        $s2 = "sekurlsa"
        $s3 = "logonpasswords"
        $s4 = "privilege::debug"
        $s5 = "kerberos::golden"
        $s6 = "lsadump::dcsync"
    condition:
        2 of them
}

rule C2Domain {
    meta:
        description = "Detects potential C2 domains in memory or files"
        author = "OSIR Analyst"
        date = "2026-06"
        severity = "high"
    strings:
        $ip = /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/
        $long_domain = /[a-z0-9]{20,}\.(com|net|xyz|top|club)/
        $dga_like = /[a-z]{5,}\.[a-z]{2,3}\/[a-z0-9]{8,}/
    condition:
        $long_domain or #ip > 5 or $dga_like
}

rule RansomwareNote {
    meta:
        description = "Detects common ransomware note strings"
        author = "OSIR Analyst"
        date = "2026-06"
        severity = "critical"
    strings:
        $note1 = "Your files have been encrypted" nocase
        $note2 = "Your documents are encrypted" nocase
        $note3 = "your data has been stolen" nocase
        $note4 = "bitcoin" nocase
        $note5 = "torproject" nocase
        $note6 = "README" nocase
    condition:
        any of ($note1, $note2, $note3) or ($note4 and $note5)
}

rule ProcessInjection {
    meta:
        description = "Detects process injection indicators in memory"
        author = "OSIR Analyst"
        date = "2026-06"
        severity = "critical"
    strings:
        $createRemote = "CreateRemoteThread" nocase
        $virtualProtect = "VirtualProtectEx" nocase
        $writeProcess = "WriteProcessMemory" nocase
        $allocMem = "VirtualAllocEx" nocase
        $openProcess = "OpenProcess" nocase
    condition:
        3 of them
}

rule BeaconConfig {
    meta:
        description = "Detects C2 beacon configuration patterns"
        author = "OSIR Analyst"
        date = "2026-06"
        severity = "high"
    strings:
        $sleep = /\d{2,6}\s*(seconds|minutes|ms)/i
        $jitter = /jitter/i
        $c2_url = /https?:\/\/[a-z0-9\.-]+\/[a-zA-Z0-9\/]+/
        $user_agent = /User-Agent/i
    condition:
        ($sleep or $jitter) and $c2_url
}
