from core.knowledge.engine import KnowledgeEngine
from core.knowledge.gita_schema import GitaRow

def test_gita_exact_match():
    rows = [GitaRow("karma","q","a",2,47,"Bhagavad Gita 2.47")]
    ke = KnowledgeEngine(rows)
    res = ke.answer("q")
    assert res["citation"] == "Bhagavad Gita 2.47"
