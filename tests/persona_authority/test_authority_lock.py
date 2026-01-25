from core.persona_authority.authority_lock import AuthorityLock


def test_authority_lock_is_active():
    assert AuthorityLock.is_locked() is True


def test_authority_lock_irreversible():
    AuthorityLock.engage()
    assert AuthorityLock.is_locked() is True
