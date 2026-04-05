# Doggy - Dog Breed Identifier

Doggy is a full-stack web application where a user uploads a dog photo and gets:
- AI-based breed recognition
- short care/lifestyle advice for the detected breed

The project includes a React frontend, a FastAPI backend, tests, CI workflows, and an OpenAPI contract.

## Project Structure

Repository modules:
- `backend/`: FastAPI app, core features, tests, Docker/Fly.io files
- `web/`: React + TypeScript + Vite frontend
- `openapi/`: API specification (`openapi.yaml`)
- `.github/workflows/`: CI/CD workflows for backend and web
- `.vscode/`: VS Code tasks for setup and local run
- `docs/`: project documentation files
- `LICENSE`: project license (MIT)
- `CHANGELOG.md`: release notes and documented changes

```text
artifact/
|- backend/
|  |- __init__.py
|  |- main.py
|  |- Core/
|  |  `- router.py
|  |- Features/
|  |  |- DogRecognition/
|  |  |  `- dog_recognition.py
|  |  `- LLM/
|  |     `- llm_engine.py
|  |- tests/
|  `- fly.toml
|- web/
|  |- src/
|  |  |- main.tsx
|  |  |- App.tsx
|  |  |- hooks/
|  |  |  `- useBreedIdentification.ts
|  |  `- components/ui/
|  |     `- DogInfoPanel.tsx
|  `- package.json
|- openapi/
|  `- openapi.yaml
|- .vscode/
|  `- tasks.json
|- docs/
|- LICENSE
|- CHANGELOG.md
`- .github/workflows/
   |- backend-ci.yml
   |- web-ci.yml
   `- backend-deploy.yml
```

## How to do stuff

### Run locally

Backend (terminal 1), from `backend/`:

```bash
./setup.sh
source venv/bin/activate
uvicorn main:app --reload
```

Frontend (terminal 2), from `web/`:

```bash
npm install
npm run dev
```

### Run from VS Code

This repository includes VS Code tasks in `.vscode/tasks.json`.

1. Open project root (`artifact/`) in VS Code.
2. Run `Terminal -> Run Task...`.
3. Select one of the prepared tasks:
   - `App: Bootstrap` for first-time setup + run (backend + frontend)
   - `App: Start` to start backend and frontend after setup
   - `Backend: Check` to run backend quality checks

### Run on web (Fly.io)

Deployed backend URL:
- `https://doggy-black-darkness-694.fly.dev/`

If the app was idle, Fly.io may need a short cold start on the first request.
If you get a timeout, wait a bit and retry.

To run frontend locally against deployed backend:

```bash
cd web
VITE_API_BASE_URL=https://doggy-black-darkness-694.fly.dev npm run dev
```

### Run quality checks

Backend:

```bash
cd backend
source venv/bin/activate
./check.sh
```

Frontend:

```bash
cd web
npm run lint
npm run test:ci
npm run build
```

### Update API contract

OpenAPI spec is in:
- `openapi/openapi.yaml`

### Release backend

Create and push a backend release tag:

```bash
git tag backend/1.0.0
git push origin backend/1.0.0
```

This triggers `.github/workflows/backend-deploy.yml` and deploys backend to Fly.io.
This repository does not publish backend packages to PyPI.

## CI/CD

Backend and web checks run via GitHub Actions workflows in:
- `.github/workflows/backend-ci.yml`
- `.github/workflows/web-ci.yml`
- `.github/workflows/backend-deploy.yml` (backend deploy on `backend/v*` tags)

## Contributing

Contributions are welcome.

1. Create a feature/fix branch from `dev`.
2. Make changes and run local checks:
   - backend: `cd backend && ./check.sh`
   - frontend: `cd web && npm run lint && npm run test:ci && npm run build`
3. Open a pull request to `dev` with a short description of changes.

## Authors

Main contributors (by commit history):
- Diana Zhigalkina
- Alina Yakubova
- Sveta Vertegel
```

## License

This project is licensed under the MIT License.
See `LICENSE` for details.
