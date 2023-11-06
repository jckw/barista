from services.wake_word_detector import WakeWordDetector
from services.audio_recorder import AudioRecorder
from services.speech_to_text import WhisperSpeechToText
from services.text_to_speech import GoogleTextToSpeech
from services.response_agent import ResponseAgent
from utils.audio_player import AudioPlayer
from dotenv import load_dotenv
import os

load_dotenv()


def on_wake_word_detected():
    print("Wake word detected!")

    file_path = audio_recorder.start_recording()
    print("Audio recording complete.")

    transcript = stt_service.transcribe_audio(file_path)
    print(f"Transcription: {transcript}")

    for sentence in agent_service.stream_response_as_sentences(transcript):
        response_audio = tts_service.synthesize_speech(sentence)
        audio_player.play_audio(response_audio)


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
