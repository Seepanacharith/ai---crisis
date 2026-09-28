import pytest
from app.rag.splitter import RecursiveTextSplitter
from app.rag.prompts import build_prompt

def test_recursive_splitter():
    splitter = RecursiveTextSplitter(chunk_size=100, chunk_overlap=10)
    sample_docs = [{
        "content": "## Flood Safety\n1. Move to high ground immediately.\n2. Avoid walking through floodwaters.",
        "metadata": {"source": "flood.txt", "disaster_type": "flood", "document_name": "flood.txt"}
    }]
    chunks = splitter.split_documents(sample_docs)
    assert len(chunks) >= 1
    assert "disaster_type" in chunks[0]["metadata"]
    assert chunks[0]["metadata"]["disaster_type"] == "flood"

def test_prompt_construction():
    chunks = [{
        "content": "Move to higher ground immediately.",
        "metadata": {"source": "flood.txt", "section": "During Flood"}
    }]
    prompt = build_prompt(
        query="What to do in flood?",
        retrieved_chunks=chunks,
        disaster_type="flood",
        language="en"
    )
    assert "Move to higher ground immediately." in prompt
    assert "AI Crisis Companion" in prompt
