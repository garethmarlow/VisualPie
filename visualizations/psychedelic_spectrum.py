#!/usr/bin/env python3
"""
Psychedelic Spectrum Visualization
Colorful, dynamic frequency spectrum with smooth animations
"""

import pygame
import numpy as np
import colorsys
import logging

logger = logging.getLogger(__name__)


class PsychedelicSpectrum:
    """Psychedelic frequency spectrum visualizer"""
    
    def __init__(self, config, screen):
        self.config = config['visualization']['psychedelic_spectrum']
        self.display_config = config['display']
        self.screen = screen
        self.width = self.display_config['width']
        self.height = self.display_config['height']
        
        # Visualization parameters
        self.num_bars = self.config['num_bars']
        self.bar_spacing = self.config['bar_spacing']
        self.color_speed = self.config['color_speed']
        self.smoothing = self.config['smoothing']
        self.amplitude_scale = self.config['amplitude_scale']
        self.bass_boost = self.config['bass_boost']
        self.glow_intensity = self.config['glow_intensity']
        self.mirror_mode = self.config['mirror_mode']
        
        # State
        self.bar_heights = np.zeros(self.num_bars)
        self.color_offset = 0.0
        self.frame_count = 0
        
        # Calculate bar dimensions
        total_spacing = (self.num_bars - 1) * self.bar_spacing
        self.bar_width = (self.width - total_spacing) // self.num_bars
        
        # Frequency bands (logarithmic spacing for better bass/treble)
        self.freq_bands = self._calculate_freq_bands()
        
        # Glow surface (for bloom effect)
        self.glow_surface = pygame.Surface((self.width, self.height))
        self.glow_surface.set_alpha(int(255 * self.glow_intensity))
        
        logger.info(f"Psychedelic spectrum initialized: {self.num_bars} bars, {self.bar_width}px wide")
        
    def _calculate_freq_bands(self):
        """Calculate logarithmic frequency bands (better for music)"""
        # Human hearing is logarithmic, so space bands logarithmically
        # Focus on 20Hz to 20kHz range
        min_freq = 20
        max_freq = 20000
        
        # Create log-spaced frequency boundaries
        bands = np.logspace(np.log10(min_freq), np.log10(max_freq), self.num_bars + 1)
        return [(bands[i], bands[i+1]) for i in range(self.num_bars)]
        
    def _map_fft_to_bands(self, magnitude, freqs):
        """Map FFT data to frequency bands"""
        band_values = np.zeros(self.num_bars)
        
        for i, (low, high) in enumerate(self.freq_bands):
            # Find FFT bins in this frequency range
            mask = (freqs >= low) & (freqs < high)
            if np.any(mask):
                # Average magnitude in this band
                band_values[i] = np.mean(magnitude[mask])
                
                # Bass boost for low frequencies
                if i < self.num_bars // 4:
                    band_values[i] *= self.bass_boost
        
        return band_values
        
    def _get_rainbow_color(self, position, brightness=1.0):
        """Generate rainbow color at given position (0.0 to 1.0)"""
        hue = (position + self.color_offset) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 0.8, brightness)
        return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        
    def update(self, fft_data):
        """Update visualization with new FFT data"""
        if fft_data is None:
            return
            
        magnitude = fft_data['magnitude']
        freqs = fft_data['freqs']
        
        # Map to frequency bands
        band_values = self._map_fft_to_bands(magnitude, freqs)
        
        # Normalize and scale
        if np.max(band_values) > 0:
            band_values = band_values / np.max(band_values)
            
        band_values *= self.amplitude_scale
        
        # Smooth transitions
        self.bar_heights = (self.smoothing * self.bar_heights + 
                           (1 - self.smoothing) * band_values)
        
        # Update color cycle
        self.color_offset += self.color_speed * 0.001
        self.frame_count += 1
        
    def draw(self):
        """Render the visualization"""
        # Clear screen to black
        self.screen.fill((0, 0, 0))
        self.glow_surface.fill((0, 0, 0, 0))
        
        # Draw spectrum bars
        x = 0
        for i in range(self.num_bars):
            # Calculate bar height
            bar_height = int(self.bar_heights[i] * self.height * 0.8)
            bar_height = max(2, min(bar_height, self.height))
            
            # Rainbow color based on position and time
            position = i / self.num_bars
            color = self._get_rainbow_color(position, 1.0)
            glow_color = self._get_rainbow_color(position, 0.5)
            
            if self.mirror_mode:
                # Mirror mode: bars grow from center
                center_y = self.height // 2
                bar_top = center_y - bar_height // 2
                bar_rect = pygame.Rect(x, bar_top, self.bar_width, bar_height)
            else:
                # Normal mode: bars grow from bottom
                bar_top = self.height - bar_height
                bar_rect = pygame.Rect(x, bar_top, self.bar_width, bar_height)
            
            # Draw main bar
            pygame.draw.rect(self.screen, color, bar_rect)
            
            # Draw glow (wider, dimmer bar behind)
            glow_width = self.bar_width + 8
            glow_rect = pygame.Rect(x - 4, bar_top - 4, glow_width, bar_height + 8)
            pygame.draw.rect(self.glow_surface, glow_color, glow_rect)
            
            x += self.bar_width + self.bar_spacing
        
        # Apply glow effect
        self.screen.blit(self.glow_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        
        # Subtle background animation (pulsing gradient)
        if self.frame_count % 3 == 0:  # Every 3rd frame for performance
            avg_energy = np.mean(self.bar_heights)
            if avg_energy > 0.1:
                pulse_alpha = int(avg_energy * 20)
                pulse_color = self._get_rainbow_color(self.color_offset, 0.3)
                pulse_surface = pygame.Surface((self.width, self.height))
                pulse_surface.set_alpha(pulse_alpha)
                pulse_surface.fill(pulse_color)
                self.screen.blit(pulse_surface, (0, 0))
