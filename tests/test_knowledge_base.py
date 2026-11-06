from ai_engine.knowledge.retriever import LocalKnowledgeBase
import pytest

def test_retrieval_returns_relevant_chunk():
    kb=LocalKnowledgeBase(chunk_words=30, overlap_words=5)
    kb.add_text("notes.md", "Python machine learning classification model spam email features labels precision recall dataset.")
    result=kb.search("spam email classification", top_k=2)
    assert result and result[0]["source"] == "notes.md"

def test_retrieval_validates_query():
    kb=LocalKnowledgeBase()
    with pytest.raises(ValueError): kb.search(" ")
