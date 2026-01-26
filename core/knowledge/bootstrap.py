# core/knowledge/bootstrap.py

from pathlib import Path

from core.knowledge.loader import load_dharma_csv
from core.knowledge.engine import KnowledgeEngine


def build_knowledge_engine() -> KnowledgeEngine:
    """
    Loads all Dharma knowledge and returns a ready engine.
    Called ONCE at startup.
    """

    project_root = Path(__file__).resolve().parents[2]
    dharma_dir = project_root / "data" / "dharma"
    csv_path = dharma_dir / "dharma_base.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Dharma CSV not found at {csv_path}")

    # load_dharma_csv RETURNS List[DharmaRow]
    rows = load_dharma_csv(path=str(csv_path))

    return KnowledgeEngine(rows)
