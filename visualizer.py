#!/usr/bin/env python3
"""
Vinyl Visualizer - Main Application

Modular music visualizer for Raspberry Pi 3
Designed for extensibility: track recognition, lyrics, multiple viz modes
"""

import pygame
import yaml
import logging
import sys
import signal
from pathlib import Path

# Local imports
from audio_engine_icecast import AudioEngine, AudioEngineFallback
from visualizations.psychedelic_spectrum import PsychedelicSpectrum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/vinyl-visualizer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class VinylVisualizer:
    """Main visualizer application"""
    
    def __init__(self, config_path='config.yaml'):
        logger.info("Initializing Vinyl Visualizer")
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize pygame
        pygame.init()
        
        # Setup display
        display_config = self.config['display']
        if display_config['fullscreen']:
            self.screen = pygame.display.set_mode(
                (display_config['width'], display_config['height']),
                pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            )
            pygame.mouse.set_visible(False)
        else:
            self.screen = pygame.display.set_mode(
                (display_config['width'], display_config['height'])
            )
        
        pygame.display.set_caption("Vinyl Visualizer")
        
        # Initialize audio engine
        # Try Icecast stream, fall back to system audio if unavailable
        try:
            self.audio_engine = AudioEngine(self.config)
            logger.info("Using Icecast stream audio engine")
        except Exception as e:
            logger.warning(f"Icecast engine failed: {e}, using fallback")
            self.audio_engine = AudioEngineFallback(self.config)
            logger.info("Using fallback audio engine (system input)")
        
        # Initialize visualization
        viz_name = self.config['visualization']['current']
        self.visualization = self._load_visualization(viz_name)
        
        # FPS control
        self.clock = pygame.time.Clock()
        self.fps_target = display_config['fps_target']
        self.running = False
        
        # Stats
        self.frame_count = 0
        self.fps_display_counter = 0
        
        logger.info("Vinyl Visualizer initialized successfully")
        
    def _load_visualization(self, viz_name):
        """Load visualization module by name"""
        if viz_name == 'psychedelic_spectrum':
            return PsychedelicSpectrum(self.config, self.screen)
        else:
            raise ValueError(f"Unknown visualization: {viz_name}")
            
    def run(self):
        """Main application loop"""
        logger.info("Starting Vinyl Visualizer")
        self.running = True
        
        # Start audio processing
        self.audio_engine.start()
        
        try:
            while self.running:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                            self.running = False
                        # Future: Switch visualizations, toggle features, etc.
                
                # Get latest audio data
                fft_data = self.audio_engine.get_fft_data()
                
                # Update visualization
                self.visualization.update(fft_data)
                
                # Render
                self.visualization.draw()
                
                # Update display
                pygame.display.flip()
                
                # FPS control
                self.clock.tick(self.fps_target)
                
                # Log FPS periodically
                self.frame_count += 1
                self.fps_display_counter += 1
                if self.fps_display_counter >= 300:  # Every 5 seconds at 60fps
                    actual_fps = self.clock.get_fps()
                    logger.info(f"FPS: {actual_fps:.1f}")
                    self.fps_display_counter = 0
                    
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        except Exception as e:
            logger.error(f"Error in main loop: {e}", exc_info=True)
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean shutdown"""
        logger.info("Shutting down...")
        self.running = False
        self.audio_engine.stop()
        pygame.quit()
        logger.info("Shutdown complete")


def main():
    """Entry point"""
    # Handle signals for clean shutdown
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Get config path from command line or use default
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    else:
        config_path = Path(__file__).parent / 'config.yaml'
    
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        sys.exit(1)
    
    # Run visualizer
    visualizer = VinylVisualizer(config_path)
    visualizer.run()


if __name__ == '__main__':
    main()
