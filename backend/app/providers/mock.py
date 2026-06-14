from app.models.schemas import Product, RequirementProfile
from app.providers.base import ProductProvider

MOCK_PRODUCTS = [
    Product(id="lap-1", title="Acer Nitro V 15", brand="Acer", category="laptop", image="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800", price=74990, rating=4.4, specs={"CPU":"Intel i5-13420H","GPU":"RTX 4050 6GB","RAM":"16GB","Storage":"512GB SSD","Weight":"2.1 kg","Battery":"57Wh"}, reviews=["Excellent gaming performance for the money", "Fans get loud under load", "Good keyboard for coding"]),
    Product(id="lap-2", title="ASUS TUF Gaming A15", brand="ASUS", category="laptop", image="https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=800", price=78990, rating=4.5, specs={"CPU":"Ryzen 7 7735HS","GPU":"RTX 3050 4GB","RAM":"16GB","Storage":"1TB SSD","Weight":"2.2 kg","Battery":"90Wh"}, reviews=["Battery life is stronger than most gaming laptops", "Display is decent", "Great Linux and coding machine"]),
    Product(id="lap-3", title="Lenovo LOQ 15", brand="Lenovo", category="laptop", image="https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=800", price=79990, rating=4.3, specs={"CPU":"Intel i5-12450H","GPU":"RTX 4060 8GB","RAM":"16GB","Storage":"512GB SSD","Weight":"2.4 kg","Battery":"60Wh"}, reviews=["Best GPU in this range", "Heavy to carry", "Thermals are reliable"]),
    Product(id="lap-4", title="HP Victus 16", brand="HP", category="laptop", image="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800", price=76990, rating=4.2, specs={"CPU":"Ryzen 5 7640HS","GPU":"RTX 3050 6GB","RAM":"16GB","Storage":"512GB SSD","Weight":"2.3 kg","Battery":"70Wh"}, reviews=["Large screen helps productivity", "Build has minor wobble", "Quiet balanced mode"]),
    Product(id="lap-5", title="MSI Thin 15", brand="MSI", category="laptop", image="https://images.unsplash.com/photo-1484788984921-03950022c9ef?w=800", price=69990, rating=4.1, specs={"CPU":"Intel i7-12650H","GPU":"RTX 3050 4GB","RAM":"16GB","Storage":"512GB SSD","Weight":"1.86 kg","Battery":"52Wh"}, reviews=["Light for a gaming laptop", "Battery is average", "Fast compiler performance"]),
    Product(id="lap-6", title="Apple MacBook Air M2", brand="Apple", category="laptop", image="https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=800", price=82990, rating=4.8, specs={"CPU":"Apple M2","GPU":"Integrated 10-core","RAM":"8GB","Storage":"256GB SSD","Weight":"1.24 kg","Battery":"52.6Wh"}, reviews=["Superb battery life", "Not for AAA gaming", "Fantastic portability"]),
]

class MockProductProvider(ProductProvider):
    async def search(self, requirements: RequirementProfile, query: str) -> list[Product]:
        products = [p for p in MOCK_PRODUCTS if not requirements.category or requirements.category.lower() in p.category.lower()]
        return products or MOCK_PRODUCTS
