import re
from typing import List, Dict, Any
from app.config import settings

class RecursiveTextSplitter:
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        self.separators = ["\n## ", "\n### ", "\n\n", "\n", ". ", " "]

    def _split_text(self, text: str) -> List[str]:
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            if end >= len(text):
                chunks.append(text[start:])
                break
            
            # Find best separator
            cut = -1
            for sep in self.separators:
                pos = text.rfind(sep, start + int(self.chunk_size * 0.5), end)
                if pos != -1:
                    cut = pos + len(sep)
                    break
            
            if cut == -1:
                cut = end
            
            chunk = text[start:cut].strip()
            if chunk:
                chunks.append(chunk)
            
            start = max(start + 1, cut - self.chunk_overlap)

        return chunks

    def split_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        chunked_docs = []
        
        for doc in documents:
            raw_text = doc["content"]
            base_meta = doc["metadata"]
            source_file = base_meta["source"]
            disaster_type = base_meta["disaster_type"]
            
            sections = re.split(r'(?=\n##\s+)', raw_text)
            
            chunk_counter = 0
            for sec in sections:
                if not sec.strip():
                    continue
                
                # Extract section title if available
                first_line = sec.strip().split("\n")[0]
                section_title = first_line.replace("#", "").strip() if first_line.startswith("#") else "General Guidelines"
                
                chunks = self._split_text(sec)
                for chunk in chunks:
                    chunk_counter += 1
                    chunk_id = f"{disaster_type}_{chunk_counter:03d}"
                    
                    chunk_meta = {
                        "source": source_file,
                        "disaster_type": disaster_type,
                        "document_name": base_meta["document_name"],
                        "section": section_title,
                        "chunk_id": chunk_id
                    }
                    
                    chunked_docs.append({
                        "content": chunk,
                        "metadata": chunk_meta
                    })
                    
        return chunked_docs
