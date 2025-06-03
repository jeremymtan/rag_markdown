# RAG w/ Mistral using Markdown Files

## Problem Statement 
Modern companies accumulate vast amounts of documentation across multiple repositories and platforms - employee handbooks, technical documentation, HR policies, and operational procedures. I assume this information is typically:
- Scattered across different markdown files
- Unstructured with inconsistent formatting and organization
- Inaccessible to non-technical users who need quick answers
- Time-consuming to search through manually, leading to repeated questions

## Target Users
1. HR Teams - need instant access to policy information for employee queries
2. Customer Support Representatives - require quick access to product documentation and troubleshooting guides
3. New Employees - seeking information about company policies, benefits, and procedures
4. Technical Teams - looking for deployment procedures and configuration details

For the non-technical users, I implement a web app to let them ask questions to chat w/ the LLM.
For technical users, I implement a cli tool to let them access in a terminal. 

## Measurable Outcomes 
1. Response Time - response needs to take <3 seconds 
2. Accuracy - response needs to be supported by the retrieved context 
3. Relevancy - retrieved context and response needs to align with user query

## Data Requirements
For this problem, I gathered documentation from various Github sources to simulate the problem. 
### Data Collection
- **Sources**: Public GitHub repositories containing company documentation
  - HR Manual (policies, benefits, procedures) from Basecamp
  - Technical Documentation (Kamal deployment docs) from Basecamp
  - Company Handbook (culture, remote work policies) from OpenGov
- **Format**: Markdown files with header hierarchies and metadata
- **Volume**: 60+ documents across 3 repositories

### Privacy & Quality Handling
- **Privacy**: API keys secured via environment variables
- **Quality Assurance**:
  - YAML frontmatter parsing to extract accurate titles
  - Header-aware chunking to preserve document structure
  - Source attribution for every response
  - Automated RAGAS evaluation for continuous quality monitoring
- **Data Processing**: Local LLM (Ollama/Mistral) ensures sensitive queries never leave the infrastructure

## Solution Design

### Components
1. **Semantic Embeddings** (Cohere): Transforms documents into high-dimensional vectors for similarity search
2. **Vector Similarity Search** (Qdrant): Vector database to store document chunks
3. **Large Language Model** (Mistral via Ollama): Generates natural language answers from retrieved context. I modularized so it can be swapped out w/ a different LLM if need be
4. **RAGAS Evaluation** (OpenAI GPT-4 w/ RAGAS): Automated quality assessment using AI as judge 

### Architecture

