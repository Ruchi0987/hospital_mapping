from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "hospitals.json"


class SuggestRequest(BaseModel):
    disease: str = Field(..., min_length=2, max_length=120)


class HospitalSuggestion(BaseModel):
    name: str
    departments: list[str]
    location: str
    contact: str
    match_score: float


class SuggestResponse(BaseModel):
    disease_query: str
    model: str
    suggestions: list[HospitalSuggestion]


app = FastAPI(title="Hospital Mapping AI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _load_hospitals() -> list[dict[str, Any]]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_PATH}")
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _build_index(hospitals: list[dict[str, Any]]) -> tuple[TfidfVectorizer, Any]:
    corpus: list[str] = []
    for hospital in hospitals:
        disease_terms = " ".join(hospital["diseases"])
        departments = " ".join(hospital["departments"])
        text = f"{disease_terms} {departments}"
        corpus.append(text)

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    matrix = vectorizer.fit_transform(corpus)
    return vectorizer, matrix


HOSPITALS = _load_hospitals()
VECTORIZER, INDEX_MATRIX = _build_index(HOSPITALS)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/suggest", response_model=SuggestResponse)
def suggest_hospitals(payload: SuggestRequest) -> SuggestResponse:
    query = payload.disease.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Disease query cannot be empty.")

    query_vector = VECTORIZER.transform([query])
    scores = cosine_similarity(query_vector, INDEX_MATRIX).flatten()

    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    suggestions: list[HospitalSuggestion] = []

    for idx, score in ranked[:3]:
        hospital = HOSPITALS[idx]
        if score <= 0:
            continue
        suggestions.append(
            HospitalSuggestion(
                name=hospital["name"],
                departments=hospital["departments"],
                location=hospital["location"],
                contact=hospital["contact"],
                match_score=round(float(score), 3),
            )
        )

    return SuggestResponse(
        disease_query=query,
        model="TF-IDF + cosine similarity baseline",
        suggestions=suggestions,
    )
