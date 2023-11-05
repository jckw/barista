import sys
import struct
import wave
import pvcobra
from pvrecorder import PvRecorder
import tempfile
import time


class AudioRecorder:
    def __init__(self, cobra_access_key):
        self.access_key = cobra_access_key

    def start_recording(self):
        output_path = tempfile.gettempdir() + "/audio-recorder-output.wav"

        cobra = pvcobra.create(access_key=self.access_key)

        recorder = None
        wav_file = None

        try:
            recorder = PvRecorder(frame_length=512)
            recorder.start()

            wav_file = wave.open(output_path, "w")
            wav_file.setparams((1, 2, 16000, 512, "NONE", "NONE"))

            print("Listening...")
            silence_start_time = None
            speaking_started = False
            while True:
                pcm = recorder.read()

                wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

                voice_probability = cobra.process(pcm)
                percentage = voice_probability * 100
                bar_length = int((percentage / 10) * 3)
                empty_length = 30 - bar_length
                sys.stdout.write(
                    "\r[%3d]|%s%s|" % (percentage, "█" * bar_length, " " * empty_length)
                )
                sys.stdout.flush()

                if voice_probability < 0.5:
                    if silence_start_time is None:
                        silence_start_time = time.time()
                    elif speaking_started and time.time() - silence_start_time > 2:
                        print(
                            "Stopping due to 2 seconds of silence after speaking started."
                        )
                        break
                    elif time.time() - silence_start_time > 5:
                        print("Stopping due to 5 seconds of total silence.")
                        break
                else:
                    speaking_started = True
                    silence_start_time = None

        except KeyboardInterrupt:
            print("Stopping ...")
        finally:
            if cobra is not None:
                cobra.delete()

            if wav_file is not None:
                wav_file.close()

            if recorder is not None:
                recorder.delete()

        return output_path
