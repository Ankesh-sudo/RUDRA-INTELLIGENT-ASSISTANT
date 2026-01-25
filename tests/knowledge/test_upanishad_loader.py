import tempfile, os
from core.knowledge.upanishad_loader import load_upanishad_csv

def test_upanishad_loader_valid():
    csv = "topic,question,answer,text,verse,citation\nmoksha,q,a,Isha Upanishad,1,Isha Upanishad 1\n"
    with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as f:
        f.write(csv); path = f.name
    rows = load_upanishad_csv(path)
    os.unlink(path)
    assert rows[0].citation == "Isha Upanishad 1"
