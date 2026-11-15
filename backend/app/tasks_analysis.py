from __future__ import annotations
import json
from pathlib import Path
from uuid import uuid4
from .discovery import build_windows
from .downloader import download_source
from .media import media_summary, probe_media
from .transcription_adapter import TranscriptionError, transcribe
from .worker import celery_app

@celery_app.task(bind=True, name="clipforge.process_source")
def process_source(self, source_url: str, job_id: str) -> dict:
    workspace = Path("/app/media") / "jobs" / job_id
    workspace.mkdir(parents=True, exist_ok=True)
    self.update_state(state="PROGRESS", meta={"stage": "downloading", "progress": 10})
    source = download_source(source_url, workspace)
    self.update_state(state="PROGRESS", meta={"stage": "probing", "progress": 25})
    metadata = media_summary(probe_media(source))
    self.update_state(state="PROGRESS", meta={"stage": "transcribing", "progress": 40})
    try:
        words = transcribe(source)
        windows = build_windows(words)
        (workspace / "transcript.json").write_text(json.dumps([word.__dict__ for word in words]), encoding="utf-8")
        window_data = [window.__dict__ for window in windows]
    except TranscriptionError as exc:
        return {"job_id": job_id, "stage": "source_ready", "progress": 30, "source": str(source), "metadata": metadata, "warning": str(exc), "windows": []}
    self.update_state(state="PROGRESS", meta={"stage": "discovered", "progress": 55})
    return {"job_id": job_id, "stage": "discovered", "progress": 55, "source": str(source), "metadata": metadata, "windows": window_data}

def new_job_id() -> str:
    return str(uuid4())
