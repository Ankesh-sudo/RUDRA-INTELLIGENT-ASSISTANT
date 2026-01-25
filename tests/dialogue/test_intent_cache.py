import time
from core.dialogue.intent_cache import IntentCache


def test_intent_cache_expires():
    cache = IntentCache(ttl_sec=0.05)
    cache.set("SMALL_TALK")
    assert cache.get() == "SMALL_TALK"
    time.sleep(0.06)
    assert cache.get() is None
