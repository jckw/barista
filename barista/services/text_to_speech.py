import tempfile
import google.cloud.texttospeech as tts
import uuid


class GoogleTextToSpeech:
    def synthesize_speech(
        self,
        text,
    ):
        output_path = f"{tempfile.gettempdir()}/tts-barista-{uuid.uuid4()}.wav"

        text_input = tts.SynthesisInput(text=text)
        voice_params = tts.VoiceSelectionParams(
            language_code="en-Gb",
            name="en-GB-Standard-A",
        )
        audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
        client = tts.TextToSpeechClient()
        response = client.synthesize_speech(
            input=text_input, voice=voice_params, audio_config=audio_config
        )

        with open(output_path, "wb") as out:
            out.write(response.audio_content)
            print(f"Audio content written to file {output_path}")

        return output_path
