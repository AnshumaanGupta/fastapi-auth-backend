#!/bin/bash

# DigitalOcean Deployment Script for Backend Authentication API
# Run this on the DigitalOcean droplet

echo "🚀 Starting deployment of Backend Authentication API..."

# Update system packages
echo "📦 Updating system packages..."
apt-get update
apt-get upgrade -y

# Install Python 3.11 and pip
echo "🐍 Installing Python 3.11..."
apt-get install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update
apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install other dependencies
echo "📚 Installing system dependencies..."
apt-get install -y git curl nginx supervisor postgresql-client

# Create application directory
echo "📁 Setting up application directory..."
mkdir -p /var/www/backendauth
cd /var/www/backendauth

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Copy application files (files will be uploaded separately)
echo "📋 Application files should be uploaded to /var/www/backendauth/"

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create systemd service file
echo "⚙️ Creating systemd service..."
cat > /etc/systemd/system/backendauth.service << 'EOF'
[Unit]
Description=Backend Authentication API
After=network.target

[Service]
Type=exec
User=root
WorkingDirectory=/var/www/backendauth
Environment=PATH=/var/www/backendauth/venv/bin
ExecStart=/var/www/backendauth/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx configuration
echo "🌐 Configuring Nginx..."
cat > /etc/nginx/sites-available/backendauth << 'EOF'
server {
    listen 80;
    server_name 209.38.123.128;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Handle CORS preflight requests
    location ~* \.(eot|ttf|woff|woff2)$ {
        add_header Access-Control-Allow-Origin *;
    }
}
EOF

# Enable Nginx site
ln -sf /etc/nginx/sites-available/backendauth /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test and reload Nginx
nginx -t
systemctl reload nginx

# Set up firewall
echo "🔒 Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Start and enable services
echo "🚀 Starting services..."
systemctl daemon-reload
systemctl enable backendauth
systemctl enable nginx
systemctl start nginx

# Set permissions
chown -R root:root /var/www/backendauth
chmod -R 755 /var/www/backendauth

echo "✅ Deployment script completed!"
echo "📝 Next steps:"
echo "1. Upload your application files to /var/www/backendauth/"
echo "2. Create /var/www/backendauth/.env with your configuration"
echo "3. Run: systemctl start backendauth"
echo "4. Check status: systemctl status backendauth"
echo "5. View logs: journalctl -u backendauth -f"
