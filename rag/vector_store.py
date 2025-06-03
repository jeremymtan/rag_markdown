import os
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue, PayloadSchemaType
)

load_dotenv()


class VectorStore:
    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )
        self.collection_name = os.getenv("COLLECTION_NAME", "tako_docs")
    
    def create_collection(self, vector_size=1024):
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="source",
                field_schema=PayloadSchemaType.KEYWORD
            )
            print(f"created collection '{self.collection_name}' with index")
            
        except Exception as e:
            if "already exists" in str(e):
                print(f"collection already exists")
            else:
                raise e
    
    def add_documents(self, texts, embeddings, metadatas):
        points = []
        
        for text, embedding, metadata in zip(texts, embeddings, metadatas):
            point_id = str(uuid.uuid4())
            
            payload = {
                "text": text,
                **metadata
            }
            
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
            )
        
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch
            )
            print(f"uploaded {min(i + batch_size, len(points))}/{len(points)}")
    
    def search(self, query_embedding, top_k=5, source_filter=None):
        
        search_params = {
            "collection_name": self.collection_name,
            "query_vector": query_embedding,
            "limit": top_k,
            "with_payload": True,
        }
        
        if source_filter:
            search_params["query_filter"] = Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(value=source_filter)
                    )
                ]
            )
        
        results = self.client.search(**search_params)
        
        return [
            {
                "text": hit.payload.get("text", ""),
                "metadata": {k: v for k, v in hit.payload.items() if k != "text"},
                "score": hit.score
            }
            for hit in results
        ]
    
    def delete_collection(self):
        self.client.delete_collection(collection_name=self.collection_name)
        print(f"deleted collection")