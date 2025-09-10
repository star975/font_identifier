#!/bin/bash

# Font Identifier VPS Deployment Script
# Supports Ubuntu 18.04+, CentOS 7+, and other systemd-based distributions

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="font-identifier"
APP_USER="fontapp"
APP_DIR="/opt/$APP_NAME"
VENV_DIR="$APP_DIR/venv"
SERVICE_NAME="$APP_NAME"
NGINX_AVAILABLE="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"
DOMAIN="${DOMAIN:-localhost}"
EMAIL="${EMAIL:-admin@$DOMAIN}"
PORT="${PORT:-8501}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root (use sudo)"
        exit 1
    fi
}

detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    else
        log_error "Cannot detect OS version"
        exit 1
    fi
    
    log_info "Detected OS: $OS $VER"
}

install_dependencies() {
    log_info "Installing system dependencies..."
    
    if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
        # Ubuntu/Debian
        apt update
        apt install -y python3 python3-pip python3-venv python3-dev \
                      nginx git curl wget unzip supervisor \
                      build-essential libssl-dev libffi-dev \
                      postgresql-client redis-tools \
                      htop nano vim ufw fail2ban
        
        # Install Docker
        if ! command -v docker &> /dev/null; then
            curl -fsSL https://get.docker.com -o get-docker.sh
            sh get-docker.sh
            systemctl enable docker
            systemctl start docker
        fi
        
    elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
        # CentOS/RHEL
        yum update -y
        yum groupinstall -y "Development Tools"
        yum install -y python3 python3-pip python3-devel \
                      nginx git curl wget unzip supervisor \
                      openssl-devel libffi-devel \
                      postgresql redis \
                      htop nano vim firewalld fail2ban
        
        # Install Docker
        if ! command -v docker &> /dev/null; then
            yum install -y yum-utils
            yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
            yum install -y docker-ce docker-ce-cli containerd.io
            systemctl enable docker
            systemctl start docker
        fi
        
    else
        log_error "Unsupported OS: $OS"
        exit 1
    fi
    
    # Install Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi
    
    log_success "Dependencies installed successfully"
}

create_app_user() {
    log_info "Creating application user: $APP_USER"
    
    if ! id "$APP_USER" &>/dev/null; then
        useradd -r -m -s /bin/bash "$APP_USER"
        usermod -aG docker "$APP_USER"
        log_success "User $APP_USER created"
    else
        log_info "User $APP_USER already exists"
    fi
}

