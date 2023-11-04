import wave
import sounddevice as sd
from pvcobra import CobraVAD
import numpy as np
import queue
import os
import tempfile


class AudioRecorder:
    def __init__(self, cobra_access_key, sample_rate=16000):
        self.vad = CobraVAD(access_key=cobra_access_key)
        self.sample_rate = sample_rate
        self.channels = 1
        self.audio_queue = queue.Queue()
        self.wavefile = None
        self.is_speaking = False
        self.temp_directory = tempfile.gettempdir()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)

        # Serialize indata to bytes for CobraVAD
        voice_activity = self.vad.process(
            np.frombuffer(indata, dtype=np.int16).tobytes()
        )

        if voice_activity:
            if not self.is_speaking:
                self.is_speaking = True
                self.start_of_speech()
            if self.wavefile:
                self.wavefile.writeframes(indata.tobytes())
        else:
            if self.is_speaking:
                self.is_speaking = False
                self.end_of_speech()

    def start_of_speech(self):
        self.wavefile = wave.open(os.path.join(self.temp_directory, "speech.wav"), "wb")
        self.wavefile.setnchannels(self.channels)
        self.wavefile.setsampwidth(2)  # Assuming 16-bit audio
        self.wavefile.setframerate(self.sample_rate)

    def end_of_speech(self):
        filename = self.wavefile.getfilename() if self.wavefile else None
        if self.wavefile:
            self.wavefile.close()
        return filename

    def start_recording(self):
        with sd.InputStream(
            callback=self.audio_callback,
            channels=self.channels,
            samplerate=self.sample_rate,
        ):
            print("Recorder started...")
            while True:
                # Replace with a more robust condition to keep the recorder alive
                sd.sleep(1000)
