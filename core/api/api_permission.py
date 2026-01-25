from .api_errors import APIPermissionDenied


class APIPermission:
    """
    Explicit consent gate.
    """

    def __init__(self, allowed_apis: set[str]):
        self.allowed_apis = allowed_apis

    def check(self, api_name: str) -> None:
        if api_name not in self.allowed_apis:
            raise APIPermissionDenied(f"Permission denied for API: {api_name}")
