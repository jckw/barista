from litellm import completion
import os


class ResponseAgent:
    def __init__(self, openai_api_key):
        os.environ["OPENAI_API_KEY"] = openai_api_key

    def messages(self, text):
        return [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
        ]

    def get_response(self, text):
        res = completion(model="gpt-4", messages=self.messages(text))

        return res["choices"][0]["message"]["content"]

    def stream_response(self, text):
        res = completion(model="gpt-4", messages=self.messages(text), stream=True)

        for chunk in res:
            if chunk["choices"][0]["finish_reason"] == "stop":
                break
            yield chunk["choices"][0]["delta"]["content"]

    def stream_response_as_sentences(self, text):
        sentence = ""
        for chunk in self.stream_response(text):
            sentence += chunk
            if sentence.endswith((".", "!", "?")):
                yield sentence
                sentence = ""
        if sentence:
            yield sentence
