import pvporcupine
from pvporcupine import pv_keyword_paths
from pvrecorder import PvRecorder
import wave
import struct
import tempfile
from datetime import datetime


class WakeWordDetector:
    def __init__(self, picovoice_access_key, detected_callback):
        self.access_key = picovoice_access_key
        self.detected_callback = detected_callback

    def listen_for_wake_word(self):
        output_path = tempfile.gettempdir() + "/audio-recorder-output.wav"

        porcupine = pvporcupine.create(
            access_key=self.access_key,
            keyword_paths=[pv_keyword_paths("")["hey barista"]],
        )

        recorder = PvRecorder(frame_length=porcupine.frame_length)
        recorder.start()

        wav_file = wave.open(output_path, "w")
        wav_file.setparams((1, 2, 16000, 512, "NONE", "NONE"))

        print("Listening ... (press Ctrl+C to exit)")

        try:
            while True:
                pcm = recorder.read()
                result = porcupine.process(pcm)

                if wav_file is not None:
                    wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

                if result >= 0:
                    print("[%s] Detected %s" % (str(datetime.now()), "hey barista"))
                    self.detected_callback()
                    break
        except KeyboardInterrupt:
            print("Stopping ...")
        finally:
            recorder.delete()
            porcupine.delete()
            if wav_file is not None:
                wav_file.close()
