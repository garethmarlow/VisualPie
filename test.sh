#!/bin/bash
# Quick test script for development

echo "=== VisualPie Test ==="
echo ""

# Check dependencies
echo "Checking dependencies..."

command -v python3 >/dev/null 2>&1 || { echo "Python3 not found!"; exit 1; }
command -v ffmpeg >/dev/null 2>&1 || { echo "WARNING: ffmpeg not found (needed for Icecast)"; }

# Check Python packages
python3 -c "import pygame" 2>/dev/null || { echo "WARNING: pygame not installed"; }
python3 -c "import numpy" 2>/dev/null || { echo "WARNING: numpy not installed"; }
python3 -c "import yaml" 2>/dev/null || { echo "WARNING: PyYAML not installed"; }

echo ""
echo "Testing visualizer in windowed mode..."
echo "Press ESC or Q to quit"
echo ""

# Create test config if it doesn't exist
if [ ! -f config.yaml.bak ]; then
    cp config.yaml config.yaml.bak
fi

# Modify config for testing (windowed mode)
cat > config.test.yaml << EOF
# Test configuration (windowed mode)
audio:
  stream_url: "http://localhost:8000/stream.ogg"
  sample_rate: 48000
  channels: 2
  buffer_size: 2048

display:
  width: 1280
  height: 720
  fullscreen: false  # Windowed for testing
  fps_target: 60

visualization:
  current: "psychedelic_spectrum"
  
  psychedelic_spectrum:
    num_bars: 64
    bar_spacing: 4
    color_speed: 0.5
    smoothing: 0.85
    amplitude_scale: 2.0
    bass_boost: 1.5
    glow_intensity: 0.6
    mirror_mode: true
    
features:
  track_recognition: false
  lyrics_display: false
  metadata_display: false
EOF

# Run with test config
export SDL_VIDEODRIVER=x11
python3 visualizer.py config.test.yaml 2>&1 | tee /tmp/visualizer-test.log

echo ""
echo "Test complete. Log saved to /tmp/visualizer-test.log"
