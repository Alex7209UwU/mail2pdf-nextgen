# Mail2PDF NextGen - Server Deployment Guide

**Deploy on Linux, macOS, or Windows Servers**

---

## 🖥️ System Requirements

### Minimum
- CPU: 1 core
- RAM: 1GB
- Disk: 500MB
- Python: 3.8+
- OS: Linux, macOS, Windows

### Recommended
- CPU: 2+ cores
- RAM: 2GB
- Disk: 2GB
- Python: 3.11
- OS: Ubuntu 20.04 LTS

---

## 🐧 Linux Deployment

### Ubuntu/Debian

#### 1. Update System

```bash
sudo apt update
sudo apt upgrade -y
```

#### 2. Install Python & Dependencies

```bash
sudo apt install -y python3.11 python3.11-venv python3-pip
sudo apt install -y libcairo2 libpango-1.0-0 libpangoft2-1.0-0
sudo apt install -y git curl
```

#### 3. Setup Application

```bash
# Create app directory
sudo mkdir -p /opt/mail2pdf-nextgen
sudo chown $USER:$USER /opt/mail2pdf-nextgen
cd /opt/mail2pdf-nextgen

# Clone repository
git clone https://github.com/yourusername/mail2pdf-nextgen.git .

# Create virtualenv
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure Service

Create `/etc/systemd/system/mail2pdf.service`:

```ini
[Unit]
Description=Mail2PDF NextGen Web Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/mail2pdf-nextgen
Environment="PATH=/opt/mail2pdf-nextgen/venv/bin"
ExecStart=/opt/mail2pdf-nextgen/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 5. Enable & Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable mail2pdf
sudo systemctl start mail2pdf

# Check status
sudo systemctl status mail2pdf

