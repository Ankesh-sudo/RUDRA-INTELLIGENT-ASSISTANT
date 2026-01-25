import pytest
from core.api.api_permission import APIPermission
from core.adapters.train_status_adapter import TrainStatusAdapter


def test_train_status_with_pnr():
    permission = APIPermission({"train"})
    adapter = TrainStatusAdapter(permission)

    result = adapter.get_status(pnr="1234567890")

    assert result.title == "Train Status"
    assert result.payload["status"] == "Running"
    assert result.payload["delay_minutes"] == 0


def test_train_status_with_train_number():
    permission = APIPermission({"train"})
    adapter = TrainStatusAdapter(permission)

    result = adapter.get_status(train_number="12951")

    assert result.payload["train_number"] == "12951"


def test_train_status_requires_permission():
    permission = APIPermission(set())
    adapter = TrainStatusAdapter(permission)

    with pytest.raises(Exception):
        adapter.get_status(pnr="1234567890")


def test_train_status_rejects_both_identifiers():
    permission = APIPermission({"train"})
    adapter = TrainStatusAdapter(permission)

    with pytest.raises(ValueError):
        adapter.get_status(pnr="123", train_number="456")


def test_train_status_rejects_missing_identifier():
    permission = APIPermission({"train"})
    adapter = TrainStatusAdapter(permission)

    with pytest.raises(ValueError):
        adapter.get_status()
