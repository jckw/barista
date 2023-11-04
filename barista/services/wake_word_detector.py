import pvporcupine
from pvporcupine.util import pv_keyword_paths


class PorcupineWakeWordDetector:
    def __init__(self, picovoice_access_key, detected_callback):
        self.detected_callback = detected_callback
        self.porcupine = pvporcupine.create(
            access_key=picovoice_access_key,
            keyword_paths=[pv_keyword_paths("hey charlie")],
        )

    def listen_for_wake_word(self):
        import sounddevice as sd

        def callback(indata, frames, time, status):
            if self.porcupine.process(indata):
                self.detected_callback()

        with sd.InputStream(
            callback=callback, channels=1, samplerate=self.porcupine.sample_rate
        ):
            print("Listening for 'Hey Charlie'...")
            sd.sleep(-1)  # Sleep indefinitely
