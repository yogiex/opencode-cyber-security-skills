#!/usr/bin/env python3
"""
OSEP Payload Encoder — XOR encode shellcode to C# / PowerShell / VBA formats.

Usage:
    python payload-encoder.py shellcode.bin --key 0xAA --format csharp
    python payload-encoder.py shellcode.bin --key 0xBB --format powershell
    python payload-encoder.py shellcode.bin --key 0xCC --format vba
"""

import argparse
import sys


def encode_shellcode(data: bytes, key: int) -> list:
    return [b ^ key for b in data]


def format_csharp(encoded: list) -> str:
    hex_bytes = ", ".join(f"0x{b:02x}" for b in encoded)
    return f"byte[] buf = new byte[] {{ {hex_bytes} }};"


def format_powershell(encoded: list) -> str:
    return "[Byte[]] @(" + ", ".join(f"0x{b:02x}" for b in encoded) + ")"


def format_vba(encoded: list) -> str:
    chunks = [", ".join(map(str, encoded[i:i+10])) for i in range(0, len(encoded), 10)]
    return "buf = Array(" + ", _\n  ".join(chunks) + ")"


def format_raw(encoded: list) -> bytes:
    return bytes(encoded)


def main():
    parser = argparse.ArgumentParser(description="OSEP Payload Encoder")
    parser.add_argument("input", help="Raw shellcode binary file")
    parser.add_argument("--key", type=lambda x: int(x, 0), default=0xAA,
                        help="XOR key (default: 0xAA)")
    parser.add_argument("--format", choices=["csharp", "powershell", "vba", "raw"],
                        default="csharp", help="Output format")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    with open(args.input, "rb") as f:
        shellcode = f.read()

    encoded = encode_shellcode(shellcode, args.key)

    if args.format == "raw":
        output = format_raw(encoded)
        mode = "wb"
    else:
        formatters = {
            "csharp": format_csharp,
            "powershell": format_powershell,
            "vba": format_vba,
        }
        output = formatters[args.format](encoded)
        mode = "w"

    if args.output:
        with open(args.output, mode) as f:
            f.write(output)
        print(f"[+] Wrote {len(encoded)} bytes to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
