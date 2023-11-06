from utils.sequential_queue import SequentialQueue
from services.wake_word_detector import WakeWordDetector
from services.audio_recorder import AudioRecorder
from services.speech_to_text import WhisperSpeechToText
from services.text_to_speech import GoogleTextToSpeech
from services.response_agent import ResponseAgent
from utils.audio_player import AudioPlayer
from dotenv import load_dotenv
import os
import threading

load_dotenv()


def play_audio_sequence(sq):
    while True:
        next_file_path = sq.get_next()
        if next_file_path is None:
            print("End of queue reached.")
            break
        audio_player.play_audio(next_file_path)


def fetch_and_add_audio(sq, sentence, seq_num):
    file_path = tts_service.synthesize_speech(sentence)
    sq.add(file_path, seq_num)


def on_wake_word_detected():
    print("Wake word detected!")
    # TODO: Stop any audio that is currently playing, and continue listening for the
    # wake word again

    file_path = audio_recorder.start_recording()
    print("Audio recording complete.")

    transcript = stt_service.transcribe_audio(file_path)
    print(f"Transcription: {transcript}")

    sq = SequentialQueue()

    threading.Thread(
        target=play_audio_sequence,
        args=(sq,),
    ).start()

    last_i = 0
    for i, sentence in enumerate(
        agent_service.stream_response_as_sentences(transcript)
    ):
        last_i = i
        # Start a new thread to fetch the audio for the next sentence
        threading.Thread(
            target=fetch_and_add_audio,
            args=(
                sq,
                sentence,
                i + 1,
            ),
        ).start()

    sq.mark_end(last_i + 2)


# Initialize services
audio_recorder = AudioRecorder(os.environ["PICOVOICE_ACCESS_KEY"])
stt_service = WhisperSpeechToText(os.environ["OPENAI_API_KEY"])
agent_service = ResponseAgent(os.environ["OPENAI_API_KEY"])
tts_service = GoogleTextToSpeech()
audio_player = AudioPlayer()

# Initialize wake word detector and start listening
wake_word_detector = WakeWordDetector(
    picovoice_access_key=os.environ["PICOVOICE_ACCESS_KEY"],
    detected_callback=on_wake_word_detected,
)

while True:
    wake_word_detector.listen_for_wake_word()
