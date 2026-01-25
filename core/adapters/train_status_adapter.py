from typing import Optional
from core.api.api_registry import APIRegistry
from core.api.api_permission import APIPermission
from core.api.api_client import APIClient
from .adapter_response import AdapterResponse


class TrainStatusAdapter:
    """
    Read-only train status adapter (India).
    Strictly factual, stubbed, deterministic.
    """

    def __init__(self, permission: APIPermission):
        self.permission = permission
        self.client = APIClient()

    def get_status(
        self,
        *,
        pnr: Optional[str] = None,
        train_number: Optional[str] = None,
    ) -> AdapterResponse:
        # Exactly one identifier required
        if (pnr and train_number) or (not pnr and not train_number):
            raise ValueError("Provide exactly one of pnr or train_number")

        identifier = pnr or train_number
        if not isinstance(identifier, str) or not identifier.strip():
            raise ValueError("Invalid identifier")

        # Permission gate
        self.permission.check("train")

        # Registry contract (expects pnr-style param)
        contract = APIRegistry.get("train")

        # Use a single, deterministic param key for the stubbed client
        self.client.fetch(contract, {"pnr": identifier})

        # Deterministic stubbed status (no prediction)
        payload = {
            "train_number": train_number or "UNKNOWN",
            "status": "Running",
            "last_station": "NDLS",
            "delay_minutes": 0,
        }

        return AdapterResponse.build(
            title="Train Status",
            payload=payload,
            source="train",
        )
