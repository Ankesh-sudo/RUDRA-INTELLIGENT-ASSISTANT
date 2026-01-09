"""
Day 20.3 Test — Slot & Preference Merger

Purpose:
- Ensure preferences act only as defaults
- Ensure explicit user slots are never overridden
- Lock safe merge behavior
"""

from core.memory.slot_preference_merger import SlotPreferenceMerger


def test_preference_does_not_override_existing_slot():
    merger = SlotPreferenceMerger()

    slots = {"browser": "firefox"}
    preferences = [{"key": "browser", "value": "chrome"}]

    merged = merger.merge(
        slots=slots,
        preferences=preferences,
        allowed_keys={"browser"}
    )

    # Explicit slot must win
    assert merged["browser"] == "firefox"


def test_preference_fills_missing_slot():
    merger = SlotPreferenceMerger()

    slots = {}
    preferences = [{"key": "browser", "value": "chrome"}]

    merged = merger.merge(
        slots=slots,
        preferences=preferences,
        allowed_keys={"browser"}
    )

    assert merged["browser"] == "chrome"


def test_preference_ignored_if_key_not_allowed():
    merger = SlotPreferenceMerger()

    slots = {}
    preferences = [{"key": "volume", "value": 70}]

    merged = merger.merge(
        slots=slots,
        preferences=preferences,
        allowed_keys={"browser"}
    )

    assert merged == {}
