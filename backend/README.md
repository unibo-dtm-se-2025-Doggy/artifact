# Backend API

FastAPI backend for the Doggy project.

## Requirements

- Python 3.12.8 (see `.python-version`)
- `pip`
- A Bash-compatible shell for the automation scripts

## Platform Setup

### Windows

- Install Git for Windows and use Git Bash if you want to run `./setup.sh` and `./check.sh`.
- If you do not want to use Git Bash, follow the manual setup steps from PowerShell instead.
- VS Code tasks in `.vscode/tasks.json` assume `bash` is available on your `PATH`.

### macOS / Linux

- The provided `.sh` scripts should run in the default terminal.
- If `pyenv` is not installed, use the manual setup path instead of `./setup.sh`.

## Setup

### Automatic Setup (`setup.sh`)

Run the setup script from the `backend` directory:

```bash
./setup.sh
```

The script will:

- check the Python version from `.python-version`
- create a virtual environment in `venv`
- install dependencies from `requirements.txt`

### Manual Setup

1. Create a virtual environment:

```bash
python3 -m venv venv
```

2. Activate the virtual environment:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## VS Code Tasks

If you use VS Code, you can run the backend scripts without typing the commands manually:

- `Terminal` -> `Run Task` -> `Backend: Setup`
- `Terminal` -> `Run Task` -> `Backend: Check`
- `Terminal` -> `Run Task` -> `Frontend: Setup`
- `Terminal` -> `Run Task` -> `Backend: Run API`
- `Terminal` -> `Run Task` -> `Frontend: Run UI`
- `Terminal` -> `Run Task` -> `App: Bootstrap`
- `Terminal` -> `Run Task` -> `App: Start`

`App: Bootstrap` runs `Backend: Setup`, then `Frontend: Setup`, then launches both the backend API and the frontend dev server.

`App: Start` only launches the backend API and the frontend dev server using the already installed dependencies.

The run tasks prompt for ports before starting `uvicorn` and Vite.

### Quick Start in VS Code

1. Open the project root folder in VS Code.
2. Open `Terminal` -> `Run Task`.
3. Open `Terminal` -> `Run Task` again.
4. Run `App: Bootstrap` the first time.
5. Enter the backend port when prompted (default: `8000`).
6. Enter the frontend port when prompted (default: `5173`).
7. Open `http://localhost:5173` in the browser.

After the first successful setup, use `App: Start` for normal day-to-day launches.

If `App: Start` fails, run `Backend: Run API` or `Frontend: Run UI` separately to see which side is missing dependencies.

If the backend task says `backend/venv is missing`, `Backend: Setup` did not complete successfully.
The backend task starts the API from the repository root so `backend.main:app` can resolve package imports correctly.

## Running the API

1. Make sure the virtual environment is activated:

```bash
source venv/bin/activate
```

2. Create a `.env` file with your Hugging Face token:

```bash
echo "HF_TOKEN=your_token_here" > .env
```

Optional: if you want to change the LLM used for advice generation, review supported hosted models here:

- https://huggingface.co/inference/models

Then set a model identifier in `.env`, for example:

```bash
echo "HF_LLM_MODEL=meta-llama/Llama-3.1-8B-Instruct" >> .env
```

3. Start the server:

```bash
uvicorn main:app --reload
```

The default server URL is `http://localhost:8000`.

To use a different port:

```bash
uvicorn main:app --reload --port 8001
```

From the repository root, the equivalent command is:

```bash
PYTHONPATH=. backend/venv/bin/python -m uvicorn backend.main:app --reload --port 8000
```

## API Endpoints

- `GET /` - Health check endpoint
- `GET /api/dog-advice?breed=<breed_name>` - Get breed-specific advice
- `POST /api/dog-from-photo` - Upload a photo to recognize the dog breed and get advice

## Example Requests

Get breed advice:

```bash
curl "http://localhost:8000/api/dog-advice?breed=Golden%20Retriever"
```

Upload a photo:

```bash
curl -X POST "http://localhost:8000/api/dog-from-photo" \
  -F "file=@dog_photo.jpg"
```

## Project Structure

```text
backend/
|-- Core/              # Core components
|-- Features/          # Feature modules
|   |-- DogRecognition/
|   `-- LLM/
|-- main.py            # FastAPI entry point
|-- requirements.txt   # Python dependencies
|-- setup.sh           # Project setup script
|-- check.sh           # Code quality check script
|-- pyproject.toml     # Ruff and mypy configuration
|-- Dockerfile         # Docker configuration for deployment
|-- fly.toml           # Fly.io configuration
`-- .dockerignore      # Docker ignore patterns
```

## Code Quality

### Scripted Checks

Run all local checks from the `backend` directory:

```bash
./check.sh
```

This runs:

- `ruff check`
- `ruff format --check`
- `mypy` (non-blocking)
- Python syntax validation

The same flow is available in VS Code via the `Backend: Check` task.

### Manual Checks

Format code:

```bash
ruff format .
```

Fix linting issues:

```bash
ruff check . --fix
```

Type checking:

```bash
mypy . --ignore-missing-imports
```

## CI

GitHub Actions automatically runs checks on push and pull request events:

- `ruff` linting
- `ruff format --check`
- `mypy`
- backend tests with coverage

See `.github/workflows/backend-ci.yml` for details.

## Deployment to Fly.io

The backend can be deployed to Fly.io, and the repository already includes `fly.toml`.
Backend release automation in this repository is deployment to Fly.io only.
There is no backend publish step to PyPI in the release workflow.

### Initial Setup

1. Install the Fly.io CLI:

```bash
curl -L https://fly.io/install.sh | sh
```

2. Log in:

```bash
flyctl auth login
```

3. Create the app if needed:

```bash
cd backend
flyctl launch
```

4. Set the backend secret:

```bash
flyctl secrets set HF_TOKEN=your_huggingface_token_here
```

5. Add `FLY_API_TOKEN` to GitHub Actions secrets.

### Release Flow

After backend changes are merged, create and push a `backend/v*` tag:

```bash
git tag backend/v1.0.0
git push origin backend/v1.0.0
```

This tag triggers `.github/workflows/backend-deploy.yml`, which deploys the backend to Fly.io.

### Billing Note

Billing details change over time, so verify them before production use.

As of March 1, 2026:

- New Fly.io organizations use pay-as-you-go billing.
- The old fixed plans are only retained for older legacy customers.
- Fly.io has a limited free trial, not a permanent free tier for new accounts.
- The current free trial is 2 total VM hours or 7 days, whichever comes first.
- After the trial ends, a payment method is required to keep apps running.

Official references:

- https://fly.io/pricing/
- https://fly.io/docs/about/pricing/
- https://fly.io/docs/about/free-trial/

## Python Version

Python is pinned in `.python-version`.

If you already use `pyenv`, you can align to that version with:

```bash
pyenv install $(cat .python-version)
pyenv local $(cat .python-version)
```
