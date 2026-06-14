import os
from app.providers.base import ProductProvider
from app.providers.dummyjson import DummyJSONProvider
from app.providers.mock import MockProductProvider

def get_provider() -> ProductProvider:
    return DummyJSONProvider() if os.getenv("PRODUCT_PROVIDER") == "dummyjson" else MockProductProvider()