setup_application() {
    log_info "Setting up application directory..."
    
    # Create application directory
    mkdir -p "$APP_DIR"
    chown "$APP_USER:$APP_USER" "$APP_DIR"
    
    # Copy application files (assuming current directory contains the app)
    if [ -f "../main.py" ]; then
        log_info "Copying application files..."
        cp -r ../* "$APP_DIR/" 2>/dev/null || true
        chown -R "$APP_USER:$APP_USER" "$APP_DIR"
        
        # Create virtual environment
        log_info "Creating Python virtual environment..."
        sudo -u "$APP_USER" python3 -m venv "$VENV_DIR"
        
        # Install Python dependencies
        log_info "Installing Python dependencies..."
        sudo -u "$APP_USER" "$VENV_DIR/bin/pip" install --upgrade pip
        sudo -u "$APP_USER" "$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt"
        
    else
        log_warning "Application files not found. You'll need to upload them manually to $APP_DIR"
    fi
    
    # Create necessary directories
    sudo -u "$APP_USER" mkdir -p "$APP_DIR/recordings"
    sudo -u "$APP_USER" mkdir -p "$APP_DIR/logs"
    sudo -u "$APP_USER" mkdir -p "$APP_DIR/config"
    
    log_success "Application setup completed"
}

create_systemd_service() {
    log_info "Creating systemd service..."
    
    cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=Font Identifier Web Application
After=network.target

[Service]
Type=exec
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment=PATH=$VENV_DIR/bin
Environment=STREAMLIT_SERVER_PORT=$PORT
Environment=STREAMLIT_SERVER_ADDRESS=127.0.0.1
Environment=STREAMLIT_SERVER_HEADLESS=true
Environment=ENVIRONMENT=production
ExecStart=$VENV_DIR/bin/streamlit run main.py --server.port=$PORT --server.address=127.0.0.1
ExecReload=/bin/kill -HUP \$MAINPID
Restart=always
RestartSec=3
StandardOutput=append:$APP_DIR/logs/app.log
StandardError=append:$APP_DIR/logs/error.log

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd and enable service
    systemctl daemon-reload
    systemctl enable $SERVICE_NAME
    
    log_success "Systemd service created"
}

configure_nginx() {
    log_info "Configuring Nginx..."
    
    # Create Nginx configuration
    cat > $NGINX_AVAILABLE/$APP_NAME << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # File upload limit
    client_max_body_size 100M;
    
    # Proxy to Streamlit
    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 86400;
    }
    
    # WebSocket support for Streamlit
    location /_stcore/stream {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 86400;
    }
    
    # Static files (if any)
    location /static {
        alias $APP_DIR/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

    # Enable the site
    ln -sf $NGINX_AVAILABLE/$APP_NAME $NGINX_ENABLED/$APP_NAME
    
    # Remove default site if it exists
    rm -f $NGINX_ENABLED/default
    
    # Test Nginx configuration
    nginx -t
    
    # Reload Nginx
    systemctl reload nginx
    
    log_success "Nginx configured successfully"
}

setup_ssl() {
    log_info "Setting up SSL certificate with Let's Encrypt..."
    
    # Install Certbot
    if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
        apt install -y certbot python3-certbot-nginx
    elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
        yum install -y certbot python3-certbot-nginx
    fi
    
    # Get SSL certificate
    if [[ "$DOMAIN" != "localhost" ]]; then
        certbot --nginx -d $DOMAIN -d www.$DOMAIN --email $EMAIL --agree-tos --non-interactive
        log_success "SSL certificate installed"
        
        # Setup auto-renewal
        echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
        log_info "SSL auto-renewal configured"
    else
        log_warning "Skipping SSL setup for localhost"
    fi
}

configure_firewall() {
    log_info "Configuring firewall..."
    
    if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
        # Ubuntu/Debian - UFW
        ufw --force enable
        ufw allow ssh
        ufw allow 'Nginx Full'
        ufw allow 80
        ufw allow 443
        ufw reload
        
    elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
        # CentOS/RHEL - firewalld
        systemctl enable firewalld
        systemctl start firewalld
        firewall-cmd --permanent --add-service=ssh
        firewall-cmd --permanent --add-service=http
        firewall-cmd --permanent --add-service=https
        firewall-cmd --permanent --add-port=80/tcp
        firewall-cmd --permanent --add-port=443/tcp
        firewall-cmd --reload
    fi
    
    log_success "Firewall configured"
}

setup_monitoring() {
    log_info "Setting up basic monitoring..."
    
    # Create log rotation
    cat > /etc/logrotate.d/$APP_NAME << EOF
$APP_DIR/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    su $APP_USER $APP_USER
    postrotate
        systemctl reload $SERVICE_NAME
    endscript
}
EOF

    # Create health check script
    cat > $APP_DIR/health_check.sh << 'EOF'
#!/bin/bash
HEALTH_URL="http://127.0.0.1:8501/_stcore/health"
if curl -f -s $HEALTH_URL > /dev/null; then
    echo "$(date): Health check passed"
else
    echo "$(date): Health check failed - restarting service"
    systemctl restart font-identifier
fi
EOF

    chmod +x $APP_DIR/health_check.sh
    chown $APP_USER:$APP_USER $APP_DIR/health_check.sh
    
    # Add to cron for health checks every 5 minutes
    echo "*/5 * * * * $APP_USER $APP_DIR/health_check.sh >> $APP_DIR/logs/health.log 2>&1" >> /etc/crontab
    
    log_success "Monitoring setup completed"
}

