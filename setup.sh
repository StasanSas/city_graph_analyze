#!/usr/bin/env bash

set -e

REQ_FILE="requirements.txt"
VENV_DIR="venv"

echo "=== Checking requirements.txt ==="
if [ ! -f "$REQ_FILE" ]; then
    echo "File $REQ_FILE not found!"
    exit 1
fi


echo "=== Installing system dependencies ==="

sudo apt-get update
sudo apt-get install -y \
    python3 python3-pip python3-venv python3-dev \
    build-essential curl wget git

echo "=== Creating virtual environment ==="
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip setuptools wheel

echo "=== Installing Python dependencies from $REQ_FILE ==="
pip install -r "$REQ_FILE"

echo "=== Installing .NET SDK ==="

UBUNTU_VER=$(lsb_release -rs)
wget "https://packages.microsoft.com/config/ubuntu/${UBUNTU_VER}/packages-microsoft-prod.deb" -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y dotnet-sdk-8.0

echo "=== Done! ==="
echo "To activate environment:"
echo "source $VENV_DIR/bin/activate"