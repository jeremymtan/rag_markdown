import os
from time import sleep
from dotenv import load_dotenv
import cohere

load_dotenv()


class EmbeddingService:
    def __init__(self):
        self.client = cohere.Client(os.getenv("COHERE_API_KEY"))
        self.model = os.getenv("EMBEDDING_MODEL", "embed-english-v3.0")
        self.batch_size = 96

    def embed_texts(self, texts):
        embeddings = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]

            try:
                response = self.client.embed(
                    texts=batch, model=self.model, input_type="search_document"
                )
                embeddings.extend(response.embeddings)

                if i + self.batch_size < len(texts):
                    sleep(0.1)

            except Exception as e:
                print(f"error: batch {i//self.batch_size}")
                embeddings.extend([[0.0] * 1024] * len(batch))

        return embeddings

    def embed_query(self, query):
        try:
            response = self.client.embed(
                texts=[query], model=self.model, input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            print(f"error: query embedding")
            return [0.0] * 1024
