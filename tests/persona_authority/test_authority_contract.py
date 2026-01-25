from core.persona_authority.authority_contract import AuthorityContract


def test_forbidden_capabilities_exist():
    assert AuthorityContract.is_forbidden("execute_actions")
    assert AuthorityContract.is_forbidden("access_memory")
    assert not AuthorityContract.is_forbidden("speak_text")
