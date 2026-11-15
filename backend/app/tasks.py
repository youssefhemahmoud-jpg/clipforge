from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from .downloader import download_source
from .media import media_summary, probe_media
from .worker import celery_app

@celery_app.task(bind=True, name="clipforge.process_source")
def process_source(self, source_url: str, job_id: str) -> dict:
    workspace = Path("/app/media") / "jobs" / job_id
    self.update_state(state="PROGRESS", meta={"stage": "downloading", "progress": 10})
    source = download_source(source_url, workspace)
    self.update_state(state="PROGRESS", meta={"stage": "probing", "progress": 25})
    metadata = media_summary(probe_media(source))
    return {"job_id": job_id, "stage": "source_ready", "progress": 30, "source": str(source), "metadata": metadata}


def new_job_id() -> str:
    return str(uuid4())
