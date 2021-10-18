kahraba deploy 
1. connect as root 
2. create taki user 
3. connect with taki pw:20905991
4. # sudo apt update
     sudo apt upgrade
5. CREATE DATABASE kahraba_7000;
CREATE USER taki WITH PASSWORD 'miyou0209';
# if postgres exist use ALTER instead of CREATE

ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE kahraba_7000 TO postgres;

# cairo error 
solution:
sudo apt-get install libpangocairo-1.0-0

ig gunicorn --bind 0.0.0.0:8000 config.wsgi => error import 
ceci veut dire qui y'a un probleme de relative and absolute error 

voic

PYTHONPATH=`pwd`/.. gunicorn --bind 0.0.0.0:8000 config.wsgi:application

9.quit venv 

10. open gunicorn.socket file :
sudo nano /etc/systemd/system/gunicorn.socket ->

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target

# sudo nano /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=taki
Group=www-data
WorkingDirectory=/home/taki/kahraba/kahraba
ExecStart=/home/taki/kahraba/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target

...

# NGINX

sudo nano /etc/nginx/sites-available/kahraba

server {
    listen 80;
    server_name 167.99.203.219;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/taki/kahraba/kahraba;
    }
    
    location /media/ {
        root /home/taki/kahraba/kahraba;    
    }
    location /assets/ {
        root /home/taki/kahraba/kahraba;    
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

## add ssl

create ssl dir with # mkdir ssl 

gneerate ceritficat with 

> sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/kahraba.key -out ssl/kahraba.crt

ajouter a nginx 
>listen 443 ssl;
ssl_certificate /home/taki/kahraba/kahraba/ssl/kahraba.crt;
ssl_certificate_key /home/taki/kahraba/kahraba/ssl/kahraba.key;



 sudo ln -s /etc/nginx/sites-available/kahraba /etc/nginx/sites-enabled


# not loaded images 
> swithed on nginx conf from statis to assets
> admin css not found 



NGINX COMMANDS 
status:
    sudo systemctl status nginx

stop :
    sudo systemctl stop nginx

start:
    sudo systemctl start nginx

restart :
    sudo systemctl reload nginx

Force Restart:
    sudo systemctl restart nginx

useful link to now more about nginx commands : https://phoenixnap.com/kb/nginx-start-stop-restart

gunicorn commands

restart :
sudo systemctl restart gunicorn


# ADMIN CSS error solved

> changed static_files root from assets to static and removed stativ files dirs on prod
>  vdvv
+ wscs
+ sdcfdsc



ALLOWED_HOSTS = ['167.99.203.219', 'www.shop.kahrabacenter.com', 'shop.kahrabacenter.com]

shop.kahrabacenter.com www.shop.kahrabacenter.com 

ALLOWED_HOSTS = ['167.99.203.219', 'shop.kahrabacenter.com', 'www.shop.kahrabacenter.com']