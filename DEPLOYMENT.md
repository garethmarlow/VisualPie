# Raspberry Pi Deployment Guide

Complete step-by-step guide for deploying Vinyl Visualizer on a fresh Raspberry Pi 3.

## Prerequisites

- Raspberry Pi 3 (Model B or B+)
- MicroSD card (16GB+ recommended)
- Raspberry Pi OS installed (Lite or Desktop)
- HDMI connection to TV
- Network connection (WiFi or Ethernet)
- Your Icecast stream URL

## Initial Pi Setup

### 1. Flash Raspberry Pi OS

Using Raspberry Pi Imager:
1. Download from raspberrypi.org/software
2. Choose "Raspberry Pi OS Lite (64-bit)" or Desktop version
3. Flash to microSD card
4. Enable SSH before booting (create empty `ssh` file on boot partition)

### 2. First Boot

```bash
# SSH into your Pi
ssh pi@raspberrypi.local
# Default password: raspberry

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Change password
passwd

# Set timezone
sudo timedatectl set-timezone Europe/London  # Adjust for your location

# Set hostname (optional)
sudo hostnamectl set-hostname vinyl-viz
```

### 3. Configure Boot Options

```bash
sudo raspi-config
```

Navigate to:
- **1 System Options → S5 Boot/Auto Login → B2 Console Autologin** (if using Lite)
- **1 System Options → S5 Boot/Auto Login → B4 Desktop Autologin** (if using Desktop)
- **6 Advanced Options → A3 Memory Split → 128** (allocate GPU memory)
- **2 Display Options → D1 Resolution → 1920x1080** (if not auto-detected)

Finish and reboot.

## Install Vinyl Visualizer

### 1. Transfer Files

**Option A: Git clone (if you have a repo)**
```bash
cd ~
git clone https://github.com/yourusername/VisualPie.git
```

**Option B: SCP from your computer**
```bash
# On your computer
scp VisualPie.tar.gz pi@raspberrypi.local:~
# Then on Pi:
tar xzf VisualPie.tar.gz
```

**Option C: Manual download**
```bash
cd ~
wget https://your-server.com/VisualPie.tar.gz
tar xzf VisualPie.tar.gz
```

### 2. Run Installation

```bash
cd ~/VisualPie
./install.sh
```

This will:
- Install system dependencies (pygame, numpy, ffmpeg, etc.)
- Install Python packages
- Create log directories
- Take ~5-10 minutes

### 3. Configure Your Stream

```bash
vi config.yaml
```

Change this line:
```yaml
audio:
  stream_url: "http://YOUR-ICECAST-SERVER:8000/stream.ogg"
```

Save and exit (`:wq` in vi).

### 4. Test Run

```bash
# Windowed test (if using Desktop OS)
./test.sh

# Or fullscreen test
./visualizer.py
```

You should see colorful psychedelic bars reacting to your audio!

Press ESC or Q to quit.

### 5. Install as Service

```bash
sudo ./install-service.sh
```

This enables auto-start on boot.

### 6. Start Service

```bash
sudo systemctl start VisualPie
sudo systemctl status VisualPie
```

## Display Configuration

### Auto-Start Display (for Headless/Lite OS)

If using Raspberry Pi OS Lite (no desktop), you need X server:

```bash
# Install minimal X server
sudo apt-get install -y xserver-xorg xinit x11-xserver-utils

# Edit ~/.bash_profile
vi ~/.bash_profile
```

Add:
```bash
if [ -z "$DISPLAY" ] && [ $(tty) = /dev/tty1 ]; then
    startx &
fi
```

Create `~/.xinitrc`:
```bash
vi ~/.xinitrc
```

Add:
```bash
#!/bin/bash
xset -dpms      # Disable screen blanking
xset s off      # Disable screensaver
xset s noblank  # Disable screen blanking
exec python3 ~/VisualPie/visualizer.py
```

Make executable:
```bash
chmod +x ~/.xinitrc
```

### Disable Screen Blanking (Desktop OS)

```bash
# Edit lightdm config
sudo vi /etc/lightdm/lightdm.conf
```

Under `[Seat:*]` add:
```
xserver-command=X -s 0 -dpms
```

## Network Configuration

### Static IP (Recommended)

```bash
sudo vi /etc/dhcpcd.conf
```

