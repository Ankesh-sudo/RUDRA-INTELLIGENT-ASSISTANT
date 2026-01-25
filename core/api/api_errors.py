class APIError(Exception):
    pass


class APIPermissionDenied(APIError):
    pass


class APIRegistryError(APIError):
    pass


class APIClientTimeout(APIError):
    pass


class APIInvalidResponse(APIError):
    pass
