# Hospital Mapping AI Web App

This project is a full-stack MVP for your idea:

- **Problem:** People don't know which hospital treats which disease.
- **Solution:** User enters a disease; app returns relevant hospitals, departments, location, and contact.

## Architecture

- **Frontend:** HTML/CSS/Vanilla JS (quick MVP UI)
- **Backend:** FastAPI REST API
- **AI/ML layer:** TF-IDF + cosine similarity ranking over disease/department text
- **Data store:** JSON (swap with PostgreSQL later)
- **Deployment:** Docker container, cloud-ready

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

Open `frontend/index.html` in browser (or serve with any static server).

## API

### Health

`GET /api/health`

### Suggestions

`POST /api/suggest`

Body:

```json
{
  "disease": "heart problem"
}
```

## Deployment plan (production)

1. **Containerize** with Dockerfile.
2. **Deploy backend** on Render/Railway/AWS ECS.
3. **Host frontend** on Vercel/Netlify/S3.
4. Set frontend `API_BASE` to deployed backend URL.
5. Add PostgreSQL + Redis for scale.
6. Add auth + rate limiting + monitoring.

## AI/ML upgrades

- Replace TF-IDF with sentence-transformers embeddings.
- Fine-tune on real hospital and treatment taxonomy data.
- Add LLM assistant for natural language triage and explanations.
- Use hybrid retrieval (vector + metadata filters by city/insurance).

## Suggested tech stack till deployment

- **Frontend:** React + TypeScript + Tailwind (next step from this MVP)
- **Backend:** FastAPI + Pydantic + Uvicorn/Gunicorn
- **ML:** scikit-learn baseline, then sentence-transformers + FAISS
- **DB:** PostgreSQL
- **Queue:** Celery/RQ with Redis for async model tasks
- **Infra:** Docker + GitHub Actions CI/CD + cloud hosting (Render/AWS/GCP)
- **Observability:** Prometheus/Grafana + Sentry
