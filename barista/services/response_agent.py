from litellm import completion
import os


class ResponseAgent:
    def __init__(self, openai_api_key):
        os.environ["OPENAI_API_KEY"] = openai_api_key

    def get_response(self, text):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
        ]
        res = completion(model="gpt-4", messages=messages)

        return res["choices"][0]["message"]["content"]
