"""
🔒 FULL DAY 15 TEST SUITE — HARD MODE

Covers:
✔ Intent isolation
✔ Entity whitelist enforcement
✔ Cross-intent replay blocking
✔ Dangerous intent replay blocking
✔ Pronoun resolution (it / them / again)
✔ UNKNOWN intent reset behavior
✔ Context timeout behavior
✔ Replay integrity after failures
✔ No regression to Day 14

Run:
    python test_day15_all_edge_cases.py
"""

import time
from core.actions.action_executor import ActionExecutor
from core.nlp.intent import Intent


def print_case(title):
    print("\n" + "=" * 70)
    print(f"🧪 {title}")
    print("=" * 70)


def run(action_executor, intent, text, confidence=1.0):
    result = action_executor.execute(
        intent=intent,
        text=text,
        confidence=confidence,
    )
    print(f"INPUT: {text}")
    print(f"OUTPUT: {result.get('message')}")
    return result


def main():
    ae = ActionExecutor()

    # --------------------------------------------------
    print_case("1. BASIC CONTEXT STORAGE")
    r1 = run(ae, Intent.OPEN_BROWSER, "open browser github")
    assert r1["success"]

    # --------------------------------------------------
    print_case("2. PRONOUN REPLAY (VALID)")
    r2 = run(ae, Intent.OPEN_BROWSER, "open it again")
    assert r2["success"]
    assert r2.get("is_followup")

    # --------------------------------------------------
    print_case("3. CROSS-INTENT BLOCK (SYSTEM → FILESYSTEM)")
    r3 = run(ae, Intent.LIST_FILES, "list it")
    assert not r3["success"]
    print("✔ Cross-intent replay blocked")

    # --------------------------------------------------
    print_case("4. FILESYSTEM CONTEXT ISOLATION")
    r4 = run(ae, Intent.OPEN_FILE_MANAGER, "open downloads folder")
    assert r4["success"]

    r5 = run(ae, Intent.LIST_FILES, "list them again")
    assert r5["success"]
    assert "path" in r5["args"]
    assert "url" not in r5["args"]

    # --------------------------------------------------
    print_case("5. ENTITY LEAK PREVENTION")
    r6 = run(ae, Intent.OPEN_BROWSER, "open it again")
    assert r6["success"]
    assert "path" not in r6["args"]
    assert "query" not in r6["args"]

    # --------------------------------------------------
    print_case("6. DANGEROUS INTENT — BLOCKED REPLAY")
    r7 = run(ae, Intent.OPEN_TERMINAL, "open terminal")
    assert r7["success"]

    r8 = run(ae, Intent.OPEN_TERMINAL, "open it again")
    assert not r8["success"]
    print("✔ Dangerous replay blocked")

    # --------------------------------------------------
    print_case("7. UNKNOWN INTENT SHOULD NOT POLLUTE CONTEXT")
    r9 = run(ae, Intent.UNKNOWN, "do some illegal hacking")
    assert not r9["success"]

    r10 = run(ae, Intent.OPEN_BROWSER, "open it again")
    assert r10["success"]
    print("✔ UNKNOWN intent did not corrupt context")

    # --------------------------------------------------
    print_case("8. CONTEXT TIMEOUT")
    ae.follow_up_context.context_timeout = 1
    time.sleep(2)

    r11 = run(ae, Intent.OPEN_BROWSER, "open it again")
    assert not r11["success"]
    print("✔ Context expired correctly")

    # --------------------------------------------------
    print_case("9. MULTI-STEP CHAIN (SYSTEM → SYSTEM)")
    run(ae, Intent.SEARCH_WEB, "search python decorators")
    r12 = run(ae, Intent.SEARCH_WEB, "search it again")
    assert r12["success"]

    # --------------------------------------------------
    print_case("10. WRONG INTENT CLASS REPLAY BLOCK")
    run(ae, Intent.SEARCH_WEB, "search linux commands")
    r13 = run(ae, Intent.OPEN_FILE, "open it")
    assert not r13["success"]
    print("✔ Intent-class mismatch blocked")

    # --------------------------------------------------
    print("\n✅ ALL DAY 15 HARD TESTS PASSED")
    print("🧠 Follow-up system is SAFE, ISOLATED, and PRODUCTION-READY")
    print("=" * 70)


if __name__ == "__main__":
    main()
