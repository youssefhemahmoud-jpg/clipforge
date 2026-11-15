# ClipForge

Local-first AI video clipping studio for turning long videos into reviewable vertical clips.

## Current pipeline foundation

- FastAPI API with validated URL jobs and local media uploads
- Redis + Celery worker plumbing
- yt-dlp source adapter
- ffprobe metadata validation
- FFmpeg 9:16 render primitive with output validation
- Explainable candidate scoring and overlap removal
- React dashboard with prompt-driven and automatic-discovery entry points

## Run locally with Docker

```bash
mkdir -p media outputs
# Windows PowerShell: New-Item -ItemType Directory media, outputs

docker compose up --build
```

Open the dashboard at http://localhost:5173 and API health at http://localhost:8000/api/health.

## Backend tests

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Current limitation

The worker currently downloads and probes sources. Transcription, complete-thought candidate discovery, caption rendering, smart face/gameplay tracking, and final batch export are the next pipeline stages. Runtime Docker/FFmpeg checks must be run on the target PC.

Use only footage you own or are licensed to process. Keep uploads private by default.
