from services.wake_word_detector import PorcupineWakeWordDetector
from services.audio_recorder import AudioRecorder
from services.speech_to_text import WhisperSpeechToText
from services.text_to_speech import GoogleTextToSpeech
from utils.audio_player import AudioPlayer


def on_wake_word_detected():
    print("Wake word detected!")
    # Start recording the command after wake word is detected
    file_path = audio_recorder.record_audio()
    print("Audio recording complete.")
    # Transcribe the audio to text
    transcript = stt_service.transcribe_audio(file_path)
    # TODO: Get response from response agent
    print(f"Transcription: {transcript}")
    # Generate and play a response (as a placeholder, we use a static text)
    response_audio = tts_service.synthesize_speech(
        "I heard you, what can I do for you?"
    )
    audio_player.play_audio(response_audio)


# Initialize services
audio_recorder = AudioRecorder()
stt_service = WhisperSpeechToText()
tts_service = GoogleTextToSpeech(api_key="Your-Google-API-Key")
audio_player = AudioPlayer()

# Initialize wake word detector and start listening
wake_word_detector = PorcupineWakeWordDetector(
    picovoice_access_key="Your-Picovoice-Access-Key",
    detected_callback=on_wake_word_detected,
)
wake_word_detector.listen_for_wake_word()
