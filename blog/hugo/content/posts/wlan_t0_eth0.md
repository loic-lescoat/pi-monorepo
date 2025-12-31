+++
date = '2024-10-20T23:26:02+01:00'
draft = false
title = 'Raspberry Pi + Ubuntu: Disable Wi-Fi and Enable Ethernet'
summary = "Ensure you use only ethernet, which is more robust than wifi"
tags = ['website-hosting']
+++

# Steps

1. Inspect `eth0` and `wlan0` by running `ifconfig`.
See `wlan0` is `RUNNING` and `eth0` is not.
1. Edit `/etc/netplan/*.yml` to have the following:
```
network:
    version: 2
    ethernets:
      renderer: networkd
      eth0:
        dhcp4: true
```
1. Apply using `sudo netplan apply`
1. Inspect `eth0` and `wlan0`: `ifconfig`.
See `eth0` is `RUNNING` and `wlan0` is not.