# View logs
sudo journalctl -u mail2pdf -f
```

#### 6. Setup Nginx Reverse Proxy

Install nginx:
```bash
sudo apt install -y nginx
```

Create `/etc/nginx/sites-available/mail2pdf`:

```nginx
upstream mail2pdf {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://mail2pdf;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    client_max_body_size 100M;
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/mail2pdf \
  /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. HTTPS with Let's Encrypt

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.com

# Auto-renew
sudo systemctl enable certbot.timer
```

---

## 🍎 macOS Deployment

### 1. Install Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Dependencies

```bash
brew install python@3.11
brew install cairo pango libffi
```

### 3. Setup Application

```bash
mkdir -p ~/Applications/mail2pdf-nextgen
cd ~/Applications/mail2pdf-nextgen

git clone https://github.com/yourusername/mail2pdf-nextgen.git .

python3 -m venv venv
source venv/bin/activate

pip install -upgrade pip
pip install -r requirements.txt
```

### 4. Create LaunchAgent

Create `~/Library/LaunchAgents/com.mail2pdf.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mail2pdf.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/USERNAME/Applications/mail2pdf-nextgen/venv/bin/python</string>
        <string>/Users/USERNAME/Applications/mail2pdf-nextgen/app.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/USERNAME/Applications/mail2pdf-nextgen</string>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutput</key>
    <string>/var/log/mail2pdf.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.mail2pdf.plist

# Check status
launchctl list | grep mail2pdf
```

### 5. Setup Nginx

```bash
brew install nginx

# Edit /usr/local/etc/nginx/nginx.conf
# Add server configuration (same as Linux)

# Start nginx
brew services start nginx
```

---

## 🪟 Windows Deployment

### 1. Install Python

- Download from https://www.python.org/downloads/
- During installation: ✓ Add Python to PATH
- Verify: `python --version`

### 2. Install Dependencies

Open PowerShell as Administrator:

```powershell
pip install --upgrade pip
pip install -r requirements.txt

# For WeasyPrint on Windows:
pip install --upgrade weasyprint
```

### 3. Install as Service

Option A: Using NSSM (Non-Sucking Service Manager)

```powershell
# Download NSSM
# https://nssm.cc/download

# Register service
nssm install Mail2PDF C:\path\to\python.exe C:\path\to\app.py

# Start service
nssm start Mail2PDF

# Check status
nssm status Mail2PDF
```

Option B: Using Task Scheduler

1. Open Task Scheduler
2. Create Basic Task: "Mail2PDF"
3. Trigger: "At startup"
4. Action: Start program
   - Program: `C:\Python311\python.exe`
   - Arguments: `C:\path\to\app.py`
5. Enable task

### 4. Setup IIS (Optional)

```powershell
# Install IIS
Install-WindowsFeature Web-Server, Web-CGI, Web-Request-Monitor

# Configure FastCGI
# Use wfastcgi or similar
```

Or simpler: Use Nginx on Windows:
- Download from https://nginx.org/en/download.html
- Configure as proxy (see Linux config)

---

## 🔧 Configuration

### Environment Variables

#### Linux
Edit `.bashrc` or `.bash_profile`:

```bash
export MAIL2PDF_ENV=production
export FLASK_ENV=production
export MAIL2PDF_DEBUG=false
```

#### macOS
Edit `~/.zshrc`:

```bash
export MAIL2PDF_ENV=production
export FLASK_ENV=production
```

#### Windows PowerShell
```powershell
$env:MAIL2PDF_ENV='production'
$env:FLASK_ENV='production'
```

### Config File

Create `config.local.py`:

```python
import os

PDF_CONFIG = {
    'page_size': 'A4',
    'quality': 300,
}

FLASK_CONFIG = {
    'host': '0.0.0.0',
    'port': int(os.getenv('PORT', 5000)),
    'debug': False,
}

EMAIL_CONFIG = {
    'max_body_length': 50000,
}
```

Use it:
```bash
python main.py --config config.local.py
```

---

## 📊 Monitoring

### Health Check

```bash
# Linux
curl -f http://localhost:5000/ || systemctl restart mail2pdf

# macOS
curl -f http://localhost:5000/ || launchctl stop com.mail2pdf.app

# Windows
invoke-webrequest http://localhost:5000/
```

### Logging

#### Linux (systemd)

```bash
# View logs
journalctl -u mail2pdf -f

# Last 100 lines
journalctl -u mail2pdf -n 100

# Export
journalctl -u mail2pdf > mail2pdf.log
```

#### Application Logs

```bash
# Run with verbose
python app.py --verbose

# Logs written to mail2pdf.log
tail -f mail2pdf.log
```

---

## 📈 Performance Tuning

### Gunicorn (Production WSGI)

```bash
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or with config file
gunicorn -c gunicorn.conf.py app:app
```

Create `gunicorn.conf.py`:

```python
workers = 4
worker_class = "sync"
bind = "0.0.0.0:5000"
timeout = 300
access_log = "/var/log/mail2pdf/access.log"
error_log = "/var/log/mail2pdf/error.log"
```

### Nginx Optimization

```nginx
upstream mail2pdf {
    least_conn;
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://mail2pdf;
        proxy_buffering on;
        proxy_buffer_size 4k;
    }
}
```

---

## 🔐 Security Hardening

### Firewall

#### Linux (UFW)

```bash
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 5000/tcp # App (internal only)
```

#### Windows (Windows Defender Firewall)

```powershell
# Allow app
netsh advfirewall firewall add rule `
  name="Mail2PDF" dir=in action=allow `
  program="C:\path\to\python.exe"
```

### HTTPS/SSL

Always use HTTPS in production!

```bash
# Let's Encrypt (Linux)
certbot certonly --standalone -d example.com
```

---

## 🚀 Scaling

### Load Balanced Setup

```
┌─────────────────┐
│    Nginx LB     │
├─────┬─────┬─────┤
│ App │ App │ App │
│ :5000 :5001 :5002 │
└─────┴─────┴─────┘
```

Run multiple instances:

```bash
# Terminal 1
FLASK_ENV=production python app.py

# Terminal 2
FLASK_ENV=production PORT=5001 python app.py

# Terminal 3
FLASK_ENV=production PORT=5002 python app.py
```

Configure Nginx as above.

---

## 🧹 Backup & Maintenance

### Regular Backups

```bash
# Backup application
tar -czf mail2pdf-$(date +%Y%m%d).tar.gz /opt/mail2pdf-nextgen

# Backup data
tar -czf mail2pdf-data-$(date +%Y%m%d).tar.gz data/

# Push to S3
aws s3 cp mail2pdf-*.tar.gz s3://backups/
```

### Updates

```bash
cd /opt/mail2pdf-nextgen
git pull origin main
pip install --upgrade -r requirements.txt
systemctl restart mail2pdf
```

---

## 🆘 Troubleshooting

**Port already in use:**
```bash
sudo lsof -i :5000
sudo kill -9 <PID>
```

**Permission denied:**
```bash
sudo chown www-data:www-data /opt/mail2pdf-nextgen
```

**OutOfMemory:**
```bash
# Increase swap (Linux)
sudo dd if=/dev/zero of=/swapfile bs=1G count=2
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

**Server Deployment Guide Complete!**
