import os
from typing import List, Dict, Any
import logging

logger = logging.getLogger("crisis_companion.rag.loader")

class DocumentLoader:
    def __init__(self, knowledge_base_dir: str):
        self.knowledge_base_dir = knowledge_base_dir

    def load_documents(self) -> List[Dict[str, Any]]:
        documents = []
        if not os.path.exists(self.knowledge_base_dir):
            logger.warning(f"Knowledge base directory {self.knowledge_base_dir} does not exist!")
            return documents

        for filename in os.listdir(self.knowledge_base_dir):
            if filename.endswith((".txt", ".md", ".json")):
                filepath = os.path.join(self.knowledge_base_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    disaster_type = filename.split(".")[0]
                    if disaster_type not in ["flood", "earthquake", "fire", "cyclone", "emergency_kit", "evacuation", "first_aid"]:
                        disaster_type = "general"

                    documents.append({
                        "content": content,
                        "metadata": {
                            "source": filename,
                            "disaster_type": disaster_type,
                            "document_name": filename,
                            "path": filepath
                        }
                    })
                    logger.info(f"Successfully loaded document: {filename}")
                except Exception as e:
                    logger.error(f"Failed to load document {filename}: {e}")
        return documents
