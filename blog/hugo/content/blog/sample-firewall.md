+++
date = '2025-12-18T23:25:46+01:00'
draft = false
title = 'Sample VPS Firewall Settings'
summary = "Minimize your Virtual Private Server's attack surface"
tags = ['website-hosting']
+++

As said [here](https://askubuntu.com/a/1128560),
it's a good idea to run ufw on your virtual private server.
Here are recommended baseline settings that allow
HTTP, HTTPS and SSH connections, and nothing else:

```
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```
