from core.memory.classifier import MemoryClassifier


def test_preference_classification():
    classifier = MemoryClassifier()
    text = "I like using dark mode"

    result = classifier.classify(text)

    assert result == "preference"


def test_habit_classification():
    classifier = MemoryClassifier()
    text = "I usually study at night"

    result = classifier.classify(text)

    assert result == "habit"


def test_fact_classification():
    classifier = MemoryClassifier()
    text = "My name is Ankesh"

    result = classifier.classify(text)

    assert result == "fact"


def test_ambiguous_classification_returns_none():
    classifier = MemoryClassifier()
    text = "I like studying at night"

    result = classifier.classify(text)

    assert result is None
