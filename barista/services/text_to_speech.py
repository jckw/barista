import requests
import json


class GoogleTextToSpeech:
    def __init__(self, api_key="Your-Google-API-Key"):
        self.api_key = api_key

    def synthesize_speech(self, text, output_file="response.mp3"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json; charset=utf-8",
        }
        data = {
            "input": {"text": text},
            "voice": {
                "languageCode": "en-gb",
                "name": "en-GB-Standard-A",
                "ssmlGender": "FEMALE",
            },
            "audioConfig": {"audioEncoding": "MP3"},
        }
        response = requests.post(
            "https://texttospeech.googleapis.com/v1/text:synthesize",
            headers=headers,
            data=json.dumps(data),
        )
        response_json = response.json()
        audio_content = response_json["audioContent"]
        with open(output_file, "wb") as audio_file:
            audio_file.write(audio_content)
        return output_file
