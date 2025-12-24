# VisualPie - Quick Reference

## Installation (One-Time Setup)

```bash
cd ~/VisualPie
./install.sh
sudo ./install-service.sh
```

## Configuration

Edit your Icecast stream URL:
```bash
vi config.yaml
# Change: stream_url: "http://your-server:8000/stream.ogg"
```

## Running

**Manual test:**
```bash
./visualizer.py                    # Fullscreen
./test.sh                          # Windowed test mode
```

**As service:**
```bash
sudo systemctl start VisualPie     # Start
sudo systemctl stop VisualPie      # Stop
sudo systemctl restart VisualPie   # Restart
sudo systemctl status VisualPie    # Check status
```

## Logs

```bash
# Service logs (live tail)
sudo journalctl -u VisualPie -f

# Last 50 lines
sudo journalctl -u VisualPie -n 50

# Application logs
tail -f /tmp/VisualPie.log
```

## Keyboard Controls (When Running Manually)

- **ESC** or **Q**: Quit
- More controls coming soon (viz switching, etc.)

## Performance Tuning

Edit `config.yaml`:

**For better performance:**
```yaml
display:
  fps_target: 30              # Lower FPS
visualization:
  psychedelic_spectrum:
    num_bars: 48              # Fewer bars
    glow_intensity: 0.0       # Disable glow
```

**For better visuals:**
```yaml
display:
  fps_target: 60
visualization:
  psychedelic_spectrum:
    num_bars: 80              # More bars
    glow_intensity: 0.8       # More glow
    color_speed: 1.0          # Faster colors
```

## Customization

**Color speed:** (How fast rainbow cycles)
- `0.1` = Very slow, meditative
- `0.5` = Moderate (default)
- `2.0` = Fast, energetic

**Smoothing:** (How reactive to audio)
- `0.5` = Very reactive, jittery
- `0.85` = Smooth (default)
- `0.95` = Very smooth, floaty

**Bass boost:** (Low frequency emphasis)
- `1.0` = Flat response
- `1.5` = Moderate boost (default)
- `2.5` = Heavy bass emphasis

**Mirror mode:**
- `true`: Bars grow from center (symmetric)
- `false`: Bars grow from bottom (classic)

## Troubleshooting

**Black screen:**
```bash
# Check if stream is accessible
curl -I http://your-stream-url

# Test ffmpeg decode
ffmpeg -i http://your-stream-url -t 5 test.wav

# Check logs
sudo journalctl -u VisualPie -n 100
```

**Poor performance:**
```bash
# Check CPU usage
htop

# If >80% on one core:
# - Reduce num_bars to 32
# - Lower fps_target to 30
# - Set glow_intensity to 0.0
```

**Service won't start:**
```bash
# Check service file paths
cat /etc/systemd/system/VisualPie.service

# Reload systemd
sudo systemctl daemon-reload

# Check for errors
sudo systemctl status VisualPie
```

## File Locations

- **Config:** `~/VisualPie/config.yaml`
- **Service:** `/etc/systemd/system/VisualPie.service`
- **Logs:** `/var/log/VisualPie/` and `/tmp/VisualPie.log`
- **Code:** `~/VisualPie/`

## Quick Tweaks Without Restart

```bash
# Edit config
vi ~/VisualPie/config.yaml

# Restart service to apply
sudo systemctl restart VisualPie

# Watch it start up
sudo journalctl -u VisualPie -f
```

## Future Features (Architecture Ready)

- Multiple visualization modes (switch via Siri/Home Assistant)
- Track recognition (display album art, artist, title)
- Lyrics display (synchronized to music)
- REST API for control
- Customizable color schemes
- Beat detection visualizations

## Development

```bash
# Run in test mode (windowed)
./test.sh

# Edit visualization
vi visualizations/psychedelic_spectrum.py

# Create new visualization
cp visualizations/psychedelic_spectrum.py visualizations/my_viz.py
# Edit my_viz.py, update config.yaml
```

## Getting Help

1. Check logs: `sudo journalctl -u VisualPie -n 100`
2. Test stream: `ffmpeg -i http://your-stream-url -t 5 test.wav`
3. Check CPU: `htop`
4. Test manually: `./test.sh`

## Emergency Stop

```bash
# Stop the service
sudo systemctl stop VisualPie

# Disable auto-start
sudo systemctl disable VisualPie

# Kill any running instances
pkill -f visualizer.py
```
