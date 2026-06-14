from __future__ import annotations
import os, re, uuid
from typing import TypedDict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph
from app.models.schemas import Recommendation, RequirementProfile, Product, SearchResponse, ChatMessage
from app.providers import get_provider

load_dotenv()

class CommerceState(TypedDict):
    query: str
    session_id: str
    history: list[ChatMessage]
    requirements: RequirementProfile
    products: list[Product]
    filtered: list[Product]
    recommendations: list[Recommendation]
    assistant_message: str

llm = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"), google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.25) if os.getenv("GOOGLE_API_KEY") else None

def _extract_budget(text: str) -> float | None:
    normalized = text.replace(",", "")
    match = re.search(r"(?:under|below|less than|upto|up to|₹|rs\.?|inr)\s*₹?\s*(\d{4,7})", normalized, re.I)
    return float(match.group(1)) if match else None

def requirement_extraction(state: CommerceState) -> CommerceState:
    text = " ".join([m.content for m in state.get("history", [])] + [state["query"]]).lower()
    req = RequirementProfile(
        category="laptop" if "laptop" in text or "coding" in text or "gaming" in text else None,
        budget_max=_extract_budget(text),
        brands_excluded=[b for b in ["Lenovo", "Acer", "ASUS", "HP", "MSI", "Apple"] if f"exclude {b.lower()}" in text or f"no {b.lower()}" in text],
        priorities=[p for p in ["battery life", "lightweight", "gaming", "coding", "display", "performance"] if p in text or (p == "lightweight" and "lighter" in text)],
        use_cases=[u for u in ["coding", "gaming", "travel", "office"] if u in text],
    )
    state["requirements"] = req
    return state

async def product_search(state: CommerceState) -> CommerceState:
    state["products"] = await get_provider().search(state["requirements"], state["query"])
    return state

def filtering(state: CommerceState) -> CommerceState:
    req = state["requirements"]
    products = state["products"]
    if req.budget_max:
        products = [p for p in products if p.price <= req.budget_max]
    if req.brands_excluded:
        products = [p for p in products if p.brand.lower() not in {b.lower() for b in req.brands_excluded}]
    state["filtered"] = products
    return state

def _score(product: Product, req: RequirementProfile) -> float:
    score = product.rating * 10
    text = " ".join([product.title, product.brand, *product.specs.values(), *product.reviews]).lower()
    for priority in req.priorities + req.use_cases:
        if priority in text:
            score += 8
    if "battery life" in req.priorities and "90wh" in text: score += 15
    if "lightweight" in req.priorities or "lighter" in req.priorities:
        weight = re.search(r"([0-9.]+)\s*kg", text)
        if weight: score += max(0, 25 - float(weight.group(1)) * 8)
    if req.budget_max:
        score += max(0, (req.budget_max - product.price) / req.budget_max * 10)
    return round(score, 2)

def review_analysis(state: CommerceState) -> CommerceState:
    recs = []
    for p in state["filtered"]:
        review_text = " ".join(p.reviews).lower()
        pros = ["Strong user rating", "Good value for the requested budget"]
        cons = []
        if "battery" in review_text: pros.append("Battery performance is frequently mentioned")
        if "loud" in review_text: cons.append("Can get loud under load")
        if "heavy" in review_text: cons.append("Heavier than ultraportable options")
        if "average" in review_text: cons.append("Some aspects are average versus competitors")
        recs.append(Recommendation(product=p, score=_score(p, state["requirements"]), pros=pros[:3], cons=cons[:3], explanation=""))
    state["recommendations"] = sorted(recs, key=lambda r: r.score, reverse=True)[:5]
    return state

def recommendation(state: CommerceState) -> CommerceState:
    req = state["requirements"]
    for rec in state["recommendations"]:
        p = rec.product
        rec.explanation = f"{p.title} fits your {', '.join(req.use_cases or req.priorities or ['shopping'])} needs with a {p.specs.get('CPU', 'balanced platform')}, {p.specs.get('GPU', 'capable graphics')}, {p.rating}/5 rating, and price of ₹{p.price:,.0f}."
    state["assistant_message"] = f"I found {len(state['recommendations'])} strong matches. You can refine by brand, weight, battery life, performance, or budget."
    return state

builder = StateGraph(CommerceState)
builder.add_node("requirement_extraction", requirement_extraction)
builder.add_node("product_search", product_search)
builder.add_node("filtering", filtering)
builder.add_node("review_analysis", review_analysis)
builder.add_node("recommendation", recommendation)
builder.set_entry_point("requirement_extraction")
builder.add_edge("requirement_extraction", "product_search")
builder.add_edge("product_search", "filtering")
builder.add_edge("filtering", "review_analysis")
builder.add_edge("review_analysis", "recommendation")
builder.add_edge("recommendation", END)
graph = builder.compile()

async def run_commerce_agent(query: str, session_id: str | None, history: list[ChatMessage]) -> SearchResponse:
    final = await graph.ainvoke({"query": query, "session_id": session_id or str(uuid.uuid4()), "history": history, "requirements": RequirementProfile(), "products": [], "filtered": [], "recommendations": [], "assistant_message": ""})
    comparison = [{"Product": r.product.title, "Brand": r.product.brand, "Price": r.product.price, "Rating": r.product.rating, **r.product.specs} for r in final["recommendations"]]
    return SearchResponse(session_id=final["session_id"], requirements=final["requirements"], recommendations=final["recommendations"], comparison=comparison, assistant_message=final["assistant_message"])
