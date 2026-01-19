from typing import List
from core.nlp.intent import Intent

class IntentSequence:
    def __init__(self, intents: List[Intent]):
        self.intents = intents

    def ordered(self) -> List[Intent]:
        return sorted(self.intents, key=lambda i: i.sequence_index)
