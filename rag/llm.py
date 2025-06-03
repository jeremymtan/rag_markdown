import os
import ollama
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    def __init__(self, model=None):
        self.model = model or os.getenv("OLLAMA_MODEL", "mistral")
        self._check_model()

    def _check_model(self):
        try:
            ollama.show(self.model)
        except ollama.ResponseError:
            print(f"pulling {self.model}...")
            ollama.pull(self.model)

    def generate(self, prompt, context=None, system_prompt=None):
        # generate response using ollama
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if context:
            user_message = f"Context:\n{context}\n\nQuestion: {prompt}"
        else:
            user_message = prompt

        messages.append({"role": "user", "content": user_message})

        response = ollama.chat(model=self.model, messages=messages)

        return response["message"]["content"]

    def stream_generate(self, prompt, context=None, system_prompt=None):
        # generate streaming response using ollama
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if context:
            user_message = f"Context:\n{context}\n\nQuestion: {prompt}"
        else:
            user_message = prompt

        messages.append({"role": "user", "content": user_message})

        stream = ollama.chat(model=self.model, messages=messages, stream=True)

        for chunk in stream:
            yield chunk["message"]["content"]
