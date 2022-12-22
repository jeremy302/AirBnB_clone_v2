#!/usr/bin/env bash
# configures server
CONFIG="
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        # root /var/www/alx-1/html;
        index index.html index.htm index.nginx-debian.html;

        server_name _;
        error_page 404 /404.html;
        rewrite ^/redirect_me / permanent;

        location / {
                try_files \$uri \$uri/ =404;
        }
        location /hbnb_static/ {
                alias /data/web_static/current/;
                try_files \$uri \$uri/ =404;
        }
}
"
sudo apt-get update
which nginx || sudo apt-get -y install nginx

sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo 'Test content' | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test /data/web_static/current

sudo chown -R ubuntu:ubuntu /data
echo -e "$CONFIG" | sudo tee /etc/nginx/sites-available/default

if pgrep nginx; then sudo nginx -s reload; else sudo nginx; fi
