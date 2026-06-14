import httpx
from app.models.schemas import Product, RequirementProfile
from app.providers.base import ProductProvider

class DummyJSONProvider(ProductProvider):
    async def search(self, requirements: RequirementProfile, query: str) -> list[Product]:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("https://dummyjson.com/products/search", params={"q": requirements.category or query, "limit": 10})
            response.raise_for_status()
        items = response.json().get("products", [])
        return [Product(id=str(i["id"]), title=i["title"], brand=i.get("brand") or "Unknown", category=i.get("category") or "general", image=i.get("thumbnail") or "", price=float(i.get("price", 0)) * 83, rating=float(i.get("rating", 0)), specs={"Description": i.get("description", ""), "Discount": f"{i.get('discountPercentage', 0)}%"}, reviews=[i.get("description", "")]) for i in items]
