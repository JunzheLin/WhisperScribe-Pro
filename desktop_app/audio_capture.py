import queue
import threading
import numpy as np
import pyaudiowpatch as pyaudio
import scipy.signal
import time

class AudioCaptureThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.audio_queue = queue.Queue()
        self.running = True
        self.target_sr = 16000
        
    def run(self):
        p = pyaudio.PyAudio()

        try:
            # Get default WASAPI info
            wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
            default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
            
            if not default_speakers["isLoopbackDevice"]:
                for loopback in p.get_loopback_device_info_generator():
                    if default_speakers["name"] in loopback["name"]:
                        default_speakers = loopback
                        break
            
            sample_rate = int(default_speakers["defaultSampleRate"])
            channels = default_speakers["maxInputChannels"]
            
            def callback(in_data, frame_count, time_info, status):
                if in_data and len(in_data) > 0:
                    # PyAudioWPatch often returns int16 or float32. We assume int16 array bytes for simplicity, 
                    # but check device properties in a real robust setup. 
                    # Here we convert from 16-bit PCM to float32
                    audio_data = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0
                    
                    # Convert to mono if stereo
                    if channels > 1:
                        audio_data = audio_data.reshape(-1, channels).mean(axis=1)

                    # Resample to 16000 Hz for Whisper
                    if sample_rate != self.target_sr:
                        num_samples = int(len(audio_data) * self.target_sr / sample_rate)
                        resampled = scipy.signal.resample(audio_data, num_samples)
                    else:
                        resampled = audio_data
                        
                    self.audio_queue.put(resampled)
                return (in_data, pyaudio.paContinue)

            print(f"Starting loopback capture on: {default_speakers['name']}")
            
            stream = p.open(
                format=pyaudio.paInt16,
                channels=channels,
                rate=sample_rate,
                frames_per_buffer=pyaudio.get_sample_size(pyaudio.paInt16) * 4096,
                input=True,
                input_device_index=default_speakers["index"],
                stream_callback=callback
            )
            
            stream.start_stream()
            while stream.is_active() and self.running:
                time.sleep(0.1)
                
            stream.stop_stream()
            stream.close()

        except Exception as e:
            print("Audio capture error:", e)
        finally:
            p.terminate()

    def stop(self):
        self.running = False
