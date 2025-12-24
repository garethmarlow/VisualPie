# VisualPie 🎵✨

Psychedelic music visualizer for Raspberry Pi 3, designed for high-quality vinyl playback via Icecast streaming.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%203-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Quick Start

```bash
# On your Raspberry Pi
git clone https://github.com/yourusername/VisualPie.git
cd VisualPie
./deploy.sh
```

That's it! The script handles everything: dependencies, config, service setup.

## Features

- 🌈 **Psychedelic spectrum analyzer** - Rainbow colors, smooth animations, glow effects
- 🎵 **Icecast stream support** - OGG/FLAC, 24-bit/48kHz audio from vinyl
- 🔧 **Modular architecture** - Ready for track recognition, lyrics, multiple viz modes
- 🚀 **Auto-start on boot** - Systemd service, set and forget
- ⚡ **Optimized for Pi 3** - 1080p HDMI @ 60fps (or 30fps for lighter load)

## Architecture

```
VisualPie/
├── visualizer.py              # Main application (orchestrator)
├── audio_engine_icecast.py    # Audio processing & FFT analysis
├── config.yaml                # Configuration
├── visualizations/            # Pluggable visualization modules
│   └── psychedelic_spectrum.py
└── future/
    ├── track_recognizer.py    # (Future) Identify tracks
    ├── lyrics_display.py      # (Future) Show synchronized lyrics
    ├── metadata_overlay.py    # (Future) Now playing info
    └── control_api.py         # (Future) REST API for Home Assistant
```

### Design Philosophy

**Modular & Extensible**: Each component is independent. Adding new visualizations or features doesn't require touching core code.

**Audio Pipeline**:
- Icecast stream → ffmpeg decode → PCM samples
- FFT analysis → frequency bands (logarithmic spacing)
- Smoothing & normalization → Visual rendering @ 60fps

**Future Extensions** (architecture ready):
- Track recognition, lyrics display, metadata overlay
- Multiple visualization modes with switching
- REST API for Home Assistant/Siri control

## Installation

### Automatic (Recommended)

```bash
cd ~
git clone https://github.com/yourusername/VisualPie.git
cd VisualPie
./deploy.sh
```

The deploy script:
1. Installs all dependencies (pygame, numpy, ffmpeg, etc.)
2. Prompts for your Icecast stream URL
3. Creates log directories
4. Offers to test the visualizer
5. Optionally installs as auto-start service

### Manual

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed step-by-step instructions.

## Configuration

Edit `config.yaml` to customize:

```yaml
audio:
  stream_url: "http://your-icecast-server:8000/stream.ogg"  # Your stream
  
visualization:
  psychedelic_spectrum:
    num_bars: 64           # 32-80 range
    color_speed: 0.5       # 0.1=slow, 2.0=fast
    smoothing: 0.85        # 0.5=reactive, 0.95=smooth
    bass_boost: 1.5        # Extra low-frequency emphasis
    glow_intensity: 0.6    # Bloom effect
    mirror_mode: true      # Center vs bottom bars
```

See [config.yaml](config.yaml) for all options.

## Usage

**Manual testing:**
```bash
./test.sh              # Windowed mode
./visualizer.py        # Fullscreen
```

**Service control:**
```bash
sudo systemctl start VisualPie
sudo systemctl stop VisualPie
sudo systemctl restart VisualPie
sudo systemctl status VisualPie
sudo journalctl -u VisualPie -f   # View logs
```

**After making changes:**
```bash
git pull                                  # Get latest
sudo systemctl restart VisualPie   # Apply
```

See [QUICKREF.md](QUICKREF.md) for more commands.

## Customization

**Visual tweaks** - Edit `config.yaml`:
- `color_speed`: Rainbow cycle speed (0.1–2.0)
- `smoothing`: Audio reactivity (0.5–0.95)
- `num_bars`: Detail level (32–80)
- `bass_boost`: Low frequency emphasis (1.0–2.5)
- `mirror_mode`: true=center, false=bottom

**Performance tuning** for Pi 3:
- Reduce `num_bars` to 48 or 32
- Lower `fps_target` to 30
- Disable `glow_intensity` (set to 0.0)

## Adding Features

The architecture is ready for extensions. See [README.md](README.md) for details on:
- Creating new visualizations
- Adding track recognition
- Building control APIs

## Troubleshooting

**No visualization:**
```bash
# Check stream
curl -I http://your-stream-url

# Test ffmpeg
ffmpeg -i http://your-stream-url -t 5 test.wav

# View logs
sudo journalctl -u VisualPie -n 100
```

**Performance issues:**
```bash
htop  # Check CPU (should be <80%)
vcgencmd measure_temp  # Check temperature
# Then reduce settings in config.yaml
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete troubleshooting guide.

## Development Workflow

```bash
# Make changes locally
vi visualizations/psychedelic_spectrum.py

# Test immediately
./test.sh

# Commit and push
git add .
git commit -m "Tweaked color cycling"
git push

# Pull on Pi and restart
ssh pi@raspberrypi.local
cd ~/VisualPie
git pull
sudo systemctl restart VisualPie
```

## Project Structure

```
VisualPie/
├── visualizer.py                    # Main application
├── audio_engine_icecast.py          # Audio processing & FFT
├── config.yaml                      # Configuration
├── deploy.sh                        # One-command deployment
├── visualizations/
│   ├── __init__.py
│   └── psychedelic_spectrum.py      # Spectrum visualizer
├── README.md                        # This file
├── QUICKREF.md                      # Command reference
└── DEPLOYMENT.md                    # Detailed Pi setup guide
```

## Contributing

This is a personal project but suggestions welcome! Open an issue or PR.

## License

MIT License - See [LICENSE](LICENSE)

## Credits

Built for vinyl lovers and psychedelic visualization enthusiasts.

Designed to complement Philips Ambilight TVs but works on any HDMI display.
