from core.knowledge.engine import KnowledgeEngine
from core.knowledge.explain_surface import KnowledgeExplainSurface
from core.knowledge.schema import DharmaRow


def test_explain_surface_hit():
    rows = [DharmaRow("dharma","q","a","c")]
    ke = KnowledgeEngine(rows)
    es = KnowledgeExplainSurface(ke)

    res = es.respond("q")
    assert res["answer"] == "a"
    assert res["citation"] == "c"
    assert res["topic"] == "dharma"


def test_explain_surface_miss():
    ke = KnowledgeEngine([])
    es = KnowledgeExplainSurface(ke)

    res = es.respond("unknown question")
    assert res["topic"] == "unknown"
    assert res["citation"] == ""
    assert "verified sources" in res["answer"]
