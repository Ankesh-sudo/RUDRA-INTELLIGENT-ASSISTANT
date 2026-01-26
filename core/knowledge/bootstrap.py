# core/knowledge/bootstrap.py

from core.knowledge.loader import load_dharma_csv
from core.knowledge.engine import KnowledgeEngine


def build_knowledge_engine() -> KnowledgeEngine:
    """
    Loads all Dharma knowledge and returns a ready engine.
    Called ONCE at startup.
    """
    loader = load_dharma_csv()
    rows = loader.load_all()
    return KnowledgeEngine(rows)
