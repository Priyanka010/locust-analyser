# Locust Analyzer API (PDF Support)

This FastAPI service accepts a **PDF Locust report**, extracts text using `pdfplumber`, and analyzes it using Vertex AI's Gemini model.

## Deployment

Deploy to Cloud Run after setting:

- `GCP_PROJECT`
- `GCP_REGION`

## API

- `POST /analyze`: Upload a Locust report PDF