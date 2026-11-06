"""Simple local retrieval layer for grounding mentor answers in uploaded text.

This is lexical retrieval (not a trained embedding model). It needs no external
vector database and can be replaced by a hosted vector store later.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import math, re
from collections import Counter

_TOKEN = re.compile(r"[a-zA-Z0-9_+#.-]+")

@dataclass
class KnowledgeChunk:
    source: str
    chunk_id: int
    text: str

class LocalKnowledgeBase:
    def __init__(self, chunk_words: int = 180, overlap_words: int = 30):
        if chunk_words < 30 or overlap_words < 0 or overlap_words >= chunk_words:
            raise ValueError("Use chunk_words >= 30 and 0 <= overlap_words < chunk_words.")
        self.chunk_words, self.overlap_words = chunk_words, overlap_words
        self._chunks: list[KnowledgeChunk] = []

    @property
    def size(self) -> int:
        return len(self._chunks)

    def add_text(self, source: str, text: str) -> int:
        if not source.strip() or not text.strip():
            raise ValueError("source and text must be non-empty.")
        words = text.split()
        step = self.chunk_words - self.overlap_words
        start, count = 0, 0
        while start < len(words):
            part = " ".join(words[start:start+self.chunk_words]).strip()
            if part:
                self._chunks.append(KnowledgeChunk(source=source, chunk_id=count, text=part))
                count += 1
            start += step
        return count

    def add_file(self, path: str | Path) -> int:
        file = Path(path)
        if not file.is_file():
            raise FileNotFoundError(str(file))
        suffix = file.suffix.lower()
        if suffix == ".pdf":
            try:
                from pypdf import PdfReader
            except ImportError as exc:
                raise RuntimeError("Install pypdf to ingest PDF files.") from exc
            text = "\n".join(page.extract_text() or "" for page in PdfReader(str(file)).pages)
        elif suffix == ".docx":
            try:
                from docx import Document
            except ImportError as exc:
                raise RuntimeError("Install python-docx to ingest DOCX files.") from exc
            doc = Document(str(file))
            text = "\n".join(p.text for p in doc.paragraphs)
        elif suffix in {".txt", ".md", ".csv", ".json", ".py"}:
            text = file.read_text(encoding="utf-8", errors="replace")
        else:
            raise ValueError("Supported files: .txt, .md, .csv, .json, .py, .pdf, .docx")
        if not text.strip():
            raise ValueError("No extractable text found in the file.")
        return self.add_text(file.name, text)

    def search(self, query: str, top_k: int = 4) -> list[dict]:
        if not query.strip():
            raise ValueError("query cannot be empty.")
        if top_k < 1 or top_k > 20:
            raise ValueError("top_k must be between 1 and 20.")
        q = Counter(t.lower() for t in _TOKEN.findall(query))
        if not q or not self._chunks:
            return []
        docs = [Counter(t.lower() for t in _TOKEN.findall(c.text)) for c in self._chunks]
        df = Counter(token for doc in docs for token in doc.keys())
        total = len(docs)
        scored=[]
        for chunk, doc in zip(self._chunks, docs):
            score=0.0
            for token, qcount in q.items():
                tf=doc.get(token,0)
                if tf:
                    idf=math.log(1 + (total-df[token]+0.5)/(df[token]+0.5))
                    score += qcount * idf * (tf*2.2)/(tf+1.2)
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{**asdict(chunk), "score": round(score, 4)} for score, chunk in scored[:top_k]]
