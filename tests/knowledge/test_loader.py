from core.knowledge.loader import load_dharma_csv
from core.knowledge.exceptions import KnowledgeValidationError
import tempfile, os

def test_loader_valid_csv():
    csv = "topic,question,answer,citation\na,b,c,d\n"
    with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as f:
        f.write(csv); path = f.name
    rows = load_dharma_csv(path)
    os.unlink(path)
    assert len(rows) == 1
