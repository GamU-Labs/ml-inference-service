#!/usr/bin/env bash
set -euo pipefail

echo "=== Docker Setup Script ==="
echo ""

echo "[1/6] Installing prerequisites..."
sudo apt update
sudo apt install -y ca-certificates curl

echo "[2/6] Adding Docker's official GPG key..."
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "[3/6] Adding Docker apt repository..."
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

echo "[4/6] Installing Docker..."
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "[5/6] Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

echo "[6/6] Adding current user to docker group..."
sudo groupadd docker 2>/dev/null || true
sudo usermod -aG docker "$USER"

echo ""
echo "=== Docker installed successfully! ==="
echo ""
echo "IMPORTANT: Run the following command to activate group changes:"
echo "  newgrp docker"
echo ""
echo "Or log out and log back in for changes to take effect."
echo ""
echo "Verify installation:"
echo "  docker --version"
echo "  docker compose version"