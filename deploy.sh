#!/bin/bash
# Complete deployment script for Raspberry Pi
# Handles: dependencies, config, service setup, everything

set -e

echo "╔════════════════════════════════════════╗"
echo "║   Vinyl Visualizer - Pi Deployment    ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check if running on Pi
if [ -f /proc/device-tree/model ]; then
    echo "✓ Detected: $(cat /proc/device-tree/model)"
else
    echo "⚠ Warning: Not detected as Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
fi

# Check we're in the right directory
if [ ! -f "visualizer.py" ]; then
    echo "✗ Error: Not in vinyl-visualizer directory"
    echo "  Run this from the project root"
    exit 1
fi

echo ""
echo "=== Step 1: System Dependencies ==="
echo ""

# Update package lists
echo "Updating package lists..."
sudo apt-get update -qq

# Install system packages
echo "Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-pygame \
    python3-numpy \
    python3-yaml \
    libsdl2-dev \
    libsdl2-mixer-dev \
    libsdl2-image-dev \
    libsdl2-ttf-dev \
    portaudio19-dev \
    python3-dev \
    ffmpeg \
    git 2>&1 | grep -v "is already the newest version" || true

echo "✓ System dependencies installed"

echo ""
echo "=== Step 2: Python Dependencies ==="
echo ""

# Install Python packages
echo "Installing Python packages..."
pip3 install --break-system-packages -q -r requirements.txt
echo "✓ Python packages installed"

echo ""
echo "=== Step 3: Configuration ==="
echo ""

# Check if config needs updating
if grep -q "http://your-icecast-server" config.yaml 2>/dev/null; then
    echo "⚠ Config needs your Icecast stream URL"
    echo ""
    read -p "Enter your Icecast stream URL (or press Enter to skip): " STREAM_URL
    if [ ! -z "$STREAM_URL" ]; then
        # Escape special chars for sed
        ESCAPED_URL=$(echo "$STREAM_URL" | sed 's/[\/&]/\\&/g')
        sed -i "s|http://your-icecast-server:8000/stream.ogg|$ESCAPED_URL|g" config.yaml
        echo "✓ Stream URL configured"
    else
        echo "  You can set it later by editing config.yaml"
    fi
else
    echo "✓ Config already customized"
fi

echo ""
echo "=== Step 4: Log Directories ==="
echo ""

# Create log directory
sudo mkdir -p /var/log/vinyl-visualizer
sudo chown $USER:$USER /var/log/vinyl-visualizer
echo "✓ Log directories created"

echo ""
echo "=== Step 5: Test Run ==="
echo ""

echo "Would you like to test the visualizer now?"
read -p "Test in windowed mode? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Starting test (press ESC or Q to quit)..."
    sleep 2
    ./test.sh || echo "Test completed"
fi

echo ""
echo "=== Step 6: Service Installation ==="
echo ""

read -p "Install as auto-start service? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing systemd service..."
    
    # Update service file with actual username and paths
    USERNAME=$(whoami)
    INSTALL_DIR=$(pwd)
    
    sed "s/User=pi/User=$USERNAME/" vinyl-visualizer.service | \
    sed "s/Group=pi/Group=$USERNAME/" | \
    sed "s|/home/pi/vinyl-visualizer|$INSTALL_DIR|g" | \
    sudo tee /etc/systemd/system/vinyl-visualizer.service > /dev/null
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    # Enable service
    sudo systemctl enable vinyl-visualizer.service
    
    echo "✓ Service installed and enabled"
    echo ""
    
    read -p "Start service now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo systemctl start vinyl-visualizer
        sleep 2
        sudo systemctl status vinyl-visualizer --no-pager || true
    fi
fi

echo ""
echo "╔════════════════════════════════════════╗"
echo "║          Deployment Complete!          ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "Quick commands:"
echo "  Test:      ./test.sh"
echo "  Start:     sudo systemctl start vinyl-visualizer"
echo "  Stop:      sudo systemctl stop vinyl-visualizer"
echo "  Restart:   sudo systemctl restart vinyl-visualizer"
echo "  Status:    sudo systemctl status vinyl-visualizer"
echo "  Logs:      sudo journalctl -u vinyl-visualizer -f"
echo ""
echo "Config:      vi config.yaml"
echo "Quick ref:   cat QUICKREF.md"
echo ""
echo "Enjoy your psychedelic vinyl visualizer! 🎵✨"
echo ""
