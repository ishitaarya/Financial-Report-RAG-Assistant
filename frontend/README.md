# FinSight React frontend

A responsive React + Vite interface for the Financial Report RAG Assistant. This frontend is designed for deployment on Vercel.

## Run locally

```bash
cd frontend
npm install
cp .env.example .env
# Set VITE_API_BASE_URL to your running FastAPI backend
npm run dev
```

## Vercel deployment

1. Import this GitHub repository into Vercel.
2. Set **Root Directory** to `frontend`.
3. Framework preset: **Vite**.
4. Build command: `npm run build`.
5. Output directory: `dist`.
6. Add the environment variable `VITE_API_BASE_URL` with the public URL of your FastAPI backend.
7. Deploy.

## Backend API contract

The current repository contains a Streamlit application, not an HTTP API. The React interface therefore needs a separately deployed FastAPI backend implementing these endpoints:

### `POST /api/upload`
Multipart form field: `file` (PDF).

Expected JSON response:
```json
{
  "document_id": "unique-document-id",
  "filename": "annual-report.pdf",
  "pages": 42,
  "chunks": 128
}
```

### `POST /api/ask`
JSON request:
```json
{ "document_id": "unique-document-id", "question": "What was the revenue?" }
```

Expected JSON response:
```json
{
  "answer": "The report states ...",
  "sources": [
    { "page": 12, "content": "Relevant report passage", "score": 0.82 }
  ]
}
```

### `POST /api/summary`
JSON request:
```json
{ "document_id": "unique-document-id" }
```

Expected JSON response:
```json
{ "summary": "Executive summary text..." }
```

The backend must also allow browser requests from your Vercel domain using CORS. Keep the Gemini API key on the backend; never put it in a `VITE_*` variable or frontend source code.

Until `VITE_API_BASE_URL` is configured and these endpoints are available, the UI will display a backend connection notice rather than pretending that report processing has succeeded.
