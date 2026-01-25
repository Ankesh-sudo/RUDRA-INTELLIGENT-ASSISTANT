import tempfile, os
from core.knowledge.yoga_loader import load_yoga_csv

def test_yoga_loader_valid():
    csv = "topic,question,answer,chapter,sutra,citation\nyoga,q,a,1,2,Yoga Sutra 1.2\n"
    with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as f:
        f.write(csv); path = f.name
    rows = load_yoga_csv(path)
    os.unlink(path)
    assert rows[0].citation == "Yoga Sutra 1.2"
