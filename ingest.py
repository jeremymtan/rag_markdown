import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from rag.document_loader import DocumentLoader
from rag.embeddings import EmbeddingService
from rag.vector_store import VectorStore


def main():
    print("starting ingestion...")

    # load and chunk documents
    loader = DocumentLoader()
    documents = loader.load_documents()
    chunks = loader.chunk_documents(documents)
    print(f"loaded {len(documents)} docs, created {len(chunks)} chunks")

    # initialize services
    embeddings_service = EmbeddingService()
    vector_store = VectorStore()

    # recreate collection
    # try:
    #     vector_store.delete_collection()
    # except:
    #     pass

    # vector_store.create_collection()

    # prepare data for embedding
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]

    print("generating embeddings...")
    embeddings = embeddings_service.embed_texts(texts)

    # upload to vector store
    print("uploading...")
    vector_store.add_documents(texts, embeddings, metadatas)


if __name__ == "__main__":
    main()
