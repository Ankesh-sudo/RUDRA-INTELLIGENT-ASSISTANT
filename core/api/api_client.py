from typing import Dict, Any
from .api_contract import APIContract
from .api_response import APIResponse
from .api_errors import APIClientTimeout


class APIClient:
    """
    Executes exactly one API call (stubbed).
    """

    def fetch(
        self,
        contract: APIContract,
        params: Dict[str, Any],
        timeout_seconds: int = 3,
    ) -> APIResponse:

        # Parameter validation
        for key, expected_type in contract.params_schema.items():
            if key not in params:
                raise ValueError(f"Missing param: {key}")
            if not isinstance(params[key], expected_type):
                raise ValueError(f"Invalid type for param: {key}")

        # Stubbed response (NO real HTTP)
        if timeout_seconds <= 0:
            raise APIClientTimeout("Request timed out")

        fake_data = {
            "endpoint": contract.endpoint,
            "params": params,
        }

        return APIResponse.build(
            data=fake_data,
            source=contract.name,
        )
