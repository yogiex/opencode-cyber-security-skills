# Triage — {{rule_id}} pada {{agent_name}}

> Placeholder `{{...}}` diisi otomatis oleh `scripts/wazuh_triage.py report`. Bagian bukti, verdict, dan tindakan tetap diisi analis.

## Ringkasan

Satu paragraf: apa yang terdeteksi, di mana, kapan, dan verdict-nya.

## Identitas Alert

| Field | Nilai |
|---|---|
| Alert ID | {{alert_id}} |
| Rule | {{rule_id}} — {{rule_description}} |
| Level | {{rule_level}} |
| Agent | {{agent_id}} / {{agent_name}} |
| Waktu (UTC) | {{timestamp}} |
| Sumber log | {{location}} |
| Decoder | {{decoder}} |
| ATT&CK | {{mitre}} |

## Bukti

| # | Bukti | Sumber | Nilai |
|---|---|---|---|
| 1 | Log mentah | full_log | `{{full_log}}` |
| 2 | | | |
| 3 | | | |

## Verdict

**TP / FP / Benign / Unknown** — alasan dalam 1–2 kalimat, sebutkan dua sumber bukti.

## Prioritas

P<n> — level {{rule_level}}, kekritisan aset <kritikal/tidak>, keyakinan bukti <tinggi/sedang/rendah>.

## Tindakan

- [ ] Tutup dengan alasan
- [ ] Monitor sampai <waktu>
- [ ] Eskalasi ke <pemilik> karena <pemicu>
- [ ] Usulan tuning: <ringkas> (change request terpisah)

## IoC

| Tipe | Nilai | Konteks | Keyakinan |
|---|---|---|---|
| | | | |

## Catatan dan Keterbatasan

- Data yang tidak tersedia:
- Redaksi yang dilakukan:
- Pertanyaan yang masih terbuka:
