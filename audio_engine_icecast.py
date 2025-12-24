#!/usr/bin/env python3
"""
Audio Engine - Handles stream processing and FFT analysis
Supports Icecast streams (OGG/FLAC) via ffmpeg
"""

import numpy as np
import threading
import queue
import logging
import subprocess
import struct
import sys

logger = logging.getLogger(__name__)


class AudioEngine:
    """Processes audio stream and provides FFT data to visualizations"""
    
    def __init__(self, config):
        self.config = config
        self.audio_config = config['audio']
        self.running = False
        self.fft_queue = queue.Queue(maxsize=2)
        self.sample_rate = self.audio_config['sample_rate']
        self.buffer_size = self.audio_config['buffer_size']
        self.channels = self.audio_config['channels']
        
        # FFT processing
        self.window = np.hanning(self.buffer_size)
        self.freqs = np.fft.rfftfreq(self.buffer_size, 1.0/self.sample_rate)
        
        # Audio buffer
        self.audio_buffer = np.zeros(self.buffer_size)
        
        logger.info(f"Audio engine initialized: {self.sample_rate}Hz, {self.channels}ch, buffer={self.buffer_size}")
        
    def start(self):
        """Start audio processing thread"""
        self.running = True
        self.thread = threading.Thread(target=self._process_stream, daemon=True)
        self.thread.start()
        logger.info("Audio engine started")
        
    def stop(self):
        """Stop audio processing"""
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join(timeout=2.0)
        logger.info("Audio engine stopped")
        
    def _process_stream(self):
        """Process audio from Icecast stream using ffmpeg"""
        stream_url = self.audio_config['stream_url']
        logger.info(f"Connecting to stream: {stream_url}")
        
        # ffmpeg command to decode Icecast stream to raw PCM
        # Output: 16-bit signed integer, sample_rate Hz, stereo
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', stream_url,
            '-f', 's16le',  # 16-bit signed little-endian
            '-acodec', 'pcm_s16le',
            '-ar', str(self.sample_rate),
            '-ac', str(self.channels),
            '-'  # Output to stdout
        ]
        
        try:
            # Start ffmpeg process
            logger.info("Starting ffmpeg stream decoder...")
            process = subprocess.Popen(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                bufsize=self.buffer_size * self.channels * 2  # 2 bytes per sample
            )
            
            logger.info("Stream connected and decoding")
            
            # Bytes per sample (16-bit = 2 bytes)
            bytes_per_sample = 2
            chunk_size = self.buffer_size * self.channels * bytes_per_sample
            
            while self.running:
                # Read chunk from ffmpeg
                raw_data = process.stdout.read(chunk_size)
                
                if len(raw_data) < chunk_size:
                    logger.warning("Stream ended or incomplete data")
                    break
                
                # Convert bytes to numpy array
                audio_data = np.frombuffer(raw_data, dtype=np.int16)
                
                # Reshape to (samples, channels) and convert to float
                audio_data = audio_data.reshape(-1, self.channels).astype(np.float32)
                audio_data /= 32768.0  # Normalize to -1.0 to 1.0
                
                # Convert to mono by averaging channels
                mono_data = np.mean(audio_data, axis=1)
                
                # Ensure we have exactly buffer_size samples
                if len(mono_data) == self.buffer_size:
                    # Perform FFT
                    windowed = mono_data * self.window
                    fft_data = np.fft.rfft(windowed)
                    magnitude = np.abs(fft_data)
                    
                    # Put in queue (non-blocking, drop if full)
                    try:
                        self.fft_queue.put_nowait({
                            'magnitude': magnitude,
                            'freqs': self.freqs,
                            'raw_audio': mono_data
                        })
                    except queue.Full:
                        pass
                        
            # Cleanup
            process.terminate()
            process.wait(timeout=2.0)
            
        except FileNotFoundError:
            logger.error("ffmpeg not found! Please install: sudo apt-get install ffmpeg")
            self.running = False
        except Exception as e:
            logger.error(f"Stream processing error: {e}", exc_info=True)
            self.running = False
            
    def get_fft_data(self):
        """Get latest FFT data (non-blocking)"""
        try:
            return self.fft_queue.get_nowait()
        except queue.Empty:
            return None


class AudioEngineFallback:
    """Fallback audio engine using sounddevice for testing without stream"""
    
    def __init__(self, config):
        self.config = config
        self.audio_config = config['audio']
        self.running = False
        self.fft_queue = queue.Queue(maxsize=2)
        self.sample_rate = self.audio_config['sample_rate']
        self.buffer_size = self.audio_config['buffer_size']
        self.channels = self.audio_config['channels']
        
        # FFT processing
        self.window = np.hanning(self.buffer_size)
        self.freqs = np.fft.rfftfreq(self.buffer_size, 1.0/self.sample_rate)
        
        logger.info(f"Audio engine (fallback) initialized: {self.sample_rate}Hz")
        
    def start(self):
        """Start audio processing using sounddevice"""
        import sounddevice as sd
        
        self.running = True
        
        def audio_callback(indata, frames, time, status):
            if status:
                logger.warning(f"Audio status: {status}")
            
            if not self.running:
                raise sd.CallbackAbort
            
            # Convert to mono
            if len(indata.shape) > 1:
                audio_data = np.mean(indata, axis=1)
            else:
                audio_data = indata[:, 0]
            
            # Perform FFT
            windowed = audio_data * self.window[:len(audio_data)]
            fft_data = np.fft.rfft(windowed)
            magnitude = np.abs(fft_data)
            
            try:
                self.fft_queue.put_nowait({
                    'magnitude': magnitude,
                    'freqs': self.freqs,
                    'raw_audio': audio_data
                })
            except queue.Full:
                pass
        
        logger.info("Using fallback audio input (system microphone/line-in)")
        
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            blocksize=self.buffer_size,
            callback=audio_callback
        )
        self.stream.start()
        logger.info("Audio engine started (fallback mode)")
        
    def stop(self):
        """Stop audio processing"""
        self.running = False
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        logger.info("Audio engine stopped")
        
    def get_fft_data(self):
        """Get latest FFT data (non-blocking)"""
        try:
            return self.fft_queue.get_nowait()
        except queue.Empty:
            return None
