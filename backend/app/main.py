from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .media import media_summary, probe_media
from .tasks import process_source

ROOT = Path(__file__).resolve().parents[2]
MEDIA_DIR = ROOT / "media"
OUTPUT_DIR = ROOT / "outputs"
MEDIA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
MAX_UPLOAD_BYTES = 10 * 1024 * 1024 * 1024
ALLOWED_SUFFIXES = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}

app = FastAPI(title="ClipForge", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
jobs: dict[str, dict] = {}

class JobRequest(BaseModel):
    source_url: str = Field(min_length=1, max_length=2048)
    clip_count: int = Field(default=5, ge=1, le=20)
    min_seconds: int = Field(default=60, ge=15, le=180)
    max_seconds: int = Field(default=90, ge=15, le=300)
    prompt: str | None = Field(default=None, max_length=1000)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "clipforge", "version": app.version}

@app.post("/api/jobs", status_code=202)
def create_job(request: JobRequest):
    if request.min_seconds > request.max_seconds:
        raise HTTPException(status_code=422, detail="min_seconds must not exceed max_seconds")
    job_id = str(uuid4())
    payload = {"id": job_id, "status": "queued", "progress": 0, "request": request.model_dump(), "clips": [], "error": None}
    jobs[job_id] = payload
    try:
        task = process_source.delay(request.source_url, job_id)
        payload["task_id"] = task.id
        payload["status"] = "submitted"
    except Exception as exc:
        payload["status"] = "failed"
        payload["error"] = f"Worker unavailable: {exc}"
    return payload

@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@app.get("/api/jobs")
def list_jobs():
    return list(jobs.values())

@app.post("/api/media/upload", status_code=201)
def upload_media(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(status_code=415, detail=f"Unsupported media type: {suffix or 'missing extension'}")
    media_id = str(uuid4())
    destination = MEDIA_DIR / f"{media_id}{suffix}"
    size = 0
    try:
        with destination.open("wb") as output:
            while chunk := file.file.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_UPLOAD_BYTES:
                    destination.unlink(missing_ok=True)
                    raise HTTPException(status_code=413, detail="Media file exceeds the 10 GB limit")
                output.write(chunk)
        metadata = media_summary(probe_media(destination))
    except HTTPException:
        raise
    except Exception as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(status_code=422, detail=f"Media validation failed: {exc}") from exc
    return {"media_id": media_id, "filename": file.filename, "path": str(destination), "metadata": metadata}