start_services() {
    log_info "Starting services..."
    
    # Start and enable services
    systemctl start nginx
    systemctl enable nginx
    systemctl start $SERVICE_NAME
    
    # Wait a moment for the service to start
    sleep 5
    
    # Check service status
    if systemctl is-active --quiet $SERVICE_NAME; then
        log_success "Font Identifier service is running"
    else
        log_error "Font Identifier service failed to start"
        systemctl status $SERVICE_NAME
        exit 1
    fi
    
    if systemctl is-active --quiet nginx; then
        log_success "Nginx is running"
    else
        log_error "Nginx failed to start"
        systemctl status nginx
        exit 1
    fi
}

create_maintenance_scripts() {
    log_info "Creating maintenance scripts..."
    
    # Backup script
    cat > $APP_DIR/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup application data
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz -C /opt/font-identifier .

# Backup database (if using SQLite)
if [ -f "/opt/font-identifier/app_users.db" ]; then
    cp /opt/font-identifier/app_users.db $BACKUP_DIR/db_backup_$DATE.db
fi

# Keep only last 7 backups
find $BACKUP_DIR -name "app_backup_*.tar.gz" -type f -mtime +7 -delete
find $BACKUP_DIR -name "db_backup_*.db" -type f -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

    # Update script
    cat > $APP_DIR/update.sh << 'EOF'
#!/bin/bash
APP_DIR="/opt/font-identifier"
SERVICE_NAME="font-identifier"

cd $APP_DIR

# Pull latest code (if using git)
if [ -d ".git" ]; then
    git pull
fi

# Update Python dependencies
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Restart service
systemctl restart $SERVICE_NAME

echo "Update completed"
EOF

    # Make scripts executable
    chmod +x $APP_DIR/backup.sh
    chmod +x $APP_DIR/update.sh
    chown $APP_USER:$APP_USER $APP_DIR/backup.sh
    chown $APP_USER:$APP_USER $APP_DIR/update.sh
    
    # Schedule daily backups
    echo "0 2 * * * $APP_USER $APP_DIR/backup.sh >> $APP_DIR/logs/backup.log 2>&1" >> /etc/crontab
    
    log_success "Maintenance scripts created"
}

print_summary() {
    log_info "Deployment Summary"
    echo "==================="
    echo "Application: Font Identifier"
    echo "Domain: $DOMAIN"
    echo "Service: $SERVICE_NAME"
    echo "Directory: $APP_DIR"
    echo "User: $APP_USER"
    echo "Port: $PORT"
    echo ""
    echo "Service Commands:"
    echo "  Start:   systemctl start $SERVICE_NAME"
    echo "  Stop:    systemctl stop $SERVICE_NAME"
    echo "  Restart: systemctl restart $SERVICE_NAME"
    echo "  Status:  systemctl status $SERVICE_NAME"
    echo "  Logs:    journalctl -u $SERVICE_NAME -f"
    echo ""
    echo "Application Logs: $APP_DIR/logs/"
    echo "Nginx Logs: /var/log/nginx/"
    echo ""
    echo "Maintenance Scripts:"
    echo "  Backup: $APP_DIR/backup.sh"
    echo "  Update: $APP_DIR/update.sh"
    echo ""
    
    if [[ "$DOMAIN" == "localhost" ]]; then
        echo "Application URL: http://localhost"
    else
        echo "Application URL: https://$DOMAIN"
    fi
    
    echo ""
    log_success "Deployment completed successfully!"
}

# Main deployment process
main() {
    log_info "Starting Font Identifier VPS deployment..."
    
    check_root
    detect_os
    install_dependencies
    create_app_user
    setup_application
    create_systemd_service
    configure_nginx
    
    if [[ "$DOMAIN" != "localhost" ]]; then
        setup_ssl
    fi
    
    configure_firewall
    setup_monitoring
    start_services
    create_maintenance_scripts
    print_summary
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --email)
            EMAIL="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --domain DOMAIN    Domain name (default: localhost)"
            echo "  --email EMAIL      Email for SSL certificate"
            echo "  --port PORT        Application port (default: 8501)"
            echo "  --help            Show this help"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main function
main
