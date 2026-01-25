from core.knowledge.engine import KnowledgeEngine
from core.knowledge.schema import DharmaRow

def test_engine_exact_match():
    rows = [DharmaRow("d","q","a","c")]
    ke = KnowledgeEngine(rows)
    res = ke.answer("q")
    assert res["answer"] == "a"
    assert res["citation"] == "c"
