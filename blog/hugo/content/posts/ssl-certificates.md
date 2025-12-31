+++
date = '2025-01-20T23:25:55+01:00'
draft = false
title = "Install Free SSL Certificate Using Let's Encrypt"
+++

# Install certificate as seen in [tutorial](https://www.youtube.com/watch?v=XxMbLr4ytCM)

1. Go to [ACME Github repo](https://github.com/acmesh-official/acme.sh)
1. Download ACME install script and run it. This creates `acme.sh`
1. `mkdir ~/pub && cd ~/pub && python3 -m http.server 8000`
1. In `~/pub/`: put the following into `nginx.conf`:
```
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://172.17.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
then run: `docker run -p 80:80 -v $(pwd)/nginx.conf:/etc/nginx/conf.d/default.conf:ro nginx`

5. **To get a new certificate**: Run `./acme.sh --issue -d loic.lescoat.me -d www.loic.lescoat.me -w ~/pub/ --server letsencrypt`. Replace the `-d` arguments as required.
**To update an existing certificate**: Run `acme.sh --renew -d loic.lescoat.me [-d lescoat.me] [--force]`.
1. Stop HTTP server
1. In `nginx`, pass `acme`'s `full-chain cert` (full-chain certificate) to `ssl_certificate` and the `cert key` (private key) to `ssl_certificate_key`:
```
server {
    listen 0.0.0.0:443 ssl;
    listen [::]:443 ssl;

    ssl_certificate /path/to/fullchain.cer;
    ssl_certificate_key /path/to/loic.lescoat.me.key;
    ...
}
```

