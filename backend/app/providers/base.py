from abc import ABC, abstractmethod
from app.models.schemas import RequirementProfile, Product

class ProductProvider(ABC):
    @abstractmethod
    async def search(self, requirements: RequirementProfile, query: str) -> list[Product]:
        raise NotImplementedError
