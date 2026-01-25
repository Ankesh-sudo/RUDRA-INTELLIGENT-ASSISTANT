from .api_contract import APIContract
from .api_errors import APIRegistryError


class APIRegistry:
    """
    Static allow-list of APIs.
    """

    _REGISTRY = {
        "weather": APIContract(
            name="weather",
            endpoint="https://api.weather.example",
            method="GET",
            params_schema={"city": str},
        ),
        "news": APIContract(
            name="news",
            endpoint="https://api.news.example",
            method="GET",
            params_schema={"topic": str},
        ),
        "train": APIContract(
            name="train",
            endpoint="https://api.train.example",
            method="GET",
            params_schema={"pnr": str},
        ),
    }

    @classmethod
    def get(cls, name: str) -> APIContract:
        if name not in cls._REGISTRY:
            raise APIRegistryError(f"API not registered: {name}")

        contract = cls._REGISTRY[name]
        contract.validate()
        return contract
