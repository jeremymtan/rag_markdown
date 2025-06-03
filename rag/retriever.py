from .embeddings import EmbeddingService
from .vector_store import VectorStore


class Retriever:
    def __init__(self):
        self.embeddings = EmbeddingService()
        self.vector_store = VectorStore()

    # retrieve top 5 sources by default
    def retrieve(self, query, top_k=5, source_filter=None):
        # get embedding for the query
        query_embedding = self.embeddings.embed_query(query)

        # search for similar documents
        results = self.vector_store.search(
            query_embedding=query_embedding, top_k=top_k, source_filter=source_filter
        )

        return results

    def format_context(self, results):
        # format retrieved documents into context string
        context_parts = []

        for i, result in enumerate(results):
            metadata = result["metadata"]
            source = metadata.get("source", "Unknown")
            title = metadata.get("title", metadata.get("file_name", "Unknown"))

            context_parts.append(f"Source {i+1} ({source} - {title}):")
            context_parts.append(result["text"])
            context_parts.append("")

        return "\n".join(context_parts)
