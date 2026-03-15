# Doggy - Dog Breed Identifier

Doggy is a full-stack web application where a user uploads a dog photo and gets:
- AI-based breed recognition
- short care/lifestyle advice for the detected breed

The project includes a React frontend, a FastAPI backend, tests, CI workflows, and an OpenAPI contract.

## Current Status

Implementation already exists.

Repository currently contains:
- `backend/`: FastAPI app, core features, tests, Docker/Fly.io files
- `web/`: React + TypeScript + Vite frontend
- `openapi/`: API specification (`openapi.yaml`)
- `.github/workflows/`: CI/CD workflows for backend and web
- `docs/`: project documentation files

## Repository Structure

```text
artifact/
|- backend/
|- web/
|- openapi/
|- docs/
`- .github/workflows/
```

## Local Run (Quick Start)

### Backend

From `backend/`:

```bash
./setup.sh
source venv/bin/activate
uvicorn main:app --reload
```

### Frontend

From `web/`:

```bash
npm install
npm run dev
```

## API Contract

OpenAPI spec is in:
- `openapi/openapi.yaml`

## CI

Backend and web checks run via GitHub Actions workflows in:
- `.github/workflows/backend-ci.yml`
- `.github/workflows/web-ci.yml`

Backend release deployment is handled by `.github/workflows/backend-deploy.yml` on `backend/v*` tags to Fly.io (no PyPI publish flow in this repository).
