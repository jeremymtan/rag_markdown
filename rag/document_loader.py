from pathlib import Path
import os
from langchain.text_splitter import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()


class DocumentLoader:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.sources = ["manual", "docs", "handbook"]
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "1000"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "200"))

        # first split by markdown headers
        self.header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header_1"),
                ("##", "Header_2"),
                ("###", "Header_3"),
            ]
        )

        # then split large sections into smaller chunks
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len,
        )

    def load_documents(self):
        documents = []

        for source in self.sources:
            source_dir = self.data_dir / source
            if source_dir.exists():
                for file_path in source_dir.glob("*.md"):
                    doc = self._load_single_document(file_path, source)
                    if doc:
                        documents.append(doc)

        return documents

    def _load_single_document(self, file_path, source):
        try:
            content = file_path.read_text(encoding="utf-8")

            metadata = {
                "source": source,
                "file_name": file_path.name,
                "file_path": str(file_path),
            }

            title = self._extract_title(content)
            if title:
                metadata["title"] = title

            return Document(page_content=content, metadata=metadata)

        except Exception as e:
            print(f"error: {e}")
            return None

    def _extract_title(self, content):
        lines = content.split("\n")
        in_frontmatter = False

        for i, line in enumerate(lines):
            # skip frontmatter (between --- markers)
            if line.strip() == "---":
                if i == 0:
                    in_frontmatter = True
                    continue
                elif in_frontmatter:
                    in_frontmatter = False
                    continue

            if in_frontmatter:
                # check for title in frontmatter
                if line.startswith("title:"):
                    return line.replace("title:", "").strip()
                continue

            # skip comment lines from kama docs
            if line.strip().startswith("#") and "This file has been generated" in line:
                continue

            # find first real heading
            if line.strip().startswith("# "):
                return line.strip("# ").strip()

        return ""

    def chunk_documents(self, documents):
        chunks = []

        for doc in documents:
            # first split by headers to maintain markdown structure
            header_splits = self.header_splitter.split_text(doc.page_content)

            # process each header-based section
            for header_doc in header_splits:
                # create a document with combined metadata
                section_metadata = {**doc.metadata}

                # add header hierarchy to metadata if present
                if hasattr(header_doc, "metadata") and header_doc.metadata:
                    for key, value in header_doc.metadata.items():
                        if value:  # only add non-empty header values
                            section_metadata[key] = value

                # create document for this section
                if hasattr(header_doc, "page_content"):
                    content = header_doc.page_content
                else:
                    content = str(header_doc)

                section_doc = Document(page_content=content, metadata=section_metadata)

                # if section is still too large, split it further
                if len(content) > self.chunk_size:
                    sub_chunks = self.text_splitter.split_documents([section_doc])
                    for i, chunk in enumerate(sub_chunks):
                        chunk.metadata["chunk_id"] = len(chunks)
                        chunk.metadata["chunk_type"] = "subsection"
                        chunks.append(chunk)
                else:
                    section_doc.metadata["chunk_id"] = len(chunks)
                    section_doc.metadata["chunk_type"] = "section"
                    chunks.append(section_doc)

        # update total chunks count
        for chunk in chunks:
            chunk.metadata["total_chunks"] = len(chunks)

        return chunks
