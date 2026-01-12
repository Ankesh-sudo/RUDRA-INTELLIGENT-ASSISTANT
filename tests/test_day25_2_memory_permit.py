from datetime import datetime, timedelta

import pytest

from core.memory.permit import MemoryPermit
from core.memory.usage_mode import MemoryUsageMode
from core.memory.guards import ensure_valid_permit


def test_permit_is_immutable():
    permit = MemoryPermit(mode=MemoryUsageMode.ONCE)
    with pytest.raises(Exception):
        permit.mode = MemoryUsageMode.SESSION


def test_permit_not_expired_by_default():
    permit = MemoryPermit(mode=MemoryUsageMode.ONCE)
    assert permit.is_expired() is False


def test_permit_expiry_detection():
    expired = MemoryPermit(
        mode=MemoryUsageMode.ONCE,
        expires_at=datetime.utcnow() - timedelta(seconds=1),
    )
    assert expired.is_expired() is True


def test_guard_blocks_expired_permit():
    expired = MemoryPermit(
        mode=MemoryUsageMode.ONCE,
        expires_at=datetime.utcnow() - timedelta(seconds=1),
    )
    with pytest.raises(PermissionError):
        ensure_valid_permit(expired)
