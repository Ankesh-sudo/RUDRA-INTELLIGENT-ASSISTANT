import tempfile, os
from core.knowledge.gita_loader import load_gita_csv

def test_gita_loader_valid():
    csv = (
        "topic,question,answer,chapter,verse,citation\n"
        "karma,q,a,2,47,Bhagavad Gita 2.47\n"
    )
    with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as f:
        f.write(csv); path = f.name
    rows = load_gita_csv(path)
    os.unlink(path)
    assert rows[0].chapter == 2
    assert rows[0].verse == 47