![Architecture Diagram](https://github.com/user-attachments/assets/84a0642e-fd47-49b0-bdc4-0cc68ee2d375)

## Installation & Setup

### Prerequisites
- Python 3.8+
- Docker (for Ollama)
- Git

### Quick Start
```bash
# clone repository
git clone https://github.com/jeremymtan/rag_markdown.git
cd rag_markdown

# install dependencies
make install

# set up environment variables
cp .env.example .env
# edit .env with your API keys:
# - COHERE_API_KEY (required)
# - QDRANT_URL & QDRANT_API_KEY (required)
# - OPENAI_API_KEY (for evaluation)

# install Ollama and pull Mistral
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull mistral

# collect and ingest documents
python data/data.py
python ingest.py
```

## Running the Application

### CLI Chat Interface
```bash
python query.py
# ex: "What is the vacation policy?"
```

### REST API
```bash
python api.py
# API available at http://localhost:8000
# ex: POST /api/query {"question": "How many weeks of parental leave?"}
```

### Web Interface (w/ REST API running)
```bash
cd web && npm install && npm run dev
# access at http://localhost:3000
```

## Evaluation

### Automated RAGAS Evaluation
```bash
make evaluate
# or
python evaluate_ragas.py
```

### Current Performance Metrics
- **Faithfulness**: 0.808333 (answers grounded in retrieved context)
- **Answer Relevancy**: 0.840166 (answers address the question)
- **Context Recall**: 0.500000 (relevant context retrieved)
- **Context Precision**: 0.53333 (retrieved context is focused)
- **Average Response Time**: ~1.5 seconds

### CI/CD Pipeline
GitHub Actions automatically runs evaluation on every push:
- RAGAS evaluation on test questions
- Results uploaded as artifacts

## Technical Implementation

### Why RAG Over Other Approaches

**RAG vs Fine-tuning**:
- RAG chosen for dynamic knowledge updates without retraining
- Fine-tuning would incur costs for each documentation update
- RAG allows source attribution for compliance and verification

**RAG vs Simple Prompting**:
- Documentation too large for context window (100K+ tokens)
- Enables precise retrieval of relevant sections only

### Design Decisions & Trade-offs

**1. Chunk Size Optimization**:
```
Tested configurations:
- 500 tokens: Higher precision (0.60) but poor context (many incomplete answers)
- 1000 tokens: Optimal balance - precision (0.53) with complete concepts
- 1500 tokens: Better context but precision dropped to 0.41

Chose 1000 tokens as it captures 3-4 paragraphs (complete policy sections)
```

**2. Retrieval Configuration**:
```
Top-K Analysis:
- k=3: Precision 0.65, Recall 0.40 (too restrictive)
- k=5: Precision 0.53, Recall 0.50 (balanced - current choice)
- k=7: Precision 0.45, Recall 0.61 (too noisy for LLM)
```

### Performance Analysis

**Query Type Performance Breakdown**:
| Query Type | Example | Avg Response Time |
|------------|---------|-------------------|
| Factual | "How many vacation days?" | 1.2s |
| Procedural | "How to request time off?" | 1.8s |
| Policy | "What is the remote work policy?" | 1.5s |
| Technical | "How to deploy with Kamal?" | 1.6s |

### Design Decisions
1. **Markdown-Aware Chunking**: Preserves document structure and header hierarchy. Markdown specific splitting then recursive character text splitting is used. 
2. **Local LLM**: Ensures data privacy and reduces costs
3. **Conciseness Prompting**: Adapted concise prompting reduces response length by 60% while maintaining accuracy

### Project Structure
```
repository/
├── data/                    # Data collection and scraped documents
│   ├── data.py             # GitHub markdown scraper with rate limiting
│   ├── docs/               # Kamal technical documentation
│   ├── handbook/           # Basecamp company handbook  
│   └── manual/             # OpenGov HR manual
│
├── rag/                    # Core RAG components
│   ├── document_loader.py  # Markdown chunking with header preservation
│   ├── embeddings.py       # Cohere embedding service with batching
│   ├── vector_store.py     # Qdrant operations and metadata indexing
│   ├── retriever.py        # Similarity search and context formatting
│   ├── llm.py             # Ollama/Mistral interface
│   └── rag_chain.py       # Main orchestration and prompting
│
├── web/                    # Next.js frontend
├── api.py                  # FastAPI backend
├── query.py               # CLI interface
├── ingest.py              # Document ingestion pipeline
├── evaluate_ragas.py      # RAGAS evaluation system
└── .github/workflows/ci.yml # CI/CD pipeline
```

## Current Limitations & Root Cause Analysis

### Low Context Precision (0.533)
**Root Causes**: 
1. **Fixed-size chunking splits semantic units**
   - Policy lists often split across chunks
   - Section headers separated from content
   
2. **Cross-organization terminology mismatch**
   - OpenGov HR Manual uses different terms than Basecamp Handbook
   - "Time off" vs "vacation" vs "PTO" across different sources
   - Retrieval returns similar concepts from wrong organization

**Impact**: Users receive incomplete or contextually mismatched answers requiring follow-up questions

### Low Context Recall (0.500)  
**Root Cause**: Single-embedding retrieval misses synonyms
- "Time off" doesn't match "vacation policy" (different embeddings)
- Technical jargon vs common terms mismatch
- No query expansion for ambiguous terms

**Impact**: Relevant documents missed in some of the queries (for the specific answer I was looking for)

### Query-Specific Performance Gaps
```
Strong Performance:
- Direct queries: "How many days of vacation?"
- Exact term matches: "Parental leave policy"

Weak Performance:
- Conceptual queries: "How does the company support work-life balance?"
- Multi-hop queries: "Can I work remotely from another country?"
```

## Future Work 
1. **Semantic Chunking**: Implement sentence-transformer based chunking to respect semantic boundaries   
2. **Query Expansion**: Generate 2-3 related queries to improve recall
3. **Organization-Aware Retrieval**: Add source weighting to prioritize documents from the relevant organization
   - Detect company context from query ("Basecamp's policy on...")
   - Boost scores for matching organization documents

### Other Enhancements
1. **Reranking Layer**: Implement Cohere rerank or cross-encoder   
2. **Dynamic K Selection**: Adjust retrieval count based on confidence scores
   - If top result >0.9 similarity: k=3
   - If top result <0.7 similarity: k=7
3. **Conversational Memory**: Handle follow-up questions in context

## References
- HR Manual: https://github.com/opengovfoundation/hr-manual
- Kamal Documentation: https://github.com/basecamp/kamal
- Basecamp Handbook: https://github.com/basecamp/handbook 
- Qdrant: https://python-client.qdrant.tech/
- Cohere: https://docs.cohere.com/reference/about
- RAGAS: https://docs.ragas.io/en/





