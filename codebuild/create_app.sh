#!/usr/bin/env bash
set -euo pipefail

# ================================
# REQUIRED ENV
# ================================
APP_NAME="${APP_NAME:?APP_NAME not set}"
APP_SECRET_PATH="${APP_SECRET_PATH:?APP_SECRET_PATH not set}"
GITHUB_REPOSITORY="${GITHUB_REPOSITORY:?GITHUB_REPOSITORY not set}"

# ================================
# CONSTANTS
# ================================
BASE_DIR="/opt/apps"
APP_DIR="$BASE_DIR/$APP_NAME"
MANIFEST="$APP_DIR/codebuild/app.manifest.json"
DEPLOY_USER="ubuntu"

echo "➡ Creating app: $APP_NAME"

cd "$APP_DIR"

# ================================
# READ MANIFEST
# ================================
if [ ! -f "$MANIFEST" ]; then
  echo "❌ Missing codebuild/app.manifest.json"
  exit 1
fi

RUNTIME=$(jq -r '.runtime' "$MANIFEST")
WORKDIR=$(jq -r '.working_dir' "$MANIFEST")
START_CMD=$(jq -r '.start_command' "$MANIFEST")
PORT=$(jq -r '.port' "$MANIFEST")
DOMAIN=$(jq -r '.domain' "$MANIFEST")

APP_WORKDIR="$APP_DIR/$WORKDIR"

if [ ! -d "$APP_WORKDIR" ]; then
  echo "❌ working_dir does not exist: $APP_WORKDIR"
  exit 1
fi

cd "$APP_WORKDIR"

# Ensure app dir is writable so new subdirs can be created at runtime
chown -R "$DEPLOY_USER:$DEPLOY_USER" "$APP_WORKDIR"
chmod -R u+rwX,g+rwX "$APP_WORKDIR"

# ================================
# RUNTIME SETUP
# ================================
if [ "$RUNTIME" = "python" ]; then
  echo "🐍 Python setup"

  if [ ! -d ".venv" ]; then
    sudo -u "$DEPLOY_USER" python3 -m venv .venv
  fi

  sudo -u "$DEPLOY_USER" .venv/bin/pip install --upgrade pip
  sudo -u "$DEPLOY_USER" .venv/bin/pip install -r requirements.txt

  if [ -f manage.py ]; then
    echo "🗄️ Running Django migrations"
    sudo -u "$DEPLOY_USER" .venv/bin/python manage.py migrate --noinput
    if [ -f "db.sqlite3" ]; then
      chown "$DEPLOY_USER:$DEPLOY_USER" "db.sqlite3"
      chmod 664 "db.sqlite3"
    fi
  fi
fi

# ================================
# SYSTEMD (GENERATED)
# ================================
cat > "/etc/systemd/system/${APP_NAME}.service" <<EOF
[Unit]
Description=${APP_NAME}
After=network.target

[Service]
User=ubuntu
WorkingDirectory=${APP_WORKDIR}
UMask=0002

Environment=APP_SECRET_JSON=${APP_SECRET_PATH}
Environment=DJANGO_SETTINGS_MODULE=trigger_engine.settings
Environment=PYTHONPATH=${APP_WORKDIR}

ExecStart=${APP_WORKDIR}/${START_CMD}
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "${APP_NAME}"
systemctl restart "${APP_NAME}"

# ================================
# NGINX (GENERATED)
# ================================
echo "🌐 Generating nginx config"

cat > "/etc/nginx/sites-available/${DOMAIN}" <<EOF
server {
  listen 80;
  server_name ${DOMAIN};

  location / {
    proxy_pass http://127.0.0.1:${PORT};
    proxy_http_version 1.1;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
  }
}

server {
  listen 443 ssl;
  server_name ${DOMAIN};

  ssl_certificate /etc/nginx/ssl/self.crt;
  ssl_certificate_key /etc/nginx/ssl/self.key;

  ssl_protocols TLSv1.2 TLSv1.3;
  ssl_ciphers HIGH:!aNULL:!MD5;

  location / {
    proxy_pass http://127.0.0.1:${PORT};
    proxy_http_version 1.1;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
  }
}
EOF

ln -sf "/etc/nginx/sites-available/${DOMAIN}" "/etc/nginx/sites-enabled/${DOMAIN}"
nginx -t
systemctl reload nginx

echo "✅ App created successfully"
