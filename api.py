"""simple api for chat interface"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.rag_chain import RAGChain

app = FastAPI()

# enable cors for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list


# initialize rag chain
rag = RAGChain()


@app.post("/api/query")
async def query(request):
    result = rag.query(request.question)
    return {"answer": result["answer"], "sources": result["sources"]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
