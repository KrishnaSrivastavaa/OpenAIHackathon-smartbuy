from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    session_id: str | None = None
    history: list[ChatMessage] = Field(default_factory=list)

class RequirementProfile(BaseModel):
    category: str | None = None
    budget_max: float | None = None
    currency: str = "INR"
    brands_excluded: list[str] = Field(default_factory=list)
    priorities: list[str] = Field(default_factory=list)
    use_cases: list[str] = Field(default_factory=list)
    constraints: dict[str, Any] = Field(default_factory=dict)

class Product(BaseModel):
    id: str
    title: str
    brand: str
    category: str
    image: str
    price: float
    currency: str = "INR"
    rating: float
    specs: dict[str, str]
    reviews: list[str] = Field(default_factory=list)

class Recommendation(BaseModel):
    product: Product
    score: float
    pros: list[str]
    cons: list[str]
    explanation: str

class SearchResponse(BaseModel):
    session_id: str
    requirements: RequirementProfile
    recommendations: list[Recommendation]
    comparison: list[dict[str, str | float]]
    assistant_message: str