Add at the end:
```
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8

# Or for WiFi:
interface wlan0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8
```

Adjust IPs for your network.

## Performance Optimization

### 1. GPU Memory

Already set to 128MB in raspi-config above.

### 2. Disable Unnecessary Services

```bash
# List running services
sudo systemctl list-unit-files --type=service --state=enabled

# Disable unneeded ones (examples)
sudo systemctl disable bluetooth.service
sudo systemctl disable avahi-daemon.service
sudo systemctl disable triggerhappy.service
```

### 3. CPU Governor

```bash
# Set to performance mode
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

Make permanent:
```bash
sudo vi /etc/rc.local
```

Add before `exit 0`:
```bash
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

### 4. Overclocking (Optional, Advanced)

```bash
sudo vi /boot/config.txt
```

Add:
```
# Overclock (tested stable on Pi 3B+)
over_voltage=2
arm_freq=1350
gpu_freq=500
sdram_freq=500
```

**Warning:** Overclocking can cause instability. Test thoroughly!

## Monitoring & Maintenance

### Check Service Status

```bash
sudo systemctl status VisualPie
```

### View Logs

```bash
# Live tail
sudo journalctl -u VisualPie -f

# Last 100 lines
sudo journalctl -u VisualPie -n 100
```

### Monitor Performance

```bash
# CPU/Memory usage
htop

# Temperature
vcgencmd measure_temp

# GPU memory
vcgencmd get_mem gpu
```

### Update Visualizer

```bash
cd ~/VisualPie
git pull  # If using git

# Or transfer new files via SCP

sudo systemctl restart VisualPie
```

## Troubleshooting

### Visualizer Won't Start

```bash
# Check logs
sudo journalctl -u VisualPie -n 50

# Test manually
sudo systemctl stop VisualPie
cd ~/VisualPie
./visualizer.py
```

### No Audio/Black Screen

```bash
# Test stream
ffmpeg -i http://your-stream-url -t 5 test.wav

# Check if ffmpeg is working
ffmpeg -version

# Verify network connectivity
ping your-icecast-server
```

### Display Issues

```bash
# Check HDMI detection
tvservice -s

# Force HDMI mode
sudo vi /boot/config.txt
# Add: hdmi_force_hotplug=1
# Add: hdmi_drive=2

sudo reboot
```

### Performance Issues

1. Check temperature: `vcgencmd measure_temp`
   - If >80°C, add heatsink or fan
2. Reduce settings in `config.yaml`:
   - `num_bars: 32`
   - `fps_target: 30`
   - `glow_intensity: 0.0`
3. Check other processes: `htop`

## Remote Access

### SSH

Already enabled during setup.

### VNC (Optional)

```bash
sudo raspi-config
# Interface Options → VNC → Enable

# Then connect with VNC client to Pi's IP
```

## Backup Configuration

```bash
# Backup config
cp ~/VisualPie/config.yaml ~/VisualPie/config.yaml.backup

# Copy to your computer
scp pi@raspberrypi.local:~/VisualPie/config.yaml ~/Desktop/
```

## Complete Deployment Checklist

- [ ] Flash Raspberry Pi OS
- [ ] First boot and update system
- [ ] Configure boot options (raspi-config)
- [ ] Transfer VisualPie files
- [ ] Run `./install.sh`
- [ ] Edit `config.yaml` with stream URL
- [ ] Test run `./test.sh` or `./visualizer.py`
- [ ] Install service `sudo ./install-service.sh`
- [ ] Configure display auto-start (if Lite OS)
- [ ] Disable screen blanking
- [ ] Set static IP (optional)
- [ ] Optimize performance (GPU memory, governor)
- [ ] Test service `sudo systemctl start VisualPie`
- [ ] Verify auto-start on reboot
- [ ] Done! 🎉

## Post-Deployment

Your visualizer should now:
- ✓ Auto-start on boot
- ✓ Display psychedelic spectrum on your TV
- ✓ React to your vinyl playback via Icecast
- ✓ Run reliably 24/7

Next steps:
- Tweak colors/speed in `config.yaml`
- Plan additional features (track recognition, lyrics)
- Consider adding more visualization modes
- Integrate with Home Assistant for control

Enjoy your vinyl visualizer! 🎵✨
