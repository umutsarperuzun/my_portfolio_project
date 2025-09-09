# Portfolio Deployment Guide

## 1. Sunucu Hazırlığı

### Ubuntu/Debian için:
```bash
# Sistem güncellemesi
sudo apt update && sudo apt upgrade -y

# Python ve pip kurulumu
sudo apt install python3 python3-pip python3-venv -y

# PostgreSQL kurulumu
sudo apt install postgresql postgresql-contrib -y

# Nginx kurulumu
sudo apt install nginx -y

# Git kurulumu
sudo apt install git -y
```

## 2. Proje Kurulumu

```bash
# Projeyi klonla
git clone <your-repo-url>
cd django_portfolio

# Sanal ortam oluştur
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları kur
pip install -r requirements_production.txt
```

## 3. Veritabanı Kurulumu

```bash
# PostgreSQL'e bağlan
sudo -u postgres psql

# Veritabanı ve kullanıcı oluştur
CREATE DATABASE portfolio_db;
CREATE USER portfolio_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;
\q
```

## 4. Ortam Değişkenleri

```bash
# .env dosyası oluştur
cp env.example .env
nano .env

# Aşağıdaki değerleri doldur:
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=portfolio_db
DB_USER=portfolio_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

## 5. Django Ayarları

```bash
# Production ayarlarını kullan
export DJANGO_SETTINGS_MODULE=config.settings_production

# Migrasyonları çalıştır
python manage.py makemigrations
python manage.py migrate

# Süper kullanıcı oluştur
python manage.py createsuperuser

# Statik dosyaları topla
python manage.py collectstatic --noinput

# Tailwind CSS'i derle
python manage.py tailwind build
```

## 6. Gunicorn Konfigürasyonu

```bash
# Gunicorn config dosyası oluştur
nano gunicorn.conf.py
```

```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
```

## 7. Systemd Service

```bash
# Service dosyası oluştur
sudo nano /etc/systemd/system/portfolio.service
```

```ini
[Unit]
Description=Portfolio Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/django_portfolio
Environment="PATH=/path/to/your/django_portfolio/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=config.settings_production"
ExecStart=/path/to/your/django_portfolio/venv/bin/gunicorn --config gunicorn.conf.py config.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Service'i etkinleştir
sudo systemctl daemon-reload
sudo systemctl enable portfolio
sudo systemctl start portfolio
```

## 8. Nginx Konfigürasyonu

```bash
# Nginx config oluştur
sudo nano /etc/nginx/sites-available/portfolio
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/your/django_portfolio;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        root /path/to/your/django_portfolio;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Site'ı etkinleştir
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 9. SSL Sertifikası (Let's Encrypt)

```bash
# Certbot kurulumu
sudo apt install certbot python3-certbot-nginx -y

# SSL sertifikası al
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Otomatik yenileme test et
sudo certbot renew --dry-run
```

## 10. Firewall Ayarları

```bash
# UFW firewall kurulumu
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 11. Monitoring ve Loglar

```bash
# Log dizini oluştur
mkdir -p logs

# Service durumunu kontrol et
sudo systemctl status portfolio
sudo systemctl status nginx

# Logları izle
sudo journalctl -u portfolio -f
tail -f logs/django.log
```

## 12. Güncelleme Süreci

```bash
# Yeni kodları çek
git pull origin main

# Sanal ortamı aktifleştir
source venv/bin/activate

# Bağımlılıkları güncelle
pip install -r requirements_production.txt

# Migrasyonları çalıştır
python manage.py migrate

# Statik dosyaları topla
python manage.py collectstatic --noinput

# Tailwind'i derle
python manage.py tailwind build

# Service'i yeniden başlat
sudo systemctl restart portfolio
```

## Popüler Hosting Alternatifleri:

### 1. DigitalOcean App Platform
- GitHub'a push yap, otomatik deploy
- PostgreSQL add-on
- SSL otomatik

### 2. Railway
- GitHub entegrasyonu
- PostgreSQL add-on
- Otomatik SSL

### 3. Heroku
- Git-based deployment
- PostgreSQL add-on
- SSL otomatik

### 4. Vercel (Frontend için)
- Static site hosting
- GitHub entegrasyonu

## Önemli Notlar:

1. **SECRET_KEY**'i mutlaka değiştir
2. **DEBUG=False** production'da
3. **ALLOWED_HOSTS**'i domain'ine göre ayarla
4. **Database backup** almayı unutma
5. **Log monitoring** yap
6. **SSL sertifikası** kullan
7. **Environment variables** güvenli tut

## Sorun Giderme:

```bash
# Service logları
sudo journalctl -u portfolio -n 50

# Nginx logları
sudo tail -f /var/log/nginx/error.log

# Django logları
tail -f logs/django.log

# Port kontrolü
sudo netstat -tlnp | grep :8000
```
